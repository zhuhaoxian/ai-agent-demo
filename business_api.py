"""
业务 API 调用模块
封装所有与业务系统交互的 API 调用函数
"""
import requests
from typing import Optional, Dict, Any

from config import BUSINESS_API_BASE, BUSINESS_API_TIMEOUT


def _handle_api_error(e: requests.exceptions.RequestException) -> Dict[str, str]:
    """统一处理 API 错误"""
    return {"error": f"API调用失败: {str(e)}"}


def get_all_customers() -> Dict[str, Any]:
    """获取所有客户列表"""
    try:
        response = requests.get(f"{BUSINESS_API_BASE}/api/customers", timeout=BUSINESS_API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e)


def get_all_orders() -> Dict[str, Any]:
    """获取所有订单列表"""
    try:
        response = requests.get(f"{BUSINESS_API_BASE}/api/orders", timeout=BUSINESS_API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e)


def create_customer(
    name: str,
    phone: str,
    level: str,
    email: Optional[str] = None,
    address: Optional[str] = None
) -> Dict[str, Any]:
    """新增客户"""
    try:
        data = {"name": name, "phone": phone, "level": level}
        if email:
            data["email"] = email
        if address:
            data["address"] = address
        
        response = requests.post(
            f"{BUSINESS_API_BASE}/api/customers",
            json=data,
            timeout=BUSINESS_API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e)


def update_customer(
    id: int,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    level: Optional[str] = None
) -> Dict[str, Any]:
    """修改客户信息"""
    try:
        data = {}
        if name:
            data["name"] = name
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if address:
            data["address"] = address
        if level:
            data["level"] = level
        
        response = requests.put(
            f"{BUSINESS_API_BASE}/api/customers/{id}",
            json=data,
            timeout=BUSINESS_API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e)


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
    """新增订单"""
    try:
        data = {
            "orderNo": orderNo,
            "productId": productId,
            "productName": productName,
            "quantity": quantity,
            "totalAmount": totalAmount,
            "status": status,
            "customerName": customerName,
            "customerPhone": customerPhone
        }
        
        response = requests.post(
            f"{BUSINESS_API_BASE}/api/orders",
            json=data,
            timeout=BUSINESS_API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e)


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
    """修改订单信息"""
    try:
        data = {}
        if orderNo:
            data["orderNo"] = orderNo
        if productId:
            data["productId"] = productId
        if productName:
            data["productName"] = productName
        if quantity is not None:
            data["quantity"] = quantity
        if totalAmount is not None:
            data["totalAmount"] = totalAmount
        if status:
            data["status"] = status
        if customerName:
            data["customerName"] = customerName
        if customerPhone:
            data["customerPhone"] = customerPhone
        
        response = requests.put(
            f"{BUSINESS_API_BASE}/api/orders/{id}",
            json=data,
            timeout=BUSINESS_API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return _handle_api_error(e)


# 函数映射表
AVAILABLE_FUNCTIONS = {
    "get_all_customers": get_all_customers,
    "get_all_orders": get_all_orders,
    "create_customer": create_customer,
    "update_customer": update_customer,
    "create_order": create_order,
    "update_order": update_order
}
