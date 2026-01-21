"""
工具配置模块
定义所有可用的工具，包括 Function 工具和 Web Search 工具
注意：web_search 和 function 不能同时使用
"""

# Function 工具列表（用于业务 API 调用）
FUNCTION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_all_customers",
            "description": "获取所有客户列表信息，包含客户ID、姓名、电话、邮箱、地址、等级和创建时间。",
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
            "name": "get_all_orders",
            "description": "获取所有订单列表信息，包含订单ID、订单编号、产品信息、数量、总金额、订单状态、客户信息和创建时间。",
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
            "name": "create_customer",
            "description": "新增客户信息。客户等级必须是VIP、GOLD或NORMAL之一。",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "客户姓名"
                    },
                    "phone": {
                        "type": "string",
                        "description": "联系电话"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["VIP", "GOLD", "NORMAL"],
                        "description": "客户等级，必须是VIP、GOLD或NORMAL"
                    },
                    "email": {
                        "type": "string",
                        "description": "电子邮箱（可选）"
                    },
                    "address": {
                        "type": "string",
                        "description": "联系地址（可选）"
                    }
                },
                "required": ["name", "phone", "level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_customer",
            "description": "修改客户信息。可以修改姓名、电话、邮箱、地址和等级。客户等级必须是VIP、GOLD或NORMAL之一。",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "客户ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "客户姓名（可选）"
                    },
                    "phone": {
                        "type": "string",
                        "description": "联系电话（可选）"
                    },
                    "email": {
                        "type": "string",
                        "description": "电子邮箱（可选）"
                    },
                    "address": {
                        "type": "string",
                        "description": "联系地址（可选）"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["VIP", "GOLD", "NORMAL"],
                        "description": "客户等级（可选），必须是VIP、GOLD或NORMAL"
                    }
                },
                "required": ["id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_order",
            "description": "新增订单信息。订单状态必须是PENDING、PAID、SHIPPED、COMPLETED或CANCELLED之一。",
            "parameters": {
                "type": "object",
                "properties": {
                    "orderNo": {
                        "type": "string",
                        "description": "订单编号"
                    },
                    "productId": {
                        "type": "integer",
                        "description": "产品ID"
                    },
                    "productName": {
                        "type": "string",
                        "description": "产品名称"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "购买数量"
                    },
                    "totalAmount": {
                        "type": "number",
                        "description": "订单总金额"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["PENDING", "PAID", "SHIPPED", "COMPLETED", "CANCELLED"],
                        "description": "订单状态，必须是PENDING、PAID、SHIPPED、COMPLETED或CANCELLED"
                    },
                    "customerName": {
                        "type": "string",
                        "description": "客户姓名"
                    },
                    "customerPhone": {
                        "type": "string",
                        "description": "客户电话"
                    }
                },
                "required": ["orderNo", "productId", "productName", "quantity", "totalAmount", "status", "customerName", "customerPhone"]
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

# Web Search 工具（用于网络搜索）
WEB_SEARCH_TOOLS = [
    {
        "type": "web_search",
        "web_search": {
            "enable": True,
            "search_mode": "normal"  # 可选 "deep" 或 "normal"，deep 模式搜索内容更丰富但 token 使用量更高
        }
    }
]

# 网络搜索关键词列表
WEB_SEARCH_KEYWORDS = ['搜索', 'search', '查询时间', '查询天气', '最新', '新闻', '今天', '现在']
