"""
配置文件
"""
import os

# AgentGuard 配置
AGENTGUARD_URL = os.getenv("AGENTGUARD_URL", "http://localhost:8080")
AGENTGUARD_API_KEY = os.getenv("AGENTGUARD_API_KEY", "ag_a7da48efa685469b84bbfa039b52020a")

# AI 模型配置
AI_MODEL = os.getenv("AI_MODEL", "z-ai/glm4.7")
