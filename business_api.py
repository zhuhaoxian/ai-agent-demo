"""
业务 API 调用模块
封装所有与业务系统交互的 API 调用函数
所有请求通过 AgentGuard 代理服务转发
"""
import requests
from typing import Optional, Dict, Any

from config import (
    BUSINESS_API_BASE,
    BUSINESS_API_TIMEOUT,
    AGENTGUARD_BUSINESS_PROXY_URL,
    AGENTGUARD_API_KEY
)


def _handle_api_error(e: requests.exceptions.RequestException) -> Dict[str, str]:
    """统一处理 API 错误"""
    return {"error": f"API调用失败: {str(e)}"}


def _call_via_agentguard(
    target_url: str,
    method: str = "GET",
    body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    通过 AgentGuard 代理服务调用目标 API（新版业务API代理端点）

    Args:
        target_url: 目标 API 的完整 URL
        method: HTTP 方法（GET、POST、PUT、DELETE 等）
        body: 请求体数据
        headers: 请求头

    Returns:
        AgentGuard 代理响应或错误信息
    """
    try:
        # 构造 AgentGuard 代理请求（新版格式）
        proxy_request = {
            "apiKey": AGENTGUARD_API_KEY,
            "targetUrl": target_url,
            "method": method,
            "headers": headers or {"Content-Type": "application/json"}
        }

        # 只有在有请求体时才添加 body 字段
        if body is not None:
            proxy_request["body"] = body

        # 发送请求到 AgentGuard 业务API代理服务（新版端点）
        response = requests.post(
            AGENTGUARD_BUSINESS_PROXY_URL,
            json=proxy_request,
            timeout=BUSINESS_API_TIMEOUT
        )
        response.raise_for_status()

        # 解析 AgentGuard 响应
        proxy_response = response.json()

        # 如果 AgentGuard 返回了目标 API 的响应数据，提取出来
        if proxy_response.get("code") == 200 and "data" in proxy_response:
            data = proxy_response["data"]
            # 如果状态是成功，返回实际的响应数据
            if data.get("status") == "SUCCESS" and "response" in data:
                return data["response"]

        # 否则返回完整的代理响应
        return proxy_response

    except requests.exceptions.RequestException as e:
        return _handle_api_error(e)


def get_all_customers() -> Dict[str, Any]:
    """获取所有客户列表（通过 AgentGuard 代理）"""
    return _call_via_agentguard(
        target_url=f"{BUSINESS_API_BASE}/api/customers",
        method="GET"
    )


def get_all_orders() -> Dict[str, Any]:
    """获取所有订单列表（通过 AgentGuard 代理）"""
    return _call_via_agentguard(
        target_url=f"{BUSINESS_API_BASE}/api/orders",
        method="GET"
    )


def create_customer(
    name: str,
    phone: str,
    level: str,
    email: Optional[str] = None,
    address: Optional[str] = None
) -> Dict[str, Any]:
    """新增客户（通过 AgentGuard 代理）"""
    body = {"name": name, "phone": phone, "level": level}
    if email:
        body["email"] = email
    if address:
        body["address"] = address
    
    return _call_via_agentguard(
        target_url=f"{BUSINESS_API_BASE}/api/customers",
        method="POST",
        body=body
    )


def update_customer(
    id: int,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    level: Optional[str] = None
) -> Dict[str, Any]:
    """修改客户信息（通过 AgentGuard 代理）"""
    body = {}
    if name:
        body["name"] = name
    if phone:
        body["phone"] = phone
    if email:
        body["email"] = email
    if address:
        body["address"] = address
    if level:
        body["level"] = level
    
    return _call_via_agentguard(
        target_url=f"{BUSINESS_API_BASE}/api/customers/{id}",
        method="PUT",
        body=body
    )


def create_order(
    orderNo: str,
    productId: int,
    productName: str,
    quantity: int,
    totalAmount: float,
    status: str,
    customerName: str,
    customerPhone: str
) -> Dict[str, Any]:
    """新增订单（通过 AgentGuard 代理）"""
    body = {
        "orderNo": orderNo,
        "productId": productId,
        "productName": productName,
        "quantity": quantity,
        "totalAmount": totalAmount,
        "status": status,
        "customerName": customerName,
        "customerPhone": customerPhone
    }
    
    return _call_via_agentguard(
        target_url=f"{BUSINESS_API_BASE}/api/orders",
        method="POST",
        body=body
    )


def update_order(
    id: int,
    orderNo: Optional[str] = None,
    productId: Optional[int] = None,
    productName: Optional[str] = None,
    quantity: Optional[int] = None,
    totalAmount: Optional[float] = None,
    status: Optional[str] = None,
    customerName: Optional[str] = None,
    customerPhone: Optional[str] = None
) -> Dict[str, Any]:
    """修改订单信息（通过 AgentGuard 代理）"""
    body = {}
    if orderNo:
        body["orderNo"] = orderNo
    if productId:
        body["productId"] = productId
    if productName:
        body["productName"] = productName
    if quantity is not None:
        body["quantity"] = quantity
    if totalAmount is not None:
        body["totalAmount"] = totalAmount
    if status:
        body["status"] = status
    if customerName:
        body["customerName"] = customerName
    if customerPhone:
        body["customerPhone"] = customerPhone
    
    return _call_via_agentguard(
        target_url=f"{BUSINESS_API_BASE}/api/orders/{id}",
        method="PUT",
        body=body
    )


# 函数映射表
AVAILABLE_FUNCTIONS = {
    "get_all_customers": get_all_customers,
    "get_all_orders": get_all_orders,
    "create_customer": create_customer,
    "update_customer": update_customer,
    "create_order": create_order,
    "update_order": update_order
}
