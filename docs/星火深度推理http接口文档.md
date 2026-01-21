# 星火深度推理http接口文档

**文档更新时间：2025.11.03**

**公告说明： 星火深度推理模型X1已升级至X1.5 （正式版本）**，X1的历史用户请求将默认指向该版本
**X1.5能力介绍**：（1）新增**动态调整思考模式**，通过thinking 字段控制；（2）上下文长度增大：输入、输出各64K；（3）支持FunctionCall功能；

## [#](https://www.xfyun.cn/doc/spark/X1http.html#_1、请求地址)1、请求地址

**可领取授权体验，[立即领取>>](https://xinghuo.xfyun.cn/sparkapi?scr=price)**

**使用HTTP方式调用推理模型的请求地址:**

```text
X1.5版本： https://spark-api-open.xf-yun.com/v2/chat/completions     对应model为：spark-x
```

**兼容openAI SDK:**

```text
X1.5版本  base_url 需要配置为:https://spark-api-open.xf-yun.com/v2/    对应model为：spark-x
```

## [#](https://www.xfyun.cn/doc/spark/X1http.html#_2、请求示例)2、请求示例

### [#](https://www.xfyun.cn/doc/spark/X1http.html#_2-1-示例demo)2.1 示例demo

[**请求示例：兼容openAI SDK**](https://openres.xfyun.cn/xfyundoc/2025-04-20/a63e0abb-da71-400c-89f8-8ebec597415a/1745132930302/X1_SDK.zip)

[**请求示例：Python demo**](https://openres.xfyun.cn/xfyundoc/2025-04-18/3586457d-cf15-4e5f-8428-8e0d54d2dd2a/1744959701998/X1_http.zip)

[**请求示例：Java demo**](https://openres.xfyun.cn/xfyundoc/2025-04-17/687d0eb2-1c48-449f-8f4f-54b3d1ec8bfa/1744894181198/X1_http_java.zip)

**兼容openAI SDK，请求示例**

**鉴权说明：** 鉴权使用http协议的APIpassword在[**控制台** ](https://console.xfyun.cn/services/bmx1)获取

```json
import os
from openai import OpenAI
import openai


client = OpenAI(
    
    api_key="AK:SK", # 两种方式：1、http协议的APIpassword； 2、ws协议的apikey和apisecret 按照ak:sk格式拼接；
    base_url="https://spark-api-open.xf-yun.com/v2",
)

# stream_res = True
stream_res = False


stream = client.chat.completions.create(
    messages=[
          {
            "role": "user",
            "content": "你好"
        },

    ],

    model="spark-x",
    stream=stream_res,
    user="123456",

)
full_response = ""

if not stream_res:
    print(stream.to_json())
else:
    for chunk in stream:
        if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content is not None:
            reasoning_content = chunk.choices[0].delta.reasoning_content
            print(reasoning_content, end="", flush=True)  # 实时打印思考模型输出的思考过程每个片段
        
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)  # 实时打印每个片段
            full_response += content
    
    print("\n\n ------完整响应：", full_response)   
```

### [#](https://www.xfyun.cn/doc/spark/X1http.html#_2-2请求说明)2.2请求说明

**请求头**

```json
    {
        "Authorization" :"Bearer XXXXXXXXXXXXXX",  // 请替换XXXXXXXXXX为您的 APIpassword, 获取地址：https://console.xfyun.cn/services/bmx1
        "content-type"  : "application/json"
    }
```

**请求体**

```json
{
    "model": "spark-x",
    "user": "user_id",
    "messages": [
        {
            "role": "user",
            "content": "推荐两个国内适合自驾的景点"
        }
    ],
    // 下面是可选参数
    "stream": true,
    "tools": [
        {
            "type": "web_search",
            "web_search": {
                "enable": true,
                "search_mode":"deep"
            }
        },
        // {
        //     "type": "function",
        //     "function": {
        //         "name": "get_current_weather",
        //         "description": "当你想查询指定城市的天气时非常有用。",
        //         "parameters": {
        //             "type": "object",
        //             "properties": {
        //                 "location": {
        //                     "type": "string",
        //                     "description": "城市或县区，比如北京市、杭州市、余杭区等。"
        //                 }
        //             },
        //             "required": [
        //                 "location"
        //             ]
        //         }
        //     }
        // }
    ]
}
```

### 2.3请求参数

| 名称                                   | 类型             | 是否必传 | 描述                                                         | 传参示例                                                     |
| -------------------------------------- | ---------------- | -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| model                                  | string           | 是       | 取值范围： spark-x (模型已升级至X1.5，x1传参同样指向X1.5模型) | spark-x                                                      |
| user                                   | string           | 否       | 用户的唯一id，表示一个用户，user_123456                      |                                                              |
| messages                               | array            | 是       | 输入数组                                                     |                                                              |
| messages.role                          | string           | 是       | 对话角色：user：表示用户 assistant：表示大模型 tool：工具结果的回传时使用 |                                                              |
| messages.content                       | string           | 是       | 角色对应的文本内容                                           |                                                              |
| temperature                            | float            | 否       | 核采样阈值 取值范围（0, 2] 默认值1.2                         |                                                              |
| top_p                                  | int              | 否       | 生成过程中核采样方法概率阈值，例如，取值为0.8时，仅保留概率加起来大于等于0.8的最可能token的最小集合作为候选集。取值越大，生成的随机性越高；取值越低，生成的确定性越高。 取值范围(0, 1] 默认值0.95 |                                                              |
| top_k                                  | int              | 否       | 从k个中随机选择一个(非等概率) 取值范围[1, 6] 默认值6         |                                                              |
| presence_penalty                       | float            | 否       | 重复词的惩罚值 取值范围[0,3] 默认2.01                        |                                                              |
| frequency_penalty                      | float            | 否       | 频率惩罚值 取值范围[0,1] 默认0.001                           |                                                              |
| stream                                 | bool             | 否       | 是否流式返回结果。默认是false 表示非流式。 如果使用流式，服务端使用SSE的方式推送结果，客户端自己适配处理结果。 |                                                              |
| keep_alive                             | bool             | 否       | 是否开启非流式请求保活。默认是false 表示不开启。 如果开启，服务端会定时发送空行，直至所有结果返回。需要客户端自己处理空行。 |                                                              |
| max_tokens                             | int              | 否       | 大模型输出信息的token上限: X1.5取值范围[1,65535] 默认值65535 |                                                              |
| tool_choice                            | string or object | 否       | 5种模式(前3种是string,后两种是object)： auto：默认该值，模型自主决策是否调用工具； none：不允许模型调用工具； required：要求调用一个至多个工具 force模式：控制模型强制调用某个工具 allowed_tools模式：控制模型可以调用的工具范围 | 示例： force模式: "tool_choice": {"type": "function", "name": "get_current_weather"} allowed_tools模式： "tool_choice": {"type":"allowed_tools","mode":"auto","tools":[{"type":"function","name":"get_weather"},{"type":"function","name":"search_docs"}]} |
| **tools**                              | array            | 否       | 模型可能会调用的 tool 的列表                                 |                                                              |
| **tools.type**                         | string           | 否       | **web_search和function 不可同时传** 取值范围： web_search ：控制搜索开关以及搜索模式 function：用于FunctionCall方法注册 |                                                              |
| **tools.web_search**                   | object           | 否       | enable 开关表示是否开启搜索功能 search_mode开启搜索时支持选择搜索模式deep or normal deep模式搜索内容更丰富 token使用量更高 默认为normal模式 | {"type":"web_search","web_search":{"enable":true,"search_mode":"deep/normal"}} |
| **tools.function**                     | object           | 否       | **FunctionCall功能：用于方法命中和变量抽取场景**             | 示例： `{"type":"function","function":{"name":"get_current_weather","description":"当你想查询指定城市的天气时非常有用。","parameters":{"type":"object","properties":{"location":{"type":"string","description":"城市或县区，比如北京市、杭州市、余杭区等。"}},"required":["location"]}}}` |
| **tools.function.name**                | string           | 否       | function工具名称                                             |                                                              |
| **tools.function.description**         | string           | 否       | function工具的功能描述，该描述影响模型的调用准确率           |                                                              |
| **tools.function.parameters**          | object           | 否       | function工具所需要的参数，参数名称自定义，比如上面示例中的‘location’ | {"location":{"type":"string","description":"城市或县区，比如北京市、杭州市、余杭区等。"}} |
| **tools.function.parameters.required** | array            | 否       | 必须要返回的字段                                             | "required":["location"]                                      |
| **thinking**                           | object           | 否       | **用于控制深度思考模式**                                     | http请求示例： "thinking": {"type":"enabled"}  兼容OpenAI SDK 示例: extra_body=`{"thinking": {"type":"enabled"}}` |
| **thinking.type**                      | string           | 否       | 默认为enabled(开启思考) 支持以下3种模式切换： enabled：强制开启深度思考能⼒ disabled：强制关闭深度思考能⼒ auto：模型⾃⾏判断是否进⾏深度思考 |                                                              |