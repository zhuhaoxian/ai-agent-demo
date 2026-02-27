"""
业务工具定义
定义 Agent 可以调用的业务函数和工具
"""
from typing import Dict, Any
from agentguard_zhx import AgentGuardHTTP
from config import AGENTGUARD_URL, AGENTGUARD_API_KEY

# 初始化 AgentGuard HTTP 客户端（用于业务 API 调用）
http = AgentGuardHTTP(
    agentguard_url=AGENTGUARD_URL,
    agent_api_key=AGENTGUARD_API_KEY
)

# ============ 业务函数实现 ============

def get_weather(city: str) -> dict:
    """获取天气信息（模拟）"""
    # 实际场景：调用真实的天气 API
    # return http.get(f"https://api.weather.com/v1/weather?city={city}")

    # Demo 模拟
    return {
        "city": city,
        "temperature": "25°C",
        "weather": "晴天",
        "humidity": "60%"
    }


def send_email(to: str, subject: str, content: str) -> dict:
    """发送邮件（通过 AgentGuard 代理）"""
    # 实际场景：调用真实的邮件 API，自动经过 AgentGuard 代理
    # return http.post(
    #     "https://api.sendgrid.com/v3/mail/send",
    #     json={
    #         "personalizations": [{"to": [{"email": to}]}],
    #         "from": {"email": "noreply@example.com"},
    #         "subject": subject,
    #         "content": [{"type": "text/plain", "value": content}]
    #     }
    # )

    # Demo 模拟（如果配置了策略规则，这个调用会被拦截）
    return {
        "status": "success",
        "message": f"邮件已发送到 {to}",
        "subject": subject
    }


def get_all_orders() -> dict:
    """获取所有订单列表"""
    return http.get("http://localhost:9090/api/orders")


def update_order(
    id: int,
    orderNo: str = None,
    productName: str = None,
    quantity: int = None,
    totalAmount: float = None,
    status: str = None,
    customerName: str = None,
    customerPhone: str = None
) -> dict:
    """修改订单信息"""
    body = {}
    if orderNo: body["orderNo"] = orderNo
    if productName: body["productName"] = productName
    if quantity is not None: body["quantity"] = quantity
    if totalAmount is not None: body["totalAmount"] = totalAmount
    if status: body["status"] = status
    if customerName: body["customerName"] = customerName
    if customerPhone: body["customerPhone"] = customerPhone
    return http.put(f"http://localhost:9090/api/orders/{id}", json=body)

# ============ 工具定义（OpenAI Function Calling 格式）============

BUSINESS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "收件人邮箱地址"
                    },
                    "subject": {
                        "type": "string",
                        "description": "邮件主题"
                    },
                    "content": {
                        "type": "string",
                        "description": "邮件内容"
                    }
                },
                "required": ["to", "subject", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_orders",
            "description": "获取所有订单列表",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_order",
            "description": "修改订单信息。可以修改订单编号、产品信息、数量、总金额、状态和客户信息。订单状态必须是PENDING、PAID、SHIPPED、COMPLETED或CANCELLED之一。",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "订单ID"
                    },
                    "orderNo": {
                        "type": "string",
                        "description": "订单编号（可选）"
                    },
                    "productId": {
                        "type": "integer",
                        "description": "产品ID（可选）"
                    },
                    "productName": {
                        "type": "string",
                        "description": "产品名称（可选）"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "购买数量（可选）"
                    },
                    "totalAmount": {
                        "type": "number",
                        "description": "订单总金额（可选）"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["PENDING", "PAID", "SHIPPED", "COMPLETED", "CANCELLED"],
                        "description": "订单状态（可选），必须是PENDING、PAID、SHIPPED、COMPLETED或CANCELLED"
                    },
                    "customerName": {
                        "type": "string",
                        "description": "客户姓名（可选）"
                    },
                    "customerPhone": {
                        "type": "string",
                        "description": "客户电话（可选）"
                    }
                },
                "required": ["id"]
            }
        }
    }
]

# ============ 函数映射 ============

BUSINESS_FUNCTIONS = {
    "get_weather": get_weather,
    "send_email": send_email,
    "get_all_orders": get_all_orders,
    "update_order": update_order
}
