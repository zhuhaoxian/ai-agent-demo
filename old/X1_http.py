import json
import requests


# 请替换XXXXXXXXXX为您的 APIpassword, 获取地址：https://console.xfyun.cn/services/bmx1
api_key = "Bearer ZcYhmLHcVoGROVMKCuAo:YeYTZYojWRblNcUrhoGa"
url = "https://spark-api-open.xf-yun.com/v2/chat/completions"

# 业务系统 API 配置
BUSINESS_API_BASE = "http://localhost:9090"

# 1. 定义工具 (Function Definition)
# 注意：web_search 和 function 不能同时使用，需要根据场景选择

# Function 工具列表（用于业务 API 调用）
function_tools = [
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
    },
    {
        "type": "web_search",
        "web_search": {
            "enable": True,
            "search_mode": "deep"
        }
    },
    {
        "type": "web_search",
        "web_search": {
            "enable": True,
            "search_mode": "deep"
        }
    }
]

# Web Search 工具（用于网络搜索）
web_search_tools = [
    {
        "type": "web_search",
        "web_search": {
            "enable": True,
            "search_mode": "normal"  # 可选 "deep" 或 "normal"，deep 模式搜索内容更丰富但 token 使用量更高
        }
    }
]

# 默认使用 function 工具
tools = function_tools

# 2. 实现实际的 API 调用函数
def get_all_customers():
    """调用业务系统的获取所有客户接口"""
    try:
        response = requests.get(f"{BUSINESS_API_BASE}/api/customers", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API调用失败: {str(e)}"}

def get_all_orders():
    """调用业务系统的获取所有订单接口"""
    try:
        response = requests.get(f"{BUSINESS_API_BASE}/api/orders", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API调用失败: {str(e)}"}

def create_customer(name, phone, level, email=None, address=None):
    """调用业务系统的新增客户接口"""
    try:
        data = {
            "name": name,
            "phone": phone,
            "level": level
        }
        if email:
            data["email"] = email
        if address:
            data["address"] = address
        
        response = requests.post(f"{BUSINESS_API_BASE}/api/customers", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API调用失败: {str(e)}"}

def update_customer(id, name=None, phone=None, email=None, address=None, level=None):
    """调用业务系统的修改客户信息接口"""
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
        
        response = requests.put(f"{BUSINESS_API_BASE}/api/customers/{id}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API调用失败: {str(e)}"}

def create_order(orderNo, productId, productName, quantity, totalAmount, status, customerName, customerPhone):
    """调用业务系统的新增订单接口"""
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
        
        response = requests.post(f"{BUSINESS_API_BASE}/api/orders", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API调用失败: {str(e)}"}

def update_order(id, orderNo=None, productId=None, productName=None, quantity=None, totalAmount=None, status=None, customerName=None, customerPhone=None):
    """调用业务系统的修改订单信息接口"""
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
        
        response = requests.put(f"{BUSINESS_API_BASE}/api/orders/{id}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API调用失败: {str(e)}"}

# 3. 函数映射表
available_functions = {
    "get_all_customers": get_all_customers,
    "get_all_orders": get_all_orders,
    "create_customer": create_customer,
    "update_customer": update_customer,
    "create_order": create_order,
    "update_order": update_order
}

# 请求模型，并将结果输出
def get_answer(message, use_web_search=False):
    """
    请求模型并返回结果
    
    参数:
        message: 消息列表
        use_web_search: 是否使用网络搜索工具（默认 False，使用 function 工具）
    """
    #初始化请求体
    headers = {
        'Authorization':api_key,
        'content-type': "application/json"
    }
    
    # 根据参数选择工具类型
    selected_tools = web_search_tools if use_web_search else function_tools
    
    body = {
        "model": "x1",
        "user": "user_id",
        "messages": message,
        # 下面是可选参数
        "stream": True,
        "tools": selected_tools
    }
    full_response = ""  # 存储返回结果
    tool_calls_dict = {}  # 使用字典存储工具调用信息，key为index
    isFirstContent = True  # 首帧标识

    response = requests.post(url=url,json= body,headers= headers,stream= True)
    # print(response)
    for chunks in response.iter_lines():
        # 打印返回的每帧内容
        # print(chunks)
        if (chunks and '[DONE]' not in str(chunks)):
            data_org = chunks[6:]

            chunk = json.loads(data_org)
            text = chunk['choices'][0]['delta']
            # 判断思维链状态并输出
            if ('reasoning_content' in text and '' != text['reasoning_content']):
                reasoning_content = text["reasoning_content"]
                print(reasoning_content, end="")
            # 判断最终结果状态并输出
            if ('content' in text and '' != text['content']):
                content = text["content"]
                if (True == isFirstContent):
                    print("\n*******************以上为思维链内容，模型回复内容如下********************\n")
                    isFirstContent = False
                print(content, end="")
                full_response += content
            # 检查是否有工具调用（流式返回需要合并）
            if ('tool_calls' in text and text['tool_calls']):
                for tool_call_chunk in text['tool_calls']:
                    index = tool_call_chunk.get('index', 0)
                    
                    if index not in tool_calls_dict:
                        # 初始化新的 tool_call
                        tool_calls_dict[index] = {
                            'id': tool_call_chunk.get('id', ''),
                            'type': tool_call_chunk.get('type', 'function'),
                            'function': {
                                'name': tool_call_chunk.get('function', {}).get('name', ''),
                                'arguments': ''
                            }
                        }
                    
                    # 合并 id（如果有）
                    if 'id' in tool_call_chunk and tool_call_chunk['id']:
                        tool_calls_dict[index]['id'] = tool_call_chunk['id']
                    
                    # 合并 function name（如果有）
                    if 'function' in tool_call_chunk:
                        if 'name' in tool_call_chunk['function'] and tool_call_chunk['function']['name']:
                            tool_calls_dict[index]['function']['name'] = tool_call_chunk['function']['name']
                        
                        # 累积 arguments
                        if 'arguments' in tool_call_chunk['function']:
                            tool_calls_dict[index]['function']['arguments'] += tool_call_chunk['function']['arguments']
    
    # 将字典转换为列表
    tool_calls = list(tool_calls_dict.values())
    
    return full_response, tool_calls


# 管理对话历史，按序编为列表
def getText(text,role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

# 获取对话中的所有角色的content长度
def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

# 判断长度是否超长，当前限制8K tokens
def checklen(text):
    while (getlength(text) > 11000):
        del text[0]
    return text


#主程序入口
if __name__ =='__main__':

    #对话历史存储列表
    chatHistory = []
    #循环对话轮次
    while (1):
        try:
            # 等待控制台输入
            Input = input("\n" + "我:")
            if not Input:
                break
            
            # 检测是否需要使用网络搜索
            use_web_search = False
            if any(keyword in Input.lower() for keyword in ['搜索', 'search', '查询时间', '查询天气', '最新', '新闻']):
                use_web_search = True
                print("[使用网络搜索模式]")
            
            question = checklen(getText(chatHistory,"user", Input))
            
            # 开始输出模型内容
            print("星火:", end="")
            answer, tool_calls = get_answer(question, use_web_search=use_web_search)
            print() # 换行
            
            # 循环处理工具调用，直到模型不再需要调用工具
            max_iterations = 5  # 防止无限循环
            iteration = 0
            
            while tool_calls and iteration < max_iterations:
                iteration += 1
                
                # 过滤掉无效的工具调用（函数名为空或不存在）
                valid_tool_calls = [
                    tc for tc in tool_calls 
                    if tc.get("function", {}).get("name") and tc.get("function", {}).get("name") in available_functions
                ]
                
                if not valid_tool_calls:
                    print("\n[警告: 检测到无效的工具调用，跳过]")
                    break
                
                print(f"\n[第{iteration}轮工具调用，检测到 {len(valid_tool_calls)} 个有效工具请求]")
                
                # 将助手的回复添加到历史（包含 tool_calls）
                assistant_message = {"role": "assistant", "content": answer}
                if tool_calls:
                    assistant_message["tool_calls"] = tool_calls
                chatHistory.append(assistant_message)
                
                # 执行每个工具调用
                for tool_call in valid_tool_calls:
                    function_name = tool_call["function"]["name"]
                    function_args_str = tool_call["function"].get("arguments", "{}")
                    
                    print(f"[调用函数: {function_name}]")
                    print(f"[参数: {function_args_str}]")
                    
                    try:
                        function_args = json.loads(function_args_str) if function_args_str else {}
                    except json.JSONDecodeError as e:
                        print(f"[错误: 参数解析失败 - {e}]")
                        continue
                    
                    # 执行函数
                    try:
                        function_to_call = available_functions[function_name]
                        function_response = function_to_call(**function_args)
                        
                        # 将函数执行结果添加到对话历史
                        tool_message = {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": json.dumps(function_response, ensure_ascii=False)
                        }
                        chatHistory.append(tool_message)
                        print(f"[函数执行完成]")
                    except TypeError as e:
                        error_msg = f"参数错误: {str(e)}"
                        print(f"[错误: {error_msg}]")
                        # 将错误信息返回给模型
                        tool_message = {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": json.dumps({"error": error_msg}, ensure_ascii=False)
                        }
                        chatHistory.append(tool_message)
                    except Exception as e:
                        error_msg = f"执行失败: {str(e)}"
                        print(f"[错误: {error_msg}]")
                        tool_message = {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": json.dumps({"error": error_msg}, ensure_ascii=False)
                        }
                        chatHistory.append(tool_message)
                
                # 再次调用模型，让它根据函数结果生成回复或继续调用工具
                print("\n星火:", end="")
                answer, tool_calls = get_answer(chatHistory, use_web_search=use_web_search)
                print() # 换行
            
            # 所有工具调用完成后，添加最终回复到历史
            if answer:
                getText(chatHistory,"assistant", answer)
            
            if iteration >= max_iterations:
                print("\n[警告: 达到最大工具调用次数限制]")
                
        except KeyboardInterrupt:
            break


