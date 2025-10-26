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
from logger_config import setup_logger

logger = setup_logger("WALL-E.VoiceNav", level=os.getenv("LOG_LEVEL", "INFO"))

load_dotenv()
logger.info("初始化 OpenAI 客户端...")
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL", "https://api.openai.com/v1")
)

def listen():
    """监听语音并转文字"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n🎤 请说话...")
        logger.info("开始监听语音输入...")
        try:
            audio = recognizer.listen(source, timeout=5)
            logger.debug("音频捕获成功,开始识别...")
            text = recognizer.recognize_google(audio, language='zh-CN')
            logger.info(f"语音识别成功: {text}")
            print(f"📝 识别: {text}")
            return text
        except sr.WaitTimeoutError:
            logger.warning("语音监听超时,没有检测到声音")
            print("⏰ 没听到声音")
            return None
        except sr.UnknownValueError:
            logger.warning("语音识别失败,无法理解音频内容")
            print("❌ 无法识别")
            return None
        except Exception as e:
            logger.error(f"语音识别出错: {e}", exc_info=True)
            print(f"❌ 错误: {e}")
            return None

def text_input():
    """文字输入"""
    try:
        text = input("\n💬 请输入(输入'退出'结束): ").strip()
        if text:
            logger.info(f"文字输入成功: {text}")
            print(f"📝 输入: {text}")
            return text
        return None
    except (EOFError, KeyboardInterrupt):
        logger.info("用户中断输入")
        return "退出"

def get_user_input(mode):
    """根据模式获取用户输入"""
    if mode == "voice":
        return listen()
    else:
        return text_input()

def understand(text):
    """AI 理解用户意图"""
    logger.info(f"开始 AI 理解用户输入: {text}")
    try:
        logger.debug(f"调用 LLM 模型: {os.getenv('MODEL', 'gpt-3.5-turbo')}")
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
        logger.info(f"AI 理解结果: {result}")
        print(f"🤖 AI: {result}")
        return result
        
    except Exception as e:
        logger.error(f"AI 理解失败: {e}", exc_info=True)
        print(f"❌ AI失败: {e}")
        return {"action": "unknown"}

def navigate(origin, destination):
    """打开百度地图"""
    logger.info(f"执行导航: {origin} → {destination}")
    url = f"https://map.baidu.com/?from={origin}&to={destination}"
    try:
        webbrowser.open(url)
        logger.info(f"已打开百度地图: {url}")
        print(f"🗺️  已打开: {origin} → {destination}")
    except Exception as e:
        logger.error(f"打开地图失败: {e}", exc_info=True)
        print(f"❌ 打开地图失败: {e}")

def main():
    """主程序"""
    logger.info("WALL-E 语音导航原型启动")
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
    logger.info(f"用户选择输入模式: {mode_text}")
    print(f"\n✅ 已选择: {mode_text}")
    print("输入'退出'或'结束'可结束程序")
    print("=" * 50)
    
    logger.info("进入主循环,等待用户输入...")
    while True:
        text = get_user_input(input_mode)
        if not text:
            continue
        
        if "退出" in text or "结束" in text:
            logger.info("用户请求退出程序")
            print("👋 再见!")
            break
        
        intent = understand(text)
        
        if intent.get("action") == "nav":
            navigate(
                intent.get("from", "当前位置"),
                intent.get("to", "")
            )
        else:
            logger.warning("无法识别用户意图")
            print("❓ 没听懂,请说导航指令")
    
    logger.info("WALL-E 语音导航原型已退出")

if __name__ == "__main__":
    main()
