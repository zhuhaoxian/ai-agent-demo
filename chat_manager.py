"""
对话管理模块
管理对话历史和上下文
"""
from typing import List, Dict, Any

from config import MAX_CHAT_HISTORY_LENGTH


class ChatManager:
    """对话历史管理器"""
    
    def __init__(self, max_length: int = MAX_CHAT_HISTORY_LENGTH):
        """
        初始化对话管理器
        
        Args:
            max_length: 对话历史最大长度（字符数）
        """
        self.history: List[Dict[str, Any]] = []
        self.max_length = max_length
    
    def add_message(self, role: str, content: str, **kwargs) -> None:
        """
        添加消息到历史
        
        Args:
            role: 角色（user/assistant/tool）
            content: 消息内容
            **kwargs: 其他参数（如 tool_calls, tool_call_id 等）
        """
        message = {"role": role, "content": content}
        message.update(kwargs)
        self.history.append(message)
        self._check_length()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.history
    
    def clear(self) -> None:
        """清空对话历史"""
        self.history.clear()
    
    def _get_total_length(self) -> int:
        """计算对话历史总长度"""
        total = 0
        for message in self.history:
            content = message.get("content", "")
            if content:
                total += len(str(content))
        return total
    
    def _check_length(self) -> None:
        """检查并裁剪过长的对话历史"""
        while self._get_total_length() > self.max_length and len(self.history) > 0:
            self.history.pop(0)
