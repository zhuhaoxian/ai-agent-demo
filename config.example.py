"""
配置文件模板
请复制此文件为 config.py 并填入真实的配置信息
"""

# AI 模型 API 配置
# 注意：使用 AgentGuard 代理后，这些配置将在 AgentGuard 后台配置，而不是在这里
# AgentGuard 会自动管理 LLM API 的密钥和调用
AI_API_KEY = "your-api-key-here"  # 如果不使用 AgentGuard，填入你的 API Key
AI_BASE_URL = "https://api.chatanywhere.tech/v1"  # 如果不使用 AgentGuard，填入你的 API 地址
AI_MODEL = "gpt-3.5-turbo"  # 替换为你要使用的模型

# 业务系统 API 配置
BUSINESS_API_BASE = "http://localhost:9090"
BUSINESS_API_TIMEOUT = 10

# AgentGuard 代理配置（新版双层代理架构）
# LLM 代理端点：用于大模型 API 调用
AGENTGUARD_LLM_PROXY_URL = "http://localhost:8080/proxy/v1"
# 业务 API 代理端点：用于业务系统 API 调用
AGENTGUARD_BUSINESS_PROXY_URL = "http://localhost:8080/proxy/v1/api"
# AgentGuard API Key
AGENTGUARD_API_KEY = "ag_your_agentguard_key_here"  # 替换为你的 AgentGuard API Key

# 对话配置
MAX_CHAT_HISTORY_LENGTH = 11000  # 最大对话历史长度（字符数）
MAX_TOOL_ITERATIONS = 5  # 最大工具调用轮次
