"""
AI Agent 实现
使用 AgentGuard SDK 统一管理 LLM 调用和审批流程
"""
import json
from typing import List, Dict, Any
from agentguard import AgentGuardOpenAI

from config import AGENTGUARD_URL, AGENTGUARD_API_KEY, AI_MODEL
from tools import BUSINESS_TOOLS, BUSINESS_FUNCTIONS


class SimpleAgent:
    """简单的 AI Agent，集成 AgentGuard"""

    def __init__(self):
        """初始化 Agent"""
        # 1. 初始化 AgentGuard 客户端
        self.client = AgentGuardOpenAI(
            agentguard_url=AGENTGUARD_URL,
            agent_api_key=AGENTGUARD_API_KEY
        )

        # 2. SDK 自动合并业务工具和 AgentGuard 审批工具
        self.tools = self.client.merge_tools(BUSINESS_TOOLS)

        # 3. SDK 自动合并业务函数和 AgentGuard 审批函数
        self.functions = self.client.get_function_map(BUSINESS_FUNCTIONS)
        # 对话历史
        self.messages = [
            {
                "role": "system",
                "content": """
                            当操作被拦截需要审批时，请：
                            1. 告知用户该操作需要审批，并提取审批ID
                            2. 引导用户说明操作理由（为什么需要执行此操作）
                            3. 提交理由后，告知用户已提交并等待审批
                            """
            }
        ]

    def chat(self, user_input: str, stream: bool = True) -> str:
        """
        与用户对话

        Args:
            user_input: 用户输入
            stream: 是否使用流式传输

        Returns:
            Agent 回复
        """
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})

        if stream:
            # 流式传输
            return self._chat_stream()
        else:
            # 非流式传输
            return self._chat_non_stream()

    def _chat_non_stream(self) -> str:
        """非流式对话处理"""
        # 调用 LLM
        response = self.client.chat.completions.create(
            model=AI_MODEL,
            messages=self.messages,
            tools=self.tools,
            stream=False
        )

        message = response.choices[0].message
        assistant_message = message.content or ""

        # 处理工具调用
        if message.tool_calls:
            # 添加 assistant 消息
            self.messages.append({
                "role": "assistant",
                "content": assistant_message,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # 执行工具调用
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"\n[工具调用] {function_name}({function_args})")

                # 执行函数
                if function_name in self.functions:
                    result = self.functions[function_name](**function_args)
                else:
                    result = {"error": f"未知函数: {function_name}"}

                # 添加工具结果
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

            # 再次调用 LLM 获取最终回复
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=self.messages,
                tools=self.tools,
                stream=False
            )

            assistant_message = response.choices[0].message.content

        # 添加 assistant 消息
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def _chat_stream(self) -> str:
        """流式对话处理"""
        # 调用 LLM
        stream = self.client.chat.completions.create(
            model=AI_MODEL,
            messages=self.messages,
            tools=self.tools,
            stream=True
        )

        # 累积响应内容
        assistant_message = ""
        # 累积 tool_calls
        tool_calls_accumulator = {}  

        print("\nAgent: ", end="", flush=True)

        # 处理流式响应
        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            # 累积内容
            if delta.content:
                content = delta.content
                assistant_message += content
                print(content, end="", flush=True)

            # 累积 tool_calls
            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    idx = tc_delta.index
                    if idx not in tool_calls_accumulator:
                        tool_calls_accumulator[idx] = {
                            "id": tc_delta.id or "",
                            "type": "function",
                            "function": {
                                "name": tc_delta.function.name or "",
                                "arguments": ""
                            }
                        }

                    # 累积函数参数
                    if tc_delta.function.arguments:
                        tool_calls_accumulator[idx]["function"]["arguments"] += tc_delta.function.arguments

        print()

        # 转换累积的 tool_calls 为列表
        tool_calls = [tool_calls_accumulator[i] for i in sorted(tool_calls_accumulator.keys())] if tool_calls_accumulator else None

        # 处理工具调用
        if tool_calls:
            # 添加 assistant 消息
            self.messages.append({
                "role": "assistant",
                "content": assistant_message,
                "tool_calls": tool_calls
            })

            # 执行工具调用
            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])

                print(f"\n[工具调用] {function_name}({function_args})")

                # 执行函数
                if function_name in self.functions:
                    result = self.functions[function_name](**function_args)
                else:
                    result = {"error": f"未知函数: {function_name}"}

                # 添加工具结果
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(result, ensure_ascii=False)
                })

            # 再次调用 LLM 获取最终回复
            stream = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=self.messages,
                tools=self.tools,
                stream=True
            )

            assistant_message = ""
            print("\nAgent: ", end="", flush=True)

            for chunk in stream:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                if delta.content:
                    content = delta.content
                    assistant_message += content
                    print(content, end="", flush=True)

            print()

        # 添加 assistant 消息
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message
