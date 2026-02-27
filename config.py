"""
配置文件
"""
import os

# AgentGuard 配置
AGENTGUARD_URL = os.getenv("AGENTGUARD_URL", "http://localhost:8080")
AGENTGUARD_API_KEY = os.getenv("AGENTGUARD_API_KEY", "ag_2a6d77701a734dffb93a3f68198f7db9")

# AI 模型配置
AI_MODEL = os.getenv("AI_MODEL", "gpt-5-mini")
