#!/usr/bin/env python3
"""
WALL-E 语音导航原型 (简化版 MCP 架构)
集成 MCP 架构概念,但不依赖 mcp 第三方库
适用于快速验证,无需安装额外依赖
"""

import os
import json
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
from mcp_client_simple import create_simple_mcp_client
from logger_config import setup_logger

logger = setup_logger("WALL-E.VoiceNavSimple", level=os.getenv("LOG_LEVEL", "INFO"))

load_dotenv()
logger.info("初始化 OpenAI 客户端...")
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL", "https://api.openai.com/v1")
)

logger.info("初始化简化版 MCP 客户端...")
mcp_client = create_simple_mcp_client()

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

def understand_with_mcp(text):
    """AI 理解用户意图并选择 MCP 工具"""
    logger.info(f"开始 AI 理解用户输入: {text}")
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
        logger.debug(f"调用 LLM 模型: {os.getenv('MODEL', 'gpt-3.5-turbo')}")
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
        logger.info(f"AI 理解结果: tool={result.get('tool')}, params={result.get('params')}")
        print(f"🤖 AI: {result}")
        return result
        
    except Exception as e:
        logger.error(f"AI 理解失败: {e}", exc_info=True)
        print(f"❌ AI失败: {e}")
        return {"tool": "unknown", "params": {}}

def execute_tool(tool_name, params):
    """执行 MCP 工具"""
    if tool_name == "unknown":
        logger.warning("无法识别用户意图,工具为 unknown")
        print("❓ 没听懂,请重新说明")
        return
    
    logger.info(f"执行 MCP 工具: {tool_name}, 参数: {params}")
    print(f"🔧 调用工具: {tool_name}")
    try:
        result = mcp_client.call_tool(tool_name, **params)
        logger.info(f"工具执行成功: {result}")
        print(f"✅ {result}")
    except Exception as e:
        logger.error(f"工具执行失败: {e}", exc_info=True)
        print(f"❌ 工具执行失败: {e}")

def main():
    """主程序"""
    logger.info("WALL-E 简化版语音助手启动")
    print("=" * 60)
    print("🤖 WALL-E 语音助手 (简化版 MCP 架构)")
    print("支持导航、天气、音乐等多种功能")
    print("说话即可操作,说'退出'结束")
    print("=" * 60)
    
    tool_count = len(mcp_client.list_tools())
    logger.info(f"已加载 {tool_count} 个 MCP 工具")
    print(f"\n📦 已加载 {tool_count} 个工具")
    
    logger.info("进入主循环,等待用户输入...")
    while True:
        text = listen()
        if not text:
            continue
        
        if "退出" in text or "结束" in text:
            logger.info("用户请求退出程序")
            print("👋 再见!")
            break
        
        intent = understand_with_mcp(text)
        execute_tool(intent.get("tool"), intent.get("params", {}))
    
    logger.info("WALL-E 简化版语音助手已退出")

if __name__ == "__main__":
    main()
