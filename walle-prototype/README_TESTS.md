# WALL-E 测试文档

## 测试文件说明

本项目包含以下测试文件,用于验证示例代码的正确性:

### 1. test_mcp_client.py
测试 MCP 客户端核心功能:
- MCPClient 初始化
- 服务器注册(成功、失败、导入错误)
- 工具列表获取
- 工具调用(成功、失败、异常处理)
- 工具信息查询
- create_mcp_client 工厂函数

**覆盖率**: 13 个测试用例

### 2. test_mcp_servers.py
测试三个 MCP 服务器:
- Navigation Server: 导航和位置搜索功能
- Weather Server: 天气查询和对比功能
- Music Server: 音乐播放和歌单搜索功能

**覆盖率**: 23 个测试用例

### 3. test_voice_nav.py
测试语音导航原型功能:
- 语音监听(成功、超时、识别失败)
- AI 意图理解(导航、未知指令、异常)
- 导航功能
- 主程序流程

**覆盖率**: 9 个测试用例

### 4. test_demo_mcp.py
测试 MCP 演示脚本:
- MCP 客户端创建
- 工具列表去重
- 各类工具调用(导航、天气、音乐)
- AI 集成功能
- 错误处理

**覆盖率**: 10 个测试用例

## 运行测试

### 运行所有测试
```bash
cd walle-prototype
python3 -m unittest discover -p "test_*.py" -v
```

### 运行单个测试文件
```bash
cd walle-prototype
python3 -m unittest test_mcp_client.py -v
python3 -m unittest test_mcp_servers.py -v
python3 -m unittest test_voice_nav.py -v
python3 -m unittest test_demo_mcp.py -v
```

### 运行特定测试类
```bash
python3 -m unittest test_mcp_client.TestMCPClient -v
```

### 运行特定测试用例
```bash
python3 -m unittest test_mcp_client.TestMCPClient.test_init -v
```

## 测试依赖

测试使用 Python 标准库的 `unittest` 模块,无需额外安装依赖。主要使用:
- `unittest.mock`: 模拟对象和函数调用
- `patch`: 替换导入的模块和函数
- `Mock/MagicMock`: 创建模拟对象

## 测试覆盖范围

| 模块 | 测试文件 | 用例数 | 覆盖功能 |
|------|---------|--------|----------|
| mcp_client.py | test_mcp_client.py | 13 | 客户端管理、工具注册和调用 |
| navigation_server.py | test_mcp_servers.py | 8 | 导航和位置搜索 |
| weather_server.py | test_mcp_servers.py | 5 | 天气查询 |
| music_server.py | test_mcp_servers.py | 10 | 音乐控制 |
| voice_nav.py | test_voice_nav.py | 9 | 语音识别和导航 |
| demo_mcp.py | test_demo_mcp.py | 10 | MCP 功能演示 |

**总计**: 55 个测试用例

## 注意事项

1. **Mock 使用**: 所有外部依赖(如 `webbrowser.open`, OpenAI API, 语音识别)都使用 mock 对象,避免实际调用
2. **环境变量**: 测试中使用 `@patch.dict('os.environ', ...)` 模拟环境变量
3. **异常处理**: 测试覆盖了正常流程和异常情况
4. **独立性**: 每个测试用例相互独立,可以单独运行

## 未来改进

1. 添加集成测试,测试完整的用户交互流程
2. 使用 `pytest` 提供更丰富的测试功能和报告
3. 添加代码覆盖率工具(如 `coverage.py`)
4. 添加性能测试,验证响应时间
5. 添加端到端测试,使用真实的 API(在测试环境)
