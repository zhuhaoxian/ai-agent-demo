# 快速设置指南

## 首次使用步骤

### 1. 克隆项目后的配置

```bash
# 1. 复制配置模板
cp config.example.py config.py

# 2. 编辑 config.py，填入你的真实配置
# 使用你喜欢的编辑器打开 config.py
```

### 2. 配置说明

打开 `config.py`，需要修改以下配置：

#### AI 模型配置

根据你使用的服务选择对应配置：

**选项 A：使用 OpenAI**
```python
AI_API_KEY = "sk-your-openai-api-key"
AI_BASE_URL = "https://api.openai.com/v1"
AI_MODEL = "gpt-4"
```

**选项 B：使用星火**
```python
AI_API_KEY = "AK:SK"  # 格式：AccessKey:SecretKey
AI_BASE_URL = "https://spark-api-open.xf-yun.com/v2"
AI_MODEL = "x1"
```

**选项 C：使用 ChatAnywhere**
```python
AI_API_KEY = "sk-your-chatanywhere-key"
AI_BASE_URL = "https://api.chatanywhere.tech/v1"
AI_MODEL = "gpt-3.5-turbo"
```

#### AgentGuard 配置

```python
AGENTGUARD_PROXY_URL = "http://localhost:8080/proxy/v1/request"
AGENTGUARD_API_KEY = "ag_your_agentguard_key_here"  # 从 AgentGuard 平台获取
```

#### 业务系统配置

```python
BUSINESS_API_BASE = "http://localhost:9090"  # 你的业务系统地址
```

### 3. 安装依赖

```bash
pip install openai requests
```

### 4. 运行程序

```bash
python main.py
```

## 安全提示

⚠️ **重要**：
- `config.py` 已添加到 `.gitignore`，不会被提交到 Git
- 不要将真实的 API Key 分享给他人
- 不要将 `config.py` 提交到公开仓库
- 如果不小心泄露了 Key，请立即在对应平台重新生成

## 文件说明

- `config.example.py` - 配置模板（可以提交到 Git）
- `config.py` - 实际配置文件（包含真实 Key，不提交到 Git）
- `.gitignore` - Git 忽略规则（已配置忽略 config.py 和 docs/）

## 团队协作

如果你是团队成员：
1. 克隆项目后，复制 `config.example.py` 为 `config.py`
2. 向团队管理员索取 API Key
3. 填入配置后即可使用
4. 不要修改 `config.example.py`（除非添加新的配置项）
