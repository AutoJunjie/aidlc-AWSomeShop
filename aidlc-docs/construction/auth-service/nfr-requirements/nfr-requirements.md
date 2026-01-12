# Auth Service - NFR Requirements

## Performance Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| PERF-1 | API 响应时间 | < 500ms (P95) |
| PERF-2 | 登录接口响应 | < 500ms (含 bcrypt) |
| PERF-3 | Token 验证响应 | < 100ms |
| PERF-4 | 并发用户支持 | 100-500 |

---

## Scalability Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| SCALE-1 | 水平扩展 | 支持多实例部署 |
| SCALE-2 | 无状态设计 | JWT 无需服务端会话存储 |
| SCALE-3 | 数据库连接池 | 每实例 10-20 连接 |

---

## Availability Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| AVAIL-1 | 服务可用性 | 99%+ |
| AVAIL-2 | 部署模式 | 单区域 |
| AVAIL-3 | 健康检查 | /health 端点 |

---

## Security Requirements

| ID | Requirement | Implementation |
|----|-------------|----------------|
| SEC-1 | 密码加密 | bcrypt, cost=12 |
| SEC-2 | Token 签名 | HS256 + 密钥 |
| SEC-3 | HTTPS | 生产环境强制 |
| SEC-4 | 敏感数据 | 不在日志中记录密码 |

---

## Logging Requirements

| ID | Requirement | Detail |
|----|-------------|--------|
| LOG-1 | 登录事件 | 记录所有登录尝试（成功/失败） |
| LOG-2 | 日志内容 | timestamp, username, IP, result |
| LOG-3 | 敏感数据 | 不记录密码和 token |

---

## Rate Limiting

| ID | Requirement | Target |
|----|-------------|--------|
| RATE-1 | 登录限制 | MVP 阶段不实现 |
