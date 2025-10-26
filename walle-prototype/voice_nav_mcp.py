#!/usr/bin/env python3
"""
WALL-E 语音导航原型 (MCP 版本)
集成 MCP 架构,支持可扩展工具
"""

import os
import json
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
from mcp_client import create_mcp_client

load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL", "https://api.openai.com/v1")
)

mcp_client = create_mcp_client()

def listen():
    """监听语音并转文字"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n🎤 请说话...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='zh-CN')
            print(f"📝 识别: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⏰ 没听到声音")
            return None
        except sr.UnknownValueError:
            print("❌ 无法识别")
            return None
        except Exception as e:
            print(f"❌ 错误: {e}")
            return None

def text_input():
    """文字输入模式"""
    try:
        text = input("\n💬 请输入(输入'退出'结束): ").strip()
        if text:
            print(f"📝 输入: {text}")
            return text
        return None
    except (EOFError, KeyboardInterrupt):
        return "退出"

def get_user_input(mode):
    """根据模式获取用户输入"""
    if mode == "voice":
        return listen()
    else:
        return text_input()

def understand_with_mcp(text):
    """AI 理解用户意图并选择 MCP 工具"""
    tools_description = """
可用工具:
1. navigate(origin, destination, map_service="baidu") - 地图导航
2. search_location(query, map_service="baidu") - 搜索地点
3. get_weather(city, date="today") - 查询天气
4. compare_weather(city1, city2) - 对比天气
5. play_music(song, artist="", platform="qq") - 播放音乐
6. search_playlist(keyword, platform="qq") - 搜索歌单
"""
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-3.5-turbo"),
            messages=[
                {
                    "role": "system",
                    "content": f"""你是 WALL-E 智能助手。根据用户需求选择合适的工具。

{tools_description}

返回 JSON:
- 格式: {{"tool": "工具名", "params": {{参数字典}}}}
- 例子: {{"tool": "navigate", "params": {{"origin": "上海", "destination": "北京"}}}}
- 不明确: {{"tool": "unknown", "params": {{}}}}
"""
                },
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"🤖 AI: {result}")
        return result
        
    except Exception as e:
        print(f"❌ AI失败: {e}")
        return {"tool": "unknown", "params": {}}

def execute_tool(tool_name, params):
    """执行 MCP 工具"""
    if tool_name == "unknown":
        print("❓ 没听懂,请重新说明")
        return
    
    print(f"🔧 调用工具: {tool_name}")
    result = mcp_client.call_tool(tool_name, **params)
    print(f"✅ {result}")

def main():
    """主程序"""
    print("=" * 60)
    print("🤖 WALL-E 语音助手 (MCP 架构版本)")
    print("支持导航、天气、音乐等多种功能")
    print("=" * 60)
    
    print(f"\n📦 已加载 {len(set(t for t in mcp_client.list_tools() if '.' not in t))} 个工具")
    
    print("\n请选择输入模式:")
    print("1. 语音输入 (按回车键)")
    print("2. 文字输入 (输入 2)")
    
    mode_choice = input("\n选择模式 [1]: ").strip()
    input_mode = "text" if mode_choice == "2" else "voice"
    
    if input_mode == "voice":
        print("\n✅ 已启用语音输入模式 - 说话即可操作,说'退出'结束")
    else:
        print("\n✅ 已启用文字输入模式 - 输入命令,输入'退出'结束")
    
    print("=" * 60)
    
    while True:
        text = get_user_input(input_mode)
        if not text:
            continue
        
        if "退出" in text or "结束" in text:
            print("👋 再见!")
            break
        
        intent = understand_with_mcp(text)
        execute_tool(intent.get("tool"), intent.get("params", {}))

if __name__ == "__main__":
    main()
