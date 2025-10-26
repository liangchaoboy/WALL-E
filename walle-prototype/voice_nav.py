#!/usr/bin/env python3
"""
WALL-E 语音导航原型
1天快速开发版本 - 能跑就行!
"""

import os
import json
import webbrowser
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL", "https://api.openai.com/v1")
)

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
    """文字输入"""
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

def understand(text):
    """AI 理解用户意图"""
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-3.5-turbo"),
            messages=[
                {
                    "role": "system",
                    "content": """你是导航助手。用户说导航需求,提取起点终点。
返回 JSON:
- 导航: {"action":"nav","from":"起点","to":"终点"}  
- 其他: {"action":"unknown"}"""
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
        return {"action": "unknown"}

def navigate(origin, destination):
    """打开百度地图"""
    url = f"https://map.baidu.com/?from={origin}&to={destination}"
    webbrowser.open(url)
    print(f"🗺️  已打开: {origin} → {destination}")

def main():
    """主程序"""
    print("=" * 50)
    print("🤖 WALL-E 语音导航原型")
    print("支持语音输入和文字输入")
    print("=" * 50)
    
    print("\n请选择输入模式:")
    print("1. 语音输入 (按回车键)")
    print("2. 文字输入 (输入 2)")
    
    mode_choice = input("\n选择模式 [1]: ").strip()
    input_mode = "text" if mode_choice == "2" else "voice"
    
    mode_text = "文字输入" if input_mode == "text" else "语音输入"
    print(f"\n✅ 已选择: {mode_text}")
    print("输入'退出'或'结束'可结束程序")
    print("=" * 50)
    
    while True:
        text = get_user_input(input_mode)
        if not text:
            continue
        
        if "退出" in text or "结束" in text:
            print("👋 再见!")
            break
        
        intent = understand(text)
        
        if intent.get("action") == "nav":
            navigate(
                intent.get("from", "当前位置"),
                intent.get("to", "")
            )
        else:
            print("❓ 没听懂,请说导航指令")

if __name__ == "__main__":
    main()
