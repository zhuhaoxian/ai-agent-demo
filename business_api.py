"""
业务 API 调用模块
封装所有与业务系统交互的 API 调用函数
所有请求通过 AgentGuard 代理服务转发
"""
import requests
import time
from typing import Optional, Dict, Any

from config import (
    BUSINESS_API_BASE,
    BUSINESS_API_TIMEOUT,
    AGENTGUARD_BUSINESS_PROXY_URL,
    AGENTGUARD_API_KEY,
    AGENTGUARD_API_URL
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



def submit_approval_reason(approval_id: str, reason: str) -> Dict[str, Any]:
    """
    提交审批申请理由

    Args:
        approval_id: 审批请求 ID
        reason: 申请理由

    Returns:
        提交结果
    """
    print(f"\n[AgentGuard] 提交审批理由: {approval_id}")
    print(f"[AgentGuard] 申请理由: {reason}")

    try:
        # 调用 AgentGuard API 提交审批理由
        response = requests.post(
            f"{AGENTGUARD_API_URL}/api/v1/approvals/{approval_id}/reason",
            headers={
                "Authorization": f"Bearer {AGENTGUARD_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"reason": reason},
            timeout=BUSINESS_API_TIMEOUT
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                print(f"[AgentGuard] 审批理由提交成功")

                # 从返回的 data 中提取审批请求信息
                data = result.get("data", {})
                application_reason = data.get("applicationReason", reason)  # 使用后端返回的理由，如果没有则使用提交的理由

                return {
                    "success": True,
                    "message": "审批理由已提交，等待审批人员审核",
                    "approval_id": approval_id,
                    "reason": application_reason,  # 返回后端确认的理由
                    "status": data.get("status", "PENDING"),
                    "expires_at": data.get("expiresAt"),
                    "policy_name": data.get("policyName")
                }
            else:
                return {
                    "success": False,
                    "message": result.get("message", "提交失败")
                }
        else:
            return {
                "success": False,
                "message": f"API 请求失败: HTTP {response.status_code}"
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "请求超时"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"提交失败: {str(e)}"
        }


def check_approval_status(approval_id: str) -> Dict[str, Any]:
    """
    查询 AgentGuard 审批状态（单次查询，不轮询）

    Args:
        approval_id: 审批请求 ID

    Returns:
        审批状态信息
    """
    print(f"\n[AgentGuard] 查询审批状态: {approval_id}")

    try:
        # 查询审批状态
        response = requests.get(
            f"{AGENTGUARD_API_URL}/api/v1/approvals/{approval_id}/status",
            headers={"Authorization": f"Bearer {AGENTGUARD_API_KEY}"},
            timeout=BUSINESS_API_TIMEOUT
        )

        if response.status_code == 200:
            result = response.json()

            # 检查响应格式
            if result.get("code") != 200:
                print(f"[AgentGuard] API 返回错误: {result.get('message')}")
                return {
                    "status": "error",
                    "message": result.get("message", "未知错误")
                }

            data = result.get("data", {})
            status = data.get("status")

            print(f"[AgentGuard] 审批状态: {status}")

            if status == "APPROVED":
                # 审批通过，检查是否有执行结果
                if "executionResult" in data:
                    execution_result = data["executionResult"]

                    # 检查是否是执行失败的情况
                    if "error" in execution_result:
                        print(f"[AgentGuard] 审批通过但执行失败: {execution_result['error']}")
                        return {
                            "status": "approved",
                            "execution_status": "failed",
                            "message": f"审批通过但执行失败: {execution_result['error']}",
                            "executionResult": execution_result
                        }

                    # 执行成功，提取内容
                    print(f"[AgentGuard] 审批通过且执行成功！")

                    # 提取执行结果中的内容
                    content = ""
                    if isinstance(execution_result, dict):
                        if "choices" in execution_result:
                            choices = execution_result.get("choices", [])
                            if choices and len(choices) > 0:
                                message = choices[0].get("message", {})
                                content = message.get("content", "")
                        elif "content" in execution_result:
                            content = execution_result.get("content", "")

                    return {
                        "status": "approved",
                        "execution_status": "success",
                        "message": "审批通过，执行成功",
                        "content": content,
                        "executionResult": execution_result
                    }
                else:
                    # 审批通过但还在执行中
                    print(f"[AgentGuard] 审批通过，正在执行中...")
                    return {
                        "status": "approved",
                        "execution_status": "pending",
                        "message": "审批通过，正在执行中，请稍后再次查询"
                    }

            elif status == "REJECTED":
                # 审批被拒绝
                rejection_reason = data.get("remark", "未提供拒绝原因")
                print(f"[AgentGuard] 审批被拒绝: {rejection_reason}")
                return {
                    "status": "rejected",
                    "message": f"审批被拒绝: {rejection_reason}",
                    "remark": rejection_reason
                }

            elif status == "EXPIRED":
                # 审批已过期
                print(f"[AgentGuard] 审批已过期")
                return {
                    "status": "expired",
                    "message": "审批请求已过期"
                }

            elif status == "PENDING":
                # 等待审批中
                print(f"[AgentGuard] 等待审批中")
                return {
                    "status": "pending",
                    "message": "审批请求等待处理中"
                }

            else:
                # 未知状态
                print(f"[AgentGuard] 未知审批状态: {status}")
                return {
                    "status": "error",
                    "message": f"未知审批状态: {status}"
                }

        elif response.status_code == 404:
            print(f"[AgentGuard] 审批请求不存在")
            return {
                "status": "error",
                "message": "审批请求不存在"
            }

        else:
            print(f"[AgentGuard] 查询审批状态失败: HTTP {response.status_code}")
            return {
                "status": "error",
                "message": f"查询失败: HTTP {response.status_code}"
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "请求超时"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"查询失败: {str(e)}"
        }


def check_agentguard_approval_status(approval_id: str) -> Dict[str, Any]:
    """
    查询 AgentGuard 审批状态并等待审批完成

    此函数会轮询审批状态，直到审批通过、拒绝、过期或超时。
    审批通过后，会返回后端自动执行的结果。

    Args:
        approval_id: 审批请求 ID

    Returns:
        审批结果，包含状态和执行结果/拒绝信息
    """
    POLL_INTERVAL = 10  # 轮询间隔（秒）
    MAX_WAIT = 300  # 最大等待时间（秒）

    print(f"\n[AgentGuard] 开始查询审批状态: {approval_id}")
    print(f"[AgentGuard] 轮询间隔: {POLL_INTERVAL}秒，最大等待: {MAX_WAIT}秒")

    start_time = time.time()
    elapsed = 0

    while elapsed < MAX_WAIT:
        try:
            # 查询审批状态
            response = requests.get(
                f"{AGENTGUARD_API_URL}/api/v1/approvals/{approval_id}/status",
                headers={"Authorization": f"Bearer {AGENTGUARD_API_KEY}"},
                timeout=BUSINESS_API_TIMEOUT
            )

            if response.status_code == 200:
                result = response.json()

                # 检查响应格式
                if result.get("code") != 200:
                    print(f"[AgentGuard] API 返回错误: {result.get('message')}")
                    return {
                        "status": "error",
                        "message": result.get("message", "未知错误")
                    }

                data = result.get("data", {})
                status = data.get("status")

                print(f"[AgentGuard] 审批状态: {status} (已等待 {int(elapsed)}秒)")

                if status == "APPROVED":
                    # 审批通过，检查是否有执行结果
                    if "executionResult" in data:
                        execution_result = data["executionResult"]

                        # 检查是否是执行失败的情况
                        if "error" in execution_result:
                            print(f"[AgentGuard] 审批通过但执行失败: {execution_result['error']}")
                            return {
                                "status": "execution_failed",
                                "message": f"审批通过但执行失败: {execution_result['error']}",
                                "executionResult": execution_result
                            }

                        # 执行成功，提取内容
                        print(f"[AgentGuard] 审批通过且执行成功！")

                        # 提取执行结果中的内容
                        content = ""
                        if isinstance(execution_result, dict):
                            if "choices" in execution_result:
                                choices = execution_result.get("choices", [])
                                if choices and len(choices) > 0:
                                    message = choices[0].get("message", {})
                                    content = message.get("content", "")
                            elif "content" in execution_result:
                                content = execution_result.get("content", "")

                        return {
                            "status": "approved",
                            "message": "审批通过，执行成功",
                            "content": content,
                            "executionResult": execution_result
                        }
                    else:
                        # 审批通过但还在执行中，继续轮询
                        print(f"[AgentGuard] 审批通过，正在执行中...")
                        time.sleep(POLL_INTERVAL)
                        elapsed = time.time() - start_time
                        continue

                elif status == "REJECTED":
                    # 审批被拒绝
                    rejection_reason = data.get("remark", "未提供拒绝原因")
                    print(f"[AgentGuard] 审批被拒绝: {rejection_reason}")
                    return {
                        "status": "rejected",
                        "message": f"审批被拒绝: {rejection_reason}",
                        "remark": rejection_reason
                    }

                elif status == "EXPIRED":
                    # 审批已过期
                    print(f"[AgentGuard] 审批已过期")
                    return {
                        "status": "expired",
                        "message": "审批请求已过期"
                    }

                elif status == "PENDING":
                    # 继续等待审批
                    time.sleep(POLL_INTERVAL)
                    elapsed = time.time() - start_time
                    continue

                else:
                    # 未知状态
                    print(f"[AgentGuard] 未知审批状态: {status}")
                    return {
                        "status": "error",
                        "message": f"未知审批状态: {status}"
                    }

            elif response.status_code == 404:
                print(f"[AgentGuard] 审批请求不存在")
                return {
                    "status": "error",
                    "message": "审批请求不存在"
                }

            else:
                print(f"[AgentGuard] 查询审批状态失败: HTTP {response.status_code}")
                time.sleep(POLL_INTERVAL)
                elapsed = time.time() - start_time

        except Exception as e:
            print(f"[AgentGuard] 查询审批状态异常: {e}")
            time.sleep(POLL_INTERVAL)
            elapsed = time.time() - start_time

    # 超时
    print(f"[AgentGuard] 审批等待超时（{MAX_WAIT}秒）")
    return {
        "status": "timeout",
        "message": f"审批等待超时（{MAX_WAIT}秒）"
    }


# 函数映射表
AVAILABLE_FUNCTIONS = {
    "get_all_customers": get_all_customers,
    "get_all_orders": get_all_orders,
    "create_customer": create_customer,
    "update_customer": update_customer,
    "create_order": create_order,
    "update_order": update_order,
    "submit_approval_reason": submit_approval_reason,
    "check_approval_status": check_approval_status,
    "check_agentguard_approval_status": check_agentguard_approval_status
}
