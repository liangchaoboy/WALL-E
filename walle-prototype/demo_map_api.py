#!/usr/bin/env python3
"""
地图Web API功能演示
展示如何使用API获取详细路线信息
"""

import os
from dotenv import load_dotenv
from mcp_servers_simple.navigation_tools_api import navigate_with_api

load_dotenv()

print("=" * 80)
print("🗺️  地图Web API功能演示")
print("=" * 80)

# 读取API密钥
amap_key = os.getenv("AMAP_API_KEY")
baidu_key = os.getenv("BAIDU_API_KEY")

if not amap_key:
    print("\n⚠️  未配置 AMAP_API_KEY")
    print("📋 配置方法:")
    print("   1. 注册高德开放平台: https://console.amap.com/")
    print("   2. 创建应用并添加Web服务API Key")
    print("   3. 在 .env 文件中添加: AMAP_API_KEY=your_key")
    print("\n✅ 暂时使用普通导航模式（无需API）")
    use_api = False
else:
    print(f"\n✅ 已配置 AMAP_API_KEY")
    use_api = True

print("\n" + "=" * 80)
print("测试1: 上海七牛云 → 虹桥机场")
print("=" * 80)

result = navigate_with_api(
    origin="上海七牛云",
    destination="虹桥机场",
    map_service="amap",
    api_key=amap_key,
    use_api=use_api
)

print(result)

print("\n" + "=" * 80)
print("测试2: 北京 → 上海")
print("=" * 80)

result = navigate_with_api(
    origin="北京",
    destination="上海",
    map_service="amap",
    api_key=amap_key,
    use_api=use_api
)

print(result)

if use_api:
    print("\n" + "=" * 80)
    print("✅ 使用Web API - 可以获取详细路线信息")
    print("=" * 80)
    print("\n优势:")
    print("  ✅ 自动获取距离和预计时间")
    print("  ✅ 显示主要路段信息")
    print("  ✅ 不需要用户手动操作")
    print("  ✅ 适合语音播报")
else:
    print("\n" + "=" * 80)
    print("✅ 使用普通导航 - 打开网页地图")
    print("=" * 80)
    print("\n特点:")
    print("  ✅ 不需要API密钥")
    print("  ✅ 在浏览器中显示地图")
    print("  ⚠️  需要用户手动点击开始导航")
    print("\n💡 配置API后可以获取详细路线信息！")

print("\n" + "=" * 80)
print("📖 更多信息:")
print("   - 查看 MAP_API_USAGE.md 了解详细使用方法")
print("   - 查看 MAP_NAVIGATION_SOLUTION.md 了解解决方案对比")
print("=" * 80)
