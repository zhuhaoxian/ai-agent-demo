"""
配置文件模板
请复制此文件为 config.py 并填入真实的配置信息
"""

# AI 模型 API 配置
# 支持任何兼容 OpenAI 格式的 API
# 例如：
# - OpenAI: base_url="https://api.openai.com/v1", model="gpt-4"
# - 星火: base_url="https://spark-api-open.xf-yun.com/v2", model="x1"
# - ChatAnywhere: base_url="https://api.chatanywhere.tech/v1", model="gpt-3.5-turbo"

AI_API_KEY = "your-api-key-here"  # 替换为你的 API Key
AI_BASE_URL = "https://api.chatanywhere.tech/v1"  # 替换为你的 API 地址
AI_MODEL = "gpt-3.5-turbo"  # 替换为你要使用的模型

# 业务系统 API 配置
BUSINESS_API_BASE = "http://localhost:9090"
BUSINESS_API_TIMEOUT = 10

# AgentGuard 代理配置
AGENTGUARD_PROXY_URL = "http://localhost:8080/proxy/v1/request"
AGENTGUARD_API_KEY = "ag_your_agentguard_key_here"  # 替换为你的 AgentGuard API Key

# 对话配置
MAX_CHAT_HISTORY_LENGTH = 11000  # 最大对话历史长度（字符数）
MAX_TOOL_ITERATIONS = 5  # 最大工具调用轮次
