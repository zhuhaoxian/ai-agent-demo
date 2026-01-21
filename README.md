# 星火 AI 对话系统

支持 Function Call 和 Web Search 功能的智能对话系统。

## 项目结构

```
.
├── main.py              # 主程序入口
├── config.py            # 配置文件（API 密钥等）
├── spark_client.py      # 星火 API 客户端
├── chat_manager.py      # 对话历史管理
├── business_api.py      # 业务系统 API 调用
├── tools_config.py      # 工具定义配置
├── X1_http.py          # 原始版本（已废弃）
└── README.md           # 项目说明
```

## 模块说明

### main.py
主程序入口，包含 `ChatBot` 类和主循环逻辑。

### config.py
集中管理所有配置项：
- 星火 API 配置（密钥、URL、模型）
- 业务系统 API 配置
- 对话参数配置

### spark_client.py
封装与星火 API 的交互：
- `SparkClient` 类：处理 API 请求和响应
- 支持流式返回
- 自动合并工具调用信息

### chat_manager.py
管理对话历史：
- `ChatManager` 类：维护对话上下文
- 自动裁剪过长的历史记录
- 支持添加各种角色的消息

### business_api.py
业务系统 API 调用封装：
- 客户管理：查询、新增、修改
- 订单管理：查询、新增、修改
- 统一的错误处理
- 函数映射表 `AVAILABLE_FUNCTIONS`

### tools_config.py
工具定义配置：
- `FUNCTION_TOOLS`：Function Call 工具列表
- `WEB_SEARCH_TOOLS`：Web Search 工具配置
- `WEB_SEARCH_KEYWORDS`：触发网络搜索的关键词

## 使用方法

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API 密钥

编辑 `config.py`，设置你的星火 API 密钥：

```python
SPARK_API_KEY = "Bearer YOUR_API_KEY"
```

### 3. 运行程序

```bash
python main.py
```

### 4. 使用示例

**业务查询（自动使用 Function Call）：**
```
我: 查询所有客户
```

**网络搜索（自动使用 Web Search）：**
```
我: 查询今天的天气
我: 搜索最新新闻
```

## 功能特性

### 智能工具选择
- 自动检测用户输入，选择合适的工具类型
- 关键词触发：包含"搜索"、"查询时间"、"最新"等词时使用网络搜索
- 其他情况使用 Function Call 调用业务 API

### Function Call
- 支持多轮工具调用
- 自动执行业务 API 函数
- 完善的错误处理

### Web Search
- 支持深度搜索模式（deep）
- 获取实时信息

### 对话管理
- 自动维护对话上下文
- 智能裁剪过长历史
- 支持多轮对话

## 注意事项

1. **工具互斥**：Web Search 和 Function Call 不能同时使用（星火 API 限制）
2. **业务系统**：需要确保业务系统 API（http://localhost:9090）正常运行
3. **API 密钥**：请妥善保管你的 API 密钥，不要提交到版本控制系统

## 配置说明

### 修改业务系统地址

编辑 `config.py`：

```python
BUSINESS_API_BASE = "http://your-api-server:port"
```

### 调整对话历史长度

编辑 `config.py`：

```python
MAX_CHAT_HISTORY_LENGTH = 11000  # 字符数
```

### 修改工具调用次数限制

编辑 `config.py`：

```python
MAX_TOOL_ITERATIONS = 5  # 最大轮次
```

### 添加网络搜索关键词

编辑 `tools_config.py`：

```python
WEB_SEARCH_KEYWORDS = ['搜索', 'search', '查询时间', '最新', '新闻', '你的关键词']
```

## 扩展开发

### 添加新的业务 API

1. 在 `business_api.py` 中添加函数实现
2. 在 `tools_config.py` 的 `FUNCTION_TOOLS` 中添加工具定义
3. 在 `business_api.py` 的 `AVAILABLE_FUNCTIONS` 中注册函数

### 修改 Web Search 模式

编辑 `tools_config.py`：

```python
WEB_SEARCH_TOOLS = [
    {
        "type": "web_search",
        "web_search": {
            "enable": True,
            "search_mode": "normal"  # 改为 "normal" 节省 token
        }
    }
]
```

## 版本历史

- v2.0: 重构版本，模块化设计
- v1.0: 原始版本（X1_http.py）
