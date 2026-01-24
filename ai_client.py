"""
AI 客户端模块
封装与 AI API 的交互逻辑（使用 OpenAI 官方库）
兼容 OpenAI 格式的 API（OpenAI、星火、ChatAnywhere 等）
"""
from typing import List, Dict, Any, Tuple
from openai import OpenAI

from tools_config import FUNCTION_TOOLS, WEB_SEARCH_TOOLS
from config import AI_MODEL


class AIClient:
    """AI 客户端（基于 OpenAI 库）"""
    
    def __init__(self, api_key: str, base_url: str):
        """
        初始化客户端
        
        Args:
            api_key: API 密钥
            base_url: API 基础地址
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
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
        selected_tools = FUNCTION_TOOLS
        
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
        
        tool_calls = list(tool_calls_dict.values())
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
