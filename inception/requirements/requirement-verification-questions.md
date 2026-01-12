# Requirements Verification Questions

## AWSomeShop - 员工福利电商网站

请回答以下问题，帮助我更好地理解项目需求。在每个问题的 [Answer]: 后填写您选择的字母选项。

---

## 技术架构相关

### Question 1
您希望使用什么技术栈来构建这个应用？

A) 全栈 JavaScript (React + Node.js + Express)
B) Python 后端 (FastAPI/Django) + React 前端
C) Java 后端 (Spring Boot) + React 前端
D) 纯前端 SPA + AWS 无服务器后端 (Lambda + API Gateway)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 2
您希望使用什么数据库？

A) 关系型数据库 (PostgreSQL/MySQL)
B) NoSQL 文档数据库 (DynamoDB/MongoDB)
C) 内存数据库 (Redis) 配合关系型数据库
D) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 3
应用的部署目标是什么？

A) AWS 云服务 (EC2/ECS/Lambda)
B) 本地服务器/私有云
C) 容器化部署 (Docker/Kubernetes)
D) 暂不考虑，先完成本地开发
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## 用户与认证相关

### Question 4
员工如何登录系统？

A) 用户名和密码
B) 企业 SSO 单点登录 (如 SAML/OIDC)
C) 邮箱验证码登录
D) 暂时使用简单的用户名密码，后续再集成 SSO
E) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 5
预计有多少员工会使用这个系统？

A) 小规模 (< 100 人)
B) 中等规模 (100-500 人)
C) 大规模 (500-2000 人)
D) 超大规模 (> 2000 人)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 6
管理员角色是否需要细分权限？

A) 不需要，所有管理员权限相同
B) 需要，区分超级管理员和普通管理员
C) 需要，按功能模块分配权限（产品管理、积分管理等）
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## 积分系统相关

### Question 7
员工的初始积分如何获得？

A) 管理员手动发放
B) 系统按规则自动发放（如每月固定额度）
C) 两者都支持
D) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 8
积分是否有有效期？

A) 没有有效期，永久有效
B) 有有效期，过期自动清零
C) 有有效期，但可以延期
D) MVP 阶段暂不考虑有效期
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 9
积分兑换是否需要审批流程？

A) 不需要，员工直接兑换
B) 需要，管理员审批后才能兑换
C) 根据产品价值决定（高价值需审批）
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## 产品管理相关

### Question 10
产品是否有库存限制？

A) 有库存限制，库存为0时不能兑换
B) 没有库存限制，可以无限兑换
C) MVP 阶段暂不考虑库存
D) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 11
产品是否需要分类管理？

A) 需要，支持多级分类
B) 需要，但只支持一级分类
C) 不需要，所有产品平铺展示
D) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 12
产品图片如何存储？

A) 存储在本地文件系统
B) 使用云存储服务 (如 AWS S3)
C) 使用外部图片链接
D) MVP 阶段使用占位图，暂不处理图片上传
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## 兑换与订单相关

### Question 13
兑换后是否需要物流配送？

A) 需要，员工填写收货地址
B) 不需要，员工到指定地点自取
C) 根据产品类型决定（实物配送，虚拟产品直接发放）
D) MVP 阶段暂不考虑物流
E) Other (please describe after [Answer]: tag below)

[Answer]: E 全部都用虚拟产品

### Question 14
是否需要兑换记录导出功能？

A) 需要，支持导出 Excel/CSV
B) 不需要，只在系统内查看
C) MVP 阶段暂不需要
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## 非功能性需求

### Question 15
系统的可用性要求是什么？

A) 高可用 (99.9%+)，需要多区域部署
B) 标准可用 (99%+)，单区域部署即可
C) MVP 阶段不做高可用要求
D) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 16
是否需要支持移动端访问？

A) 需要，开发原生移动应用
B) 需要，但使用响应式 Web 设计即可
C) 暂不需要，只支持桌面端
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

请在每个问题的 [Answer]: 后填写您的选择，完成后告诉我。
