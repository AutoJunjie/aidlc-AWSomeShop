# Auth Service - NFR Requirements

## Performance

| ID | Requirement | Target |
|----|-------------|--------|
| PERF-1 | Login API 响应时间 | < 500ms (P95) |
| PERF-2 | Token 验证响应时间 | < 100ms (P95) |
| PERF-3 | 并发登录支持 | 100 req/s |

## Security

| ID | Requirement |
|----|-------------|
| SEC-1 | 密码使用 bcrypt 加密，salt rounds >= 12 |
| SEC-2 | JWT secret 从环境变量读取，禁止硬编码 |
| SEC-3 | 登录失败不暴露用户是否存在 |
| SEC-4 | API 强制 HTTPS（生产环境） |
| SEC-5 | 防止暴力破解：5次失败后锁定5分钟（P1，MVP可选） |

## Reliability

| ID | Requirement |
|----|-------------|
| REL-1 | 服务可用性 99%+ |
| REL-2 | 数据库连接池管理，自动重连 |
| REL-3 | 健康检查端点 /health |

## Scalability

| ID | Requirement |
|----|-------------|
| SCA-1 | 无状态设计，支持水平扩展 |
| SCA-2 | 支持 100-500 并发用户 |

## Observability

| ID | Requirement |
|----|-------------|
| OBS-1 | 结构化日志（JSON 格式） |
| OBS-2 | 记录所有登录尝试（成功/失败） |
| OBS-3 | 暴露 Prometheus metrics（P1） |
