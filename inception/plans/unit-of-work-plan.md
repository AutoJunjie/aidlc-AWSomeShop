# Unit of Work Plan - AWSomeShop

## Overview
本计划定义如何将 AWSomeShop 系统分解为可管理的工作单元。

---

## Part 1: Planning Questions

请回答以下问题，在每个 [Answer]: 后填写您选择的字母选项。

### Question 1
系统应该如何分解为工作单元？

A) 单体应用 - 一个工作单元包含前后端所有功能
B) 前后端分离 - 两个工作单元（后端 API + 前端 UI）
C) 微服务架构 - 多个独立服务（Auth Service, Product Service, Points Service, Redemption Service）
D) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 2
您选择了微服务架构。前端如何组织？

A) 单一前端应用，调用所有后端微服务
B) 前端也按微服务拆分（微前端架构）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 3
微服务的粒度如何确定？

A) 按应用设计的模块拆分（Auth, Products, Points, Redemptions 各一个服务）
B) 更粗粒度 - 合并相关服务（如 Points + Redemptions 合并）
C) 更细粒度 - 进一步拆分服务
D) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 4
用户故事如何分配到工作单元？

A) 按功能模块分配（认证、产品、积分、兑换）
B) 按用户角色分配（员工功能、管理员功能）
C) 所有故事在一个单元中实现
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Part 2: Execution Checklist

完成问题回答后，将按以下步骤生成工作单元：

### Step 1: Define Units of Work
- [x] 定义每个工作单元的名称和职责
- [x] 确定单元边界
- [x] 定义单元接口

### Step 2: Map Components to Units
- [x] 将应用设计中的组件分配到工作单元
- [x] 确保每个组件只属于一个单元
- [x] 验证组件分配合理性

### Step 3: Map Stories to Units
- [x] 将用户故事分配到工作单元
- [x] 确保每个故事有明确的单元归属
- [x] 验证故事覆盖完整性

### Step 4: Define Unit Dependencies
- [x] 创建单元依赖关系矩阵
- [x] 定义单元间通信方式
- [x] 识别共享依赖

### Step 5: Document Code Organization (Greenfield)
- [x] 定义项目目录结构
- [x] 确定代码组织策略
- [x] 记录构建和部署配置

### Step 6: Validate Units
- [x] 验证单元职责清晰
- [x] 检查依赖关系合理
- [x] 确认故事分配完整

### Step 7: Save Artifacts
- [x] 保存 unit-of-work.md
- [x] 保存 unit-of-work-dependency.md
- [x] 保存 unit-of-work-story-map.md

---

请在 Part 1 的每个问题后填写您的选择，完成后告诉我。
