"""
配置文件模板
请复制此文件为 config.py 并填入真实的配置信息
"""

# ============================================================================
# AgentGuard 代理配置（核心配置）
# ============================================================================
# 使用 AgentGuard 代理服务时，只需要配置以下内容：
# 1. AGENTGUARD_API_KEY - AgentGuard API 密钥（包含了模型、API地址等配置）
# 2. AGENTGUARD_LLM_PROXY_URL - LLM 代理端点
# 3. AGENTGUARD_BUSINESS_PROXY_URL - 业务 API 代理端点
# 4. AGENTGUARD_API_URL - 管理 API 地址

# AgentGuard API Key（包含模型配置信息）
AGENTGUARD_API_KEY = "ag_your_agentguard_key_here"  # 替换为你的 AgentGuard API Key

# LLM 代理端点：用于大模型 API 调用
AGENTGUARD_LLM_PROXY_URL = "http://localhost:8080/proxy/v1"

# 业务 API 代理端点：用于业务系统 API 调用
AGENTGUARD_BUSINESS_PROXY_URL = "http://localhost:8080/proxy/v1/api"

# AgentGuard 管理 API 地址：用于查询审批状态、提交审批理由等
AGENTGUARD_API_URL = "http://localhost:8080"

# ============================================================================
# AI 模型配置（仅用于满足 OpenAI 客户端 API 要求）
# ============================================================================
# 注意：使用 AgentGuard 代理时，以下配置会被忽略
# AgentGuard 会使用 API Key 中配置的模型和地址
# 这里的值仅用于满足 OpenAI 客户端库的 API 要求

AI_API_KEY = "placeholder"  # 占位符，实际使用 AGENTGUARD_API_KEY
AI_BASE_URL = "placeholder"  # 占位符，实际使用 AGENTGUARD_LLM_PROXY_URL
AI_MODEL = "gpt-3.5-turbo"  # 占位符，实际模型由 AgentGuard 配置决定

# ============================================================================
# 业务系统 API 配置
# ============================================================================
BUSINESS_API_BASE = "http://localhost:9090"
BUSINESS_API_TIMEOUT = 10

# ============================================================================
# 对话配置
# ============================================================================
MAX_CHAT_HISTORY_LENGTH = 11000  # 最大对话历史长度（字符数）
MAX_TOOL_ITERATIONS = 5  # 最大工具调用轮次
