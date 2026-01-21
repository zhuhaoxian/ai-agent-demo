"""
星火 AI 客户端模块
封装与星火 API 的交互逻辑
"""
import json
import requests
from typing import List, Dict, Any, Tuple

from tools_config import FUNCTION_TOOLS, WEB_SEARCH_TOOLS
from config import SPARK_MODEL


class SparkClient:
    """星火 AI 客户端"""
    
    def __init__(self, api_key: str, api_url: str = "https://spark-api-open.xf-yun.com/v2/chat/completions"):
        """
        初始化客户端
        
        Args:
            api_key: API 密钥（格式：Bearer AK:SK）
            api_url: API 地址
        """
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            'Authorization': api_key,
            'content-type': "application/json"
        }
    
    def chat(
        self,
        messages: List[Dict[str, Any]],
        use_web_search: bool = False,
        stream: bool = True,
        model: str = SPARK_MODEL,
        user_id: str = "user_id"
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            use_web_search: 是否使用网络搜索工具
            stream: 是否流式返回
            model: 模型名称
            user_id: 用户ID
            
        Returns:
            (完整回复内容, 工具调用列表)
        """
        # 根据参数选择工具类型
        selected_tools = WEB_SEARCH_TOOLS if use_web_search else FUNCTION_TOOLS
        
        body = {
            "model": model,
            "user": user_id,
            "messages": messages,
            "stream": stream,
            "tools": selected_tools
        }
        
        full_response = ""
        tool_calls_dict = {}
        is_first_content = True
        
        response = requests.post(
            url=self.api_url,
            json=body,
            headers=self.headers,
            stream=stream
        )
        
        for chunks in response.iter_lines():
            if chunks and '[DONE]' not in str(chunks):
                data_org = chunks[6:]
                chunk = json.loads(data_org)
                text = chunk['choices'][0]['delta']
                
                # 处理思维链内容
                if 'reasoning_content' in text and text['reasoning_content']:
                    print(text["reasoning_content"], end="", flush=True)
                
                # 处理最终结果内容
                if 'content' in text and text['content']:
                    content = text["content"]
                    if is_first_content:
                        print("\n*******************以上为思维链内容，模型回复内容如下********************\n")
                        is_first_content = False
                    print(content, end="", flush=True)
                    full_response += content
                
                # 处理工具调用（流式返回需要合并）
                if 'tool_calls' in text and text['tool_calls']:
                    self._merge_tool_calls(text['tool_calls'], tool_calls_dict)
        
        tool_calls = list(tool_calls_dict.values())
        return full_response, tool_calls
    
    @staticmethod
    def _merge_tool_calls(tool_call_chunks: List[Dict], tool_calls_dict: Dict[int, Dict]) -> None:
        """合并流式返回的工具调用信息"""
        for tool_call_chunk in tool_call_chunks:
            index = tool_call_chunk.get('index', 0)
            
            if index not in tool_calls_dict:
                # 初始化新的 tool_call
                tool_calls_dict[index] = {
                    'id': tool_call_chunk.get('id', ''),
                    'type': tool_call_chunk.get('type', 'function'),
                    'function': {
                        'name': tool_call_chunk.get('function', {}).get('name', ''),
                        'arguments': ''
                    }
                }
            
            # 合并 id
            if 'id' in tool_call_chunk and tool_call_chunk['id']:
                tool_calls_dict[index]['id'] = tool_call_chunk['id']
            
            # 合并 function name 和 arguments
            if 'function' in tool_call_chunk:
                if 'name' in tool_call_chunk['function'] and tool_call_chunk['function']['name']:
                    tool_calls_dict[index]['function']['name'] = tool_call_chunk['function']['name']
                
                if 'arguments' in tool_call_chunk['function']:
                    tool_calls_dict[index]['function']['arguments'] += tool_call_chunk['function']['arguments']
