"""
AI 客户端模块
封装与 AI API 的交互逻辑（使用 OpenAI 官方库）
兼容 OpenAI 格式的 API（OpenAI、星火、ChatAnywhere 等）
支持 AgentGuard 审批流程自动处理
"""
from typing import List, Dict, Any, Tuple, Optional
from openai import OpenAI
import time
import requests
import json

from tools_config import FUNCTION_TOOLS, WEB_SEARCH_TOOLS
from config import AI_MODEL


class AIClient:
    """AI 客户端（基于 OpenAI 库），支持 AgentGuard 审批流程处理"""

    # 提交审批理由工具定义
    SUBMIT_APPROVAL_REASON_TOOL = {
        "type": "function",
        "function": {
            "name": "submit_approval_reason",
            "description": "提交审批申请理由。当用户的请求需要审批时，使用此工具提交用户的申请理由，帮助审批人员更好地理解用户的需求。",
            "parameters": {
                "type": "object",
                "properties": {
                    "approval_id": {
                        "type": "string",
                        "description": "审批请求ID"
                    },
                    "reason": {
                        "type": "string",
                        "description": "申请理由，应该清晰说明用户为什么需要执行这个操作，包括操作目的、业务需求等"
                    }
                },
                "required": ["approval_id", "reason"]
            }
        }
    }

    # 查询审批状态工具定义
    CHECK_APPROVAL_STATUS_TOOL = {
        "type": "function",
        "function": {
            "name": "check_approval_status",
            "description": "查询审批状态。当用户想知道审批结果时，使用此工具查询当前的审批状态（待审批/已通过/已拒绝/已过期）。注意：此工具只查询一次，不会轮询等待。",
            "parameters": {
                "type": "object",
                "properties": {
                    "approval_id": {
                        "type": "string",
                        "description": "审批请求ID"
                    }
                },
                "required": ["approval_id"]
            }
        }
    }

    # 审批轮询配置（内部实现细节，用于 LLM 请求审批的直接处理）
    APPROVAL_POLL_INTERVAL = 10  # 轮询间隔（秒）
    APPROVAL_MAX_WAIT = 300  # 最大等待时间（秒）

    def __init__(self, api_key: str, base_url: str, agentguard_api_url: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: API 密钥
            base_url: API 基础地址
            agentguard_api_url: AgentGuard 管理 API 地址（用于查询审批状态）
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.agentguard_api_url = agentguard_api_url
        self.api_key = api_key
    
    def chat(
        self,
        messages: List[Dict[str, Any]],
        use_web_search: bool = False,
        stream: bool = True,
        model: str = AI_MODEL,
        user_id: str = "user_id",
        enable_thinking: bool = True
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            use_web_search: 是否使用网络搜索工具
            stream: 是否流式返回
            model: 模型名称
            user_id: 用户ID
            enable_thinking: 是否启用思维链（某些模型可能需要）
            
        Returns:
            (完整回复内容, 工具调用列表)
        """
        # 根据参数选择工具类型
        # 注意：WEB_SEARCH_TOOLS 是星火模型专属格式，其他模型可能不支持
        # selected_tools = WEB_SEARCH_TOOLS if use_web_search else FUNCTION_TOOLS
        selected_tools = FUNCTION_TOOLS.copy()

        # 添加审批工具（如果配置了 AgentGuard API URL）
        if self.agentguard_api_url:
            selected_tools.append(self.SUBMIT_APPROVAL_REASON_TOOL)
            selected_tools.append(self.CHECK_APPROVAL_STATUS_TOOL)
        
        full_response = ""
        tool_calls_dict = {}
        is_first_content = True
        
        # 构建请求参数
        request_params = {
            "model": model,
            "messages": messages,
            "tools": selected_tools,
            "stream": stream,
            "user": user_id
        }
        
        # 某些模型可能需要额外参数来启用思维链
        # 如果你的模型需要，可以取消下面的注释
        # if enable_thinking:
        #     request_params["reasoning_effort"] = "high"  # OpenAI o1 系列
        #     # 或者其他模型特定的参数
        
        # 使用 OpenAI 客户端发送请求
        response = self.client.chat.completions.create(**request_params)

        # 处理流式响应
        finish_reason = None
        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            # 处理思维链内容（如果存在）
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                print(delta.reasoning_content, end="", flush=True)

            # 处理最终结果内容
            if delta.content:
                if is_first_content:
                    print("\n*******************以上为思维链内容，模型回复内容如下********************\n")
                    is_first_content = False
                print(delta.content, end="", flush=True)
                full_response += delta.content

            # 处理工具调用（流式返回需要合并）
            if delta.tool_calls:
                self._merge_tool_calls_from_openai(delta.tool_calls, tool_calls_dict)

            # 检查完成原因
            if chunk.choices[0].finish_reason:
                finish_reason = chunk.choices[0].finish_reason

        tool_calls = list(tool_calls_dict.values())

        # 检查响应内容是否包含 AgentGuard 审批拦截信息
        # 检查响应内容是否包含 AgentGuard 审批拦截信息
        # 新流程：不再自动处理审批，而是返回特殊标记，让 AI 引导用户提供理由
        if "[AgentGuard 审批]" in full_response and "审批ID" in full_response:
            print("[检测到 LLM 请求被拦截，需要用户提供审批理由]")

            # 从响应中提取审批 ID
            import re
            match = re.search(r'审批ID[：:]\s*([a-f0-9]+)', full_response)
            if match:
                approval_id = match.group(1)
                print(f"[提取到审批ID: {approval_id}]")

                # 返回特殊标记，告诉 main.py 需要 AI 处理审批流程
                return full_response, [{
                    "_llm_approval_interception": True,
                    "approval_id": approval_id,
                    "interception_message": full_response
                }]
            else:
                print("[警告: 无法从响应中提取审批ID]")
                return full_response, []
        # 正常返回（没有审批拦截）
        return full_response, tool_calls
    
    @staticmethod
    def _merge_tool_calls_from_openai(tool_call_chunks, tool_calls_dict: Dict[int, Dict]) -> None:
        """合并流式返回的工具调用信息（OpenAI 格式）"""
        for tool_call_chunk in tool_call_chunks:
            index = tool_call_chunk.index

            if index not in tool_calls_dict:
                # 初始化新的 tool_call
                tool_calls_dict[index] = {
                    'id': tool_call_chunk.id or '',
                    'type': tool_call_chunk.type or 'function',
                    'function': {
                        'name': '',
                        'arguments': ''
                    }
                }

            # 合并 id
            if tool_call_chunk.id:
                tool_calls_dict[index]['id'] = tool_call_chunk.id

            # 合并 function name 和 arguments
            if tool_call_chunk.function:
                if tool_call_chunk.function.name:
                    tool_calls_dict[index]['function']['name'] = tool_call_chunk.function.name

                if tool_call_chunk.function.arguments:
                    tool_calls_dict[index]['function']['arguments'] += tool_call_chunk.function.arguments

    def check_agentguard_approval_status(
        self,
        approval_id: str
    ) -> Dict[str, Any]:
        """
        轮询审批状态直到审批完成或超时

        根据 AgentGuard 审批状态查询接口规范实现：
        - PENDING：继续轮询
        - APPROVED：检查是否有 executionResult
          - 有 executionResult：返回执行结果
          - 无 executionResult：继续轮询（执行中）
        - REJECTED：返回拒绝原因
        - EXPIRED：返回过期信息

        Args:
            approval_id: 审批请求 ID

        Returns:
            审批结果，包含状态和执行结果/拒绝信息
        """
        if not self.agentguard_api_url:
            return {
                "status": "error",
                "message": "AgentGuard API URL 未配置"
            }

        print(f"\n[AgentGuard] 等待审批: {approval_id}")
        print(f"[AgentGuard] 轮询间隔: {self.APPROVAL_POLL_INTERVAL}秒")

        start_time = time.time()
        elapsed = 0

        while elapsed < self.APPROVAL_MAX_WAIT:
            try:
                # 查询审批状态
                response = requests.get(
                    f"{self.agentguard_api_url}/api/v1/approvals/{approval_id}/status",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )

                if response.status_code == 200:
                    result = response.json()

                    # 检查响应格式
                    if result.get("code") != 200:
                        print(f"[AgentGuard] API 返回错误: {result.get('message')}")
                        return {
                            "status": "error",
                            "message": result.get("message", "未知错误")
                        }

                    data = result.get("data", {})
                    status = data.get("status")

                    print(f"[AgentGuard] 审批状态: {status} (已等待 {int(elapsed)}秒)")

                    if status == "APPROVED":
                        # 审批通过，检查是否有执行结果
                        if "executionResult" in data:
                            execution_result = data["executionResult"]

                            # 检查是否是执行失败的情况
                            if "error" in execution_result:
                                print(f"[AgentGuard] 审批通过但执行失败: {execution_result['error']}")
                                return {
                                    "status": "execution_failed",
                                    "message": f"执行失败: {execution_result['error']}"
                                }

                            # 执行成功
                            print(f"[AgentGuard] 审批通过且执行成功！")
                            return {
                                "status": "approved",
                                "result": execution_result
                            }
                        else:
                            # 审批通过但还在执行中，继续轮询
                            print(f"[AgentGuard] 审批通过，正在执行中...")
                            time.sleep(self.APPROVAL_POLL_INTERVAL)
                            elapsed = time.time() - start_time
                            continue

                    elif status == "REJECTED":
                        # 审批被拒绝
                        rejection_reason = data.get("remark", "未提供拒绝原因")
                        print(f"[AgentGuard] 审批被拒绝: {rejection_reason}")
                        return {
                            "status": "rejected",
                            "message": f"审批被拒绝: {rejection_reason}"
                        }

                    elif status == "EXPIRED":
                        # 审批已过期
                        print(f"[AgentGuard] 审批已过期")
                        return {
                            "status": "expired",
                            "message": "审批请求已过期"
                        }

                    elif status == "PENDING":
                        # 继续等待审批
                        time.sleep(self.APPROVAL_POLL_INTERVAL)
                        elapsed = time.time() - start_time
                        continue

                    else:
                        # 未知状态
                        print(f"[AgentGuard] 未知审批状态: {status}")
                        return {
                            "status": "error",
                            "message": f"未知审批状态: {status}"
                        }

                elif response.status_code == 404:
                    print(f"[AgentGuard] 审批请求不存在")
                    return {
                        "status": "error",
                        "message": "审批请求不存在"
                    }

                else:
                    print(f"[AgentGuard] 查询审批状态失败: HTTP {response.status_code}")
                    time.sleep(self.APPROVAL_POLL_INTERVAL)
                    elapsed = time.time() - start_time

            except Exception as e:
                print(f"[AgentGuard] 查询审批状态异常: {e}")
                time.sleep(self.APPROVAL_POLL_INTERVAL)
                elapsed = time.time() - start_time

        # 超时
        print(f"[AgentGuard] 审批等待超时（{self.APPROVAL_MAX_WAIT}秒）")
        return {
            "status": "timeout",
            "message": f"审批等待超时（{self.APPROVAL_MAX_WAIT}秒）"
        }

    def _extract_content_from_result(self, execution_result: Any) -> str:
        """
        从执行结果中提取内容

        Args:
            execution_result: 执行结果（可能是完整的 LLM 响应）

        Returns:
            提取的文本内容
        """
        # 处理不同格式的执行结果
        if isinstance(execution_result, dict):
            # OpenAI 格式：{"choices": [{"message": {"content": "..."}}]}
            if "choices" in execution_result:
                choices = execution_result.get("choices", [])
                if choices and len(choices) > 0:
                    message = choices[0].get("message", {})
                    return message.get("content", "")

            # 简化格式：{"content": "..."}
            if "content" in execution_result:
                return execution_result.get("content", "")

            # 其他格式：尝试转换为 JSON 字符串
            return json.dumps(execution_result, ensure_ascii=False, indent=2)

        # 如果是字符串，直接返回
        return str(execution_result)
