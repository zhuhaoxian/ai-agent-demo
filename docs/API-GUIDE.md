# Business Project - 业务系统API

这是一个基于Spring Boot 3 + MyBatis-Plus + MySQL的业务系统，提供客户、产品和订单管理的RESTful API接口。

## 技术栈

- JDK: OpenJDK 21 (LTS)
- 框架: Spring Boot 3.2.1
- ORM: MyBatis-Plus 3.5.5
- 数据库: MySQL 8.0+
- 构建工具: Maven

## 快速开始

### 1. 数据库初始化

首先确保MySQL已安装并运行，然后执行数据库初始化：

**Windows用户：**
```bash
init-database.bat
```

**或手动执行：**
```bash
mysql -u root -p < database-init.sql
```

这将创建 `business_db` 数据库，并初始化以下表和测试数据：
- customer (客户表) - 5条测试数据
- product (产品表) - 10条测试数据
- orders (订单表) - 10条测试数据

### 2. 配置数据库连接

编辑 `src/main/resources/application.yml`，修改数据库连接信息：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/business_db
    username: root
    password: your_password
```

### 3. 启动项目

**Windows用户：**
```bash
start.bat
```

**或使用Maven：**
```bash
mvnw.cmd clean package -DskipTests
mvnw.cmd spring-boot:run
```

**或在IDE中：**
直接运行 `BusinessProjectApplication.java` 的main方法

项目将在 `http://localhost:9090` 启动。

## API接口文档

### 统一响应格式

所有接口均返回统一的JSON格式：

```json
{
  "code": 200,
  "message": "操作描述",
  "data": {}
}
```

**响应字段说明：**
- `code`: 状态码，200表示成功，404表示资源不存在
- `message`: 操作结果描述信息
- `data`: 返回的数据对象或数组

---

### 客户管理 API

#### 1. 获取所有客户

**接口地址：** `GET /api/customers`

**请求参数：** 无

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "name": "张三",
      "phone": "13800138001",
      "email": "zhangsan@example.com",
      "address": "北京市朝阳区",
      "level": "VIP",
      "createTime": "2024-01-15T10:30:00"
    }
  ]
}
```

**响应字段说明（Customer对象）：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 客户ID |
| name | String | 客户姓名 |
| phone | String | 联系电话 |
| email | String | 电子邮箱 |
| address | String | 联系地址 |
| level | String | 客户等级：VIP/GOLD/NORMAL |
| createTime | DateTime | 创建时间 |

---

#### 2. 根据ID获取客户

**接口地址：** `GET /api/customers/{id}`

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | Long | 是 | 客户ID |

**请求示例：** `GET /api/customers/1`

**响应示例（成功）：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "id": 1,
    "name": "张三",
    "phone": "13800138001",
    "email": "zhangsan@example.com",
    "address": "北京市朝阳区",
    "level": "VIP",
    "createTime": "2024-01-15T10:30:00"
  }
}
```

**响应示例（失败）：**
```json
{
  "code": 404,
  "message": "客户不存在"
}
```

---

#### 3. 根据等级获取客户

**接口地址：** `GET /api/customers/level/{level}`

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| level | String | 是 | 客户等级：VIP/GOLD/NORMAL |

**请求示例：** `GET /api/customers/level/VIP`

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "name": "张三",
      "phone": "13800138001",
      "email": "zhangsan@example.com",
      "address": "北京市朝阳区",
      "level": "VIP",
      "createTime": "2024-01-15T10:30:00"
    }
  ]
}
```

---

#### 4. 新增客户

**接口地址：** `POST /api/customers`

**请求头：**
```
Content-Type: application/json
```

**请求参数（JSON Body）：**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | String | 是 | 客户姓名 |
| phone | String | 是 | 联系电话 |
| email | String | 否 | 电子邮箱 |
| address | String | 否 | 联系地址 |
| level | String | 是 | 客户等级：VIP/GOLD/NORMAL |

**请求示例：**
```json
{
  "name": "李四",
  "phone": "13900139002",
  "email": "lisi@example.com",
  "address": "上海市浦东新区",
  "level": "GOLD"
}
```

**响应示例（成功）：**
```json
{
  "code": 200,
  "message": "客户创建成功",
  "data": {
    "id": 6,
    "name": "李四",
    "phone": "13900139002",
    "email": "lisi@example.com",
    "address": "上海市浦东新区",
    "level": "GOLD",
    "createTime": "2024-01-20T15:30:00"
  }
}
```

**响应示例（失败）：**
```json
{
  "code": 500,
  "message": "客户创建失败"
}
```

---

#### 5. 修改客户信息

**接口地址：** `PUT /api/customers/{id}`

**请求头：**
```
Content-Type: application/json
```

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | Long | 是 | 客户ID |

**请求参数（JSON Body）：**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | String | 否 | 客户姓名 |
| phone | String | 否 | 联系电话 |
| email | String | 否 | 电子邮箱 |
| address | String | 否 | 联系地址 |
| level | String | 否 | 客户等级：VIP/GOLD/NORMAL |

**请求示例：** `PUT /api/customers/1`
```json
{
  "name": "张三",
  "phone": "13800138001",
  "email": "zhangsan_new@example.com",
  "address": "北京市海淀区",
  "level": "VIP"
}
```

**响应示例（成功）：**
```json
{
  "code": 200,
  "message": "客户更新成功",
  "data": {
    "id": 1,
    "name": "张三",
    "phone": "13800138001",
    "email": "zhangsan_new@example.com",
    "address": "北京市海淀区",
    "level": "VIP",
    "createTime": "2024-01-15T10:30:00"
  }
}
```

**响应示例（失败）：**
```json
{
  "code": 500,
  "message": "客户更新失败"
}
```

---

### 产品管理 API

#### 1. 获取所有产品

**接口地址：** `GET /api/products`

**请求参数：** 无

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "category": "电子产品",
      "price": 7999.00,
      "stock": 50,
      "description": "最新款苹果手机",
      "createTime": "2024-01-10T09:00:00",
      "updateTime": "2024-01-15T14:30:00"
    }
  ]
}
```

**响应字段说明（Product对象）：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 产品ID |
| name | String | 产品名称 |
| category | String | 产品分类 |
| price | BigDecimal | 产品价格 |
| stock | Integer | 库存数量 |
| description | String | 产品描述 |
| createTime | DateTime | 创建时间 |
| updateTime | DateTime | 更新时间 |

---

#### 2. 根据ID获取产品

**接口地址：** `GET /api/products/{id}`

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | Long | 是 | 产品ID |

**请求示例：** `GET /api/products/1`

**响应示例（成功）：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "id": 1,
    "name": "iPhone 15 Pro",
    "category": "电子产品",
    "price": 7999.00,
    "stock": 50,
    "description": "最新款苹果手机",
    "createTime": "2024-01-10T09:00:00",
    "updateTime": "2024-01-15T14:30:00"
  }
}
```

**响应示例（失败）：**
```json
{
  "code": 404,
  "message": "产品不存在"
}
```

---

#### 3. 根据分类获取产品

**接口地址：** `GET /api/products/category/{category}`

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | String | 是 | 产品分类（如：电子产品、家居用品、图书等） |

**请求示例：** `GET /api/products/category/电子产品`

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "category": "电子产品",
      "price": 7999.00,
      "stock": 50,
      "description": "最新款苹果手机",
      "createTime": "2024-01-10T09:00:00",
      "updateTime": "2024-01-15T14:30:00"
    }
  ]
}
```

---

#### 4. 获取低库存产品

**接口地址：** `GET /api/products/low-stock`

**查询参数：**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| threshold | Integer | 否 | 10 | 库存阈值，返回库存小于等于该值的产品 |

**请求示例：** `GET /api/products/low-stock?threshold=20`

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 5,
      "name": "无线鼠标",
      "category": "电子产品",
      "price": 89.00,
      "stock": 15,
      "description": "罗技无线鼠标",
      "createTime": "2024-01-12T11:00:00",
      "updateTime": "2024-01-18T16:20:00"
    }
  ]
}
```

---

### 订单管理 API

#### 1. 获取所有订单

**接口地址：** `GET /api/orders`

**请求参数：** 无

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "orderNo": "ORD20240115001",
      "productId": 1,
      "productName": "iPhone 15 Pro",
      "quantity": 2,
      "totalAmount": 15998.00,
      "status": "COMPLETED",
      "customerName": "张三",
      "customerPhone": "13800138001",
      "createTime": "2024-01-15T14:30:00"
    }
  ]
}
```

**响应字段说明（Order对象）：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 订单ID |
| orderNo | String | 订单编号 |
| productId | Long | 产品ID |
| productName | String | 产品名称 |
| quantity | Integer | 购买数量 |
| totalAmount | BigDecimal | 订单总金额 |
| status | String | 订单状态：PENDING/PAID/SHIPPED/COMPLETED/CANCELLED |
| customerName | String | 客户姓名 |
| customerPhone | String | 客户电话 |
| createTime | DateTime | 创建时间 |

---

#### 2. 根据ID获取订单

**接口地址：** `GET /api/orders/{id}`

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | Long | 是 | 订单ID |

**请求示例：** `GET /api/orders/1`

**响应示例（成功）：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "id": 1,
    "orderNo": "ORD20240115001",
    "productId": 1,
    "productName": "iPhone 15 Pro",
    "quantity": 2,
    "totalAmount": 15998.00,
    "status": "COMPLETED",
    "customerName": "张三",
    "customerPhone": "13800138001",
    "createTime": "2024-01-15T14:30:00"
  }
}
```

**响应示例（失败）：**
```json
{
  "code": 404,
  "message": "订单不存在"
}
```

---

#### 3. 根据状态获取订单

**接口地址：** `GET /api/orders/status/{status}`

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | String | 是 | 订单状态：PENDING/PAID/SHIPPED/COMPLETED/CANCELLED |

**订单状态说明：**
- `PENDING`: 待支付
- `PAID`: 已支付
- `SHIPPED`: 已发货
- `COMPLETED`: 已完成
- `CANCELLED`: 已取消

**请求示例：** `GET /api/orders/status/COMPLETED`

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "orderNo": "ORD20240115001",
      "productId": 1,
      "productName": "iPhone 15 Pro",
      "quantity": 2,
      "totalAmount": 15998.00,
      "status": "COMPLETED",
      "customerName": "张三",
      "customerPhone": "13800138001",
      "createTime": "2024-01-15T14:30:00"
    }
  ]
}
```

---

#### 4. 根据客户名称搜索订单

**接口地址：** `GET /api/orders/customer`

**查询参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | String | 是 | 客户姓名（支持模糊查询） |

**请求示例：** `GET /api/orders/customer?name=张三`

**响应示例：**
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "orderNo": "ORD20240115001",
      "productId": 1,
      "productName": "iPhone 15 Pro",
      "quantity": 2,
      "totalAmount": 15998.00,
      "status": "COMPLETED",
      "customerName": "张三",
      "customerPhone": "13800138001",
      "createTime": "2024-01-15T14:30:00"
    }
  ]
}
```

---

#### 5. 新增订单

**接口地址：** `POST /api/orders`

**请求头：**
```
Content-Type: application/json
```

**请求参数（JSON Body）：**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderNo | String | 是 | 订单编号 |
| productId | Long | 是 | 产品ID |
| productName | String | 是 | 产品名称 |
| quantity | Integer | 是 | 购买数量 |
| totalAmount | BigDecimal | 是 | 订单总金额 |
| status | String | 是 | 订单状态：PENDING/PAID/SHIPPED/COMPLETED/CANCELLED |
| customerName | String | 是 | 客户姓名 |
| customerPhone | String | 是 | 客户电话 |

**请求示例：**
```json
{
  "orderNo": "ORD20240120001",
  "productId": 2,
  "productName": "MacBook Pro",
  "quantity": 1,
  "totalAmount": 12999.00,
  "status": "PENDING",
  "customerName": "王五",
  "customerPhone": "13700137003"
}
```

**响应示例（成功）：**
```json
{
  "code": 200,
  "message": "订单创建成功",
  "data": {
    "id": 11,
    "orderNo": "ORD20240120001",
    "productId": 2,
    "productName": "MacBook Pro",
    "quantity": 1,
    "totalAmount": 12999.00,
    "status": "PENDING",
    "customerName": "王五",
    "customerPhone": "13700137003",
    "createTime": "2024-01-20T16:00:00"
  }
}
```

**响应示例（失败）：**
```json
{
  "code": 500,
  "message": "订单创建失败"
}
```

---

#### 6. 修改订单信息

**接口地址：** `PUT /api/orders/{id}`

**请求头：**
```
Content-Type: application/json
```

**路径参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | Long | 是 | 订单ID |

**请求参数（JSON Body）：**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderNo | String | 否 | 订单编号 |
| productId | Long | 否 | 产品ID |
| productName | String | 否 | 产品名称 |
| quantity | Integer | 否 | 购买数量 |
| totalAmount | BigDecimal | 否 | 订单总金额 |
| status | String | 否 | 订单状态：PENDING/PAID/SHIPPED/COMPLETED/CANCELLED |
| customerName | String | 否 | 客户姓名 |
| customerPhone | String | 否 | 客户电话 |

**请求示例：** `PUT /api/orders/1`
```json
{
  "status": "SHIPPED",
  "quantity": 3,
  "totalAmount": 23997.00
}
```

**响应示例（成功）：**
```json
{
  "code": 200,
  "message": "订单更新成功",
  "data": {
    "id": 1,
    "orderNo": "ORD20240115001",
    "productId": 1,
    "productName": "iPhone 15 Pro",
    "quantity": 3,
    "totalAmount": 23997.00,
    "status": "SHIPPED",
    "customerName": "张三",
    "customerPhone": "13800138001",
    "createTime": "2024-01-15T14:30:00"
  }
}
```

**响应示例（失败）：**
```json
{
  "code": 500,
  "message": "订单更新失败"
}
```

## 测试API

使用curl测试接口：

**查询接口：**
```bash
# 获取所有产品
curl http://localhost:8080/api/products

# 获取电子产品
curl http://localhost:8080/api/products/category/电子产品

# 获取VIP客户
curl http://localhost:8080/api/customers/level/VIP

# 获取已完成的订单
curl http://localhost:8080/api/orders/status/COMPLETED
```

**新增接口：**
```bash
# 新增客户
curl -X POST http://localhost:8080/api/customers \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"李四\",\"phone\":\"13900139002\",\"email\":\"lisi@example.com\",\"address\":\"上海市浦东新区\",\"level\":\"GOLD\"}"

# 新增订单
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d "{\"orderNo\":\"ORD20240120001\",\"productId\":2,\"productName\":\"MacBook Pro\",\"quantity\":1,\"totalAmount\":12999.00,\"status\":\"PENDING\",\"customerName\":\"王五\",\"customerPhone\":\"13700137003\"}"
```

**修改接口：**
```bash
# 修改客户信息
curl -X PUT http://localhost:8080/api/customers/1 \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"张三\",\"phone\":\"13800138001\",\"email\":\"zhangsan_new@example.com\",\"address\":\"北京市海淀区\",\"level\":\"VIP\"}"

# 修改订单状态
curl -X PUT http://localhost:8080/api/orders/1 \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"SHIPPED\"}"
```
