#!/usr/bin/env python3
"""
WALL-E MCP 功能演示脚本
无需语音,直接测试 MCP 集成功能
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from mcp_client import create_mcp_client
from logger_config import setup_logger

logger = setup_logger("WALL-E.Demo", level=os.getenv("LOG_LEVEL", "INFO"))

load_dotenv()

logger.info("WALL-E MCP 功能演示启动")
print("=" * 60)
print("🤖 WALL-E MCP 功能演示")
print("=" * 60)

print("\n1️⃣  初始化 MCP 客户端...")
logger.info("开始初始化 MCP 客户端...")
mcp_client = create_mcp_client()

print("\n2️⃣  列出所有可用工具:")
unique_tools = set()
for tool in mcp_client.list_tools():
    if '.' not in tool:
        unique_tools.add(tool)

for i, tool in enumerate(sorted(unique_tools), 1):
    print(f"   {i}. {tool}")

print("\n3️⃣  测试各个工具:")
logger.info("开始测试各个工具")

print("\n   📍 导航工具测试:")
logger.info("测试导航工具")
print("      - navigate(上海, 北京)")
result = mcp_client.call_tool("navigate", origin="上海", destination="北京")
print(f"      ✅ {result}")

print("\n      - search_location(虹桥机场)")
result = mcp_client.call_tool("search_location", query="虹桥机场")
print(f"      ✅ {result}")

print("\n   🌤️  天气工具测试:")
print("      - get_weather(上海, 明天)")
result = mcp_client.call_tool("get_weather", city="上海", date="明天")
print(f"      ✅ {result}")

print("\n      - compare_weather(北京, 上海)")
result = mcp_client.call_tool("compare_weather", city1="北京", city2="上海")
print(f"      ✅ {result}")

print("\n   🎵 音乐工具测试:")
print("      - play_music(晴天, 周杰伦)")
result = mcp_client.call_tool("play_music", song="晴天", artist="周杰伦")
print(f"      ✅ {result}")

print("\n      - search_playlist(流行音乐)")
result = mcp_client.call_tool("search_playlist", keyword="流行音乐")
print(f"      ✅ {result}")

if os.getenv("API_KEY"):
    print("\n4️⃣  测试 AI + MCP 集成:")
    
    # 首先测试API是否可用
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL", "https://api.openai.com/v1")
    )
    
    # 测试API连接
    api_available = False
    try:
        # 使用.env中配置的模型
        current_model = os.getenv("MODEL", "gpt-3.5-turbo")
        test_response = client.chat.completions.create(
            model=current_model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        api_available = True
        print(f"   ✅ API 连接成功 (模型: {current_model})")
    except Exception as e:
        print(f"   ⚠️  API 不可用: {str(e)[:100]}")
        print(f"   ℹ️  这可能是因为:")
        print(f"      1. API_KEY无效或过期")
        print(f"      2. 模型 {os.getenv('MODEL', 'gpt-3.5-turbo')} 未开通")
        print(f"      3. API服务暂时不可用")
        print(f"\n   ✅ 核心功能正常,可以跳过AI集成测试\n")
    
    if api_available:
        tools_description = """
可用工具:
1. navigate(origin, destination, map_service="amap") - 地图导航（默认高德）
2. search_location(query, map_service="amap") - 搜索地点
3. get_weather(city, date="today") - 查询天气
4. compare_weather(city1, city2) - 对比天气
5. play_music(song, artist="", platform="qq") - 播放音乐
6. search_playlist(keyword, platform="qq") - 搜索歌单
"""

        test_queries = [
            "从上海七牛云到虹桥机场",
            "查看明天北京的天气",
            "播放周杰伦的七里香"
        ]
        
        for query in test_queries:
            print(f"\n   用户: {query}")
            
            try:
                response = client.chat.completions.create(
                    model=current_model,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""你是 WALL-E 智能助手。根据用户需求选择合适的工具。

{tools_description}

返回 JSON:
- 格式: {{"tool": "工具名", "params": {{参数字典}}}}
- 不明确: {{"tool": "unknown", "params": {{}}}}
"""
                        },
                        {"role": "user", "content": query}
                    ],
                    temperature=0
                )
                
                # 获取响应内容
                content = response.choices[0].message.content
                print(f"   AI原始响应: {content}")
                
                # 清理代码块标记（如果有）
                if content.strip().startswith('```'):
                    # 移除开头的```json或```标记
                    lines = content.strip().split('\n')
                    content = '\n'.join(lines[1:-1])  # 去掉第一行和最后一行
                
                # 尝试解析JSON
                result = json.loads(content)
                print(f"   AI理解: {result}")
                
                if result.get("tool") != "unknown":
                    tool_result = mcp_client.call_tool(result["tool"], **result.get("params", {}))
                    print(f"   执行结果: {tool_result}")
                
            except Exception as e:
                print(f"   ❌ 错误: {e}")
                break  # 如果出错就停止尝试
    
    # 演示如何手动调用工具(即使AI不可用)
    print("\n   💡 提示: 即使AI不可用,您也可以直接手动调用工具:")
    print("      示例:")
    print("      from mcp_client_simple import create_simple_mcp_client")
    print("      client = create_simple_mcp_client()")
    print("      client.call_tool('navigate', origin='上海', destination='北京')")
else:
    print("\n⚠️  未配置 API_KEY,跳过 AI 集成测试")
    print("   提示: 配置 .env 文件后可测试完整的 AI + MCP 功能")

print("\n" + "=" * 60)
print("✅ MCP 功能演示完成!")
print("=" * 60)
print("\n📖 下一步:")
print("   1. 运行 'python voice_nav_mcp.py' 测试语音助手")
print("   2. 阅读 README_MCP.md 了解更多信息")
print("   3. 添加自己的 MCP Server 扩展功能")
print("\n🚀 WALL-E MCP 架构让扩展更简单!")
