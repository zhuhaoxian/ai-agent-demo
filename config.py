"""
配置文件
存储 API 密钥和其他配置信息
"""

# 星火 API 配置
SPARK_API_KEY = "Bearer ZcYhmLHcVoGROVMKCuAo:YeYTZYojWRblNcUrhoGa"
SPARK_API_URL = "https://spark-api-open.xf-yun.com/v2/chat/completions"
SPARK_MODEL = "x1"

# 业务系统 API 配置
BUSINESS_API_BASE = "http://localhost:9090"
BUSINESS_API_TIMEOUT = 10

# 对话配置
MAX_CHAT_HISTORY_LENGTH = 11000  # 最大对话历史长度（字符数）
MAX_TOOL_ITERATIONS = 5  # 最大工具调用轮次
