"""
AI 对话主程序
支持 Function Call 和 Web Search 功能
兼容 OpenAI 格式的 API
"""
import json
from typing import List, Dict, Any

from ai_client import AIClient
from chat_manager import ChatManager
from business_api import AVAILABLE_FUNCTIONS
from tools_config import WEB_SEARCH_KEYWORDS
from config import AGENTGUARD_API_KEY, AGENTGUARD_LLM_PROXY_URL, MAX_TOOL_ITERATIONS


class ChatBot:
    """聊天机器人"""
    
    def __init__(self, api_key: str, base_url: str):
        """初始化聊天机器人"""
        self.client = AIClient(api_key, base_url)
        self.chat_manager = ChatManager()
    
    def should_use_web_search(self, user_input: str) -> bool:
        """判断是否需要使用网络搜索"""
        return any(keyword in user_input.lower() for keyword in WEB_SEARCH_KEYWORDS)
    
    def process_tool_calls(
        self,
        tool_calls: List[Dict[str, Any]],
        use_web_search: bool
    ) -> str:
        """
        处理工具调用
        
        Args:
            tool_calls: 工具调用列表
            use_web_search: 是否使用网络搜索模式
            
        Returns:
            最终回复内容
        """
        iteration = 0
        answer = ""
        
        while tool_calls and iteration < MAX_TOOL_ITERATIONS:
            iteration += 1
            
            # 过滤有效的工具调用
            valid_tool_calls = [
                tc for tc in tool_calls
                if tc.get("function", {}).get("name") and 
                   tc.get("function", {}).get("name") in AVAILABLE_FUNCTIONS
            ]
            
            if not valid_tool_calls:
                if tool_calls:  # 有工具调用但都无效
                    print("\n[警告: 检测到无效的工具调用，跳过]")
                break
            
            print(f"\n[第{iteration}轮工具调用，检测到 {len(valid_tool_calls)} 个有效工具请求]")
            
            # 将助手的回复添加到历史
            self.chat_manager.add_message("assistant", answer, tool_calls=tool_calls)
            
            # 执行每个工具调用
            for tool_call in valid_tool_calls:
                self._execute_tool_call(tool_call)
            
            # 再次调用模型
            print("\nAI:", end="")
            answer, tool_calls = self.client.chat(
                self.chat_manager.get_history(),
                use_web_search=use_web_search
            )
            print()  # 换行
        
        if iteration >= MAX_TOOL_ITERATIONS:
            print("\n[警告: 达到最大工具调用次数限制]")
        
        return answer
    
    def _execute_tool_call(self, tool_call: Dict[str, Any]) -> None:
        """执行单个工具调用"""
        function_name = tool_call["function"]["name"]
        function_args_str = tool_call["function"].get("arguments", "{}")
        
        print(f"[调用函数: {function_name}]")
        print(f"[参数: {function_args_str}]")
        
        try:
            function_args = json.loads(function_args_str) if function_args_str else {}
        except json.JSONDecodeError as e:
            print(f"[错误: 参数解析失败 - {e}]")
            return
        
        # 执行函数
        try:
            function_to_call = AVAILABLE_FUNCTIONS[function_name]
            function_response = function_to_call(**function_args)
            
            # 显示函数返回内容
            print("[返回内容]")
            print(json.dumps(function_response, ensure_ascii=False, indent=2))
            
            # 将函数执行结果添加到对话历史
            self.chat_manager.add_message(
                "tool",
                json.dumps(function_response, ensure_ascii=False),
                tool_call_id=tool_call["id"]
            )
            print(f"[函数执行完成]")
        except TypeError as e:
            error_msg = f"参数错误: {str(e)}"
            print(f"[错误: {error_msg}]")
            self.chat_manager.add_message(
                "tool",
                json.dumps({"error": error_msg}, ensure_ascii=False),
                tool_call_id=tool_call["id"]
            )
        except Exception as e:
            error_msg = f"执行失败: {str(e)}"
            print(f"[错误: {error_msg}]")
            self.chat_manager.add_message(
                "tool",
                json.dumps({"error": error_msg}, ensure_ascii=False),
                tool_call_id=tool_call["id"]
            )
    
    def chat(self, user_input: str) -> None:
        """处理用户输入"""
        # 检测是否需要使用网络搜索
        use_web_search = self.should_use_web_search(user_input)
        if use_web_search:
            print("[使用网络搜索模式]")
        
        # 添加用户消息到历史
        self.chat_manager.add_message("user", user_input)
        
        # 开始输出模型内容
        print("AI:", end="")
        answer, tool_calls = self.client.chat(
            self.chat_manager.get_history(),
            use_web_search=use_web_search
        )
        print()  # 换行
        
        # 处理工具调用
        if tool_calls:
            answer = self.process_tool_calls(tool_calls, use_web_search)
        
        # 添加最终回复到历史
        if answer:
            self.chat_manager.add_message("assistant", answer)


def main():
    """主程序入口"""
    print("==" * 60)
    print("AI 对话系统（通过 AgentGuard 代理）")
    print("支持 Function Call 和 Web Search 功能")
    print("输入空行退出")
    print("=" * 60)

    # 使用 AgentGuard 代理来调用 LLM
    bot = ChatBot(AGENTGUARD_API_KEY, AGENTGUARD_LLM_PROXY_URL)
    
    while True:
        try:
            user_input = input("\n我: ")
            if not user_input:
                print("再见！")
                break
            
            bot.chat(user_input)
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n[错误: {e}]")


if __name__ == '__main__':
    main()
