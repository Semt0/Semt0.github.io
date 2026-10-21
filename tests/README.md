# 回归测试

```bash
uv run python -m unittest discover -s tests -p 'test_*.py'
node --experimental-vm-modules --test tests/*.test.mjs
```

- `test_site.py`：YAML 元数据、确定性排序、URL/HTML 转义、生成区块、导航分组和生成文件一致性。
- `waline.test.mjs`：本地资源校验、异步下载期间切页、禁用评论、实例清理、评论迁移和失败重试。使用模拟模块，不向线上发布测试评论。
- 构建后运行 `uv run python scripts/check_site.py` 检查实际 HTML。

测试不依赖被忽略的 `.trae` / `.claude` 文件，也不要求连接评论服务。
