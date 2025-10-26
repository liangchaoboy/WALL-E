#!/usr/bin/env python3
"""
简化版 MCP Client (不依赖 mcp 库)
用于快速验证 MCP 架构,无需安装第三方 mcp 包
"""

import importlib
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from logger_config import setup_logger

logger = setup_logger("WALL-E.SimpleMCPClient", level=os.getenv("LOG_LEVEL", "INFO"))

class SimpleMCPClient:
    """简化版 MCP 客户端,不依赖 mcp 库"""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}
        
    def register_tools_module(self, module_name: str, module_path: str):
        """
        从工具模块注册工具
        
        Args:
            module_name: 模块名称
            module_path: 模块文件路径
        """
        try:
            logger.debug(f"尝试注册工具模块: {module_name}, 路径: {module_path}")
            sys.path.insert(0, str(Path(module_path).parent))
            module_file = Path(module_path).stem
            module = importlib.import_module(module_file)
            
            if hasattr(module, 'TOOLS'):
                for tool_name, tool_func in module.TOOLS.items():
                    self.tools[tool_name] = tool_func
                    logger.debug(f"注册工具: {tool_name}")
                logger.info(f"成功注册工具模块: {module_name} ({len(module.TOOLS)} 个工具)")
                print(f"✅ 注册工具模块: {module_name} ({len(module.TOOLS)} 个工具)")
            else:
                logger.error(f"模块 {module_file} 没有 TOOLS 字典")
                print(f"❌ 模块 {module_file} 没有 TOOLS 字典")
                
        except Exception as e:
            logger.error(f"注册工具模块失败 ({module_name}): {e}", exc_info=True)
            print(f"❌ 注册工具模块失败 ({module_name}): {e}")
    
    def list_tools(self) -> List[str]:
        """列出所有可用工具"""
        return list(self.tools.keys())
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        调用工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            工具执行结果
        """
        if tool_name not in self.tools:
            available = ', '.join(self.list_tools())
            logger.warning(f"工具 '{tool_name}' 不存在,可用工具: {available}")
            return f"工具 '{tool_name}' 不存在。可用工具: {available}"
        
        try:
            logger.debug(f"调用工具: {tool_name}, 参数: {kwargs}")
            tool_func = self.tools[tool_name]
            result = tool_func(**kwargs)
            logger.debug(f"工具 {tool_name} 返回结果: {result}")
            return result
        except Exception as e:
            logger.error(f"工具 {tool_name} 调用失败: {e}", exc_info=True)
            return f"工具调用失败: {e}"
    
    def get_tool_info(self, tool_name: str) -> Optional[str]:
        """获取工具文档"""
        if tool_name not in self.tools:
            return None
        
        tool_func = self.tools[tool_name]
        return tool_func.__doc__ or "无文档"

def create_simple_mcp_client(tools_dir: str = None) -> SimpleMCPClient:
    """
    创建并配置简化版 MCP 客户端
    
    Args:
        tools_dir: 工具模块目录
        
    Returns:
        配置好的 SimpleMCPClient 实例
    """
    logger.info("创建简化版 MCP 客户端...")
    client = SimpleMCPClient()
    
    if tools_dir is None:
        tools_dir = Path(__file__).parent / "mcp_servers_simple"
    else:
        tools_dir = Path(tools_dir)
    
    logger.debug(f"工具模块目录: {tools_dir}")
    tool_modules = {
        "navigation": tools_dir / "navigation_tools.py",
        "weather": tools_dir / "weather_tools.py",
        "music": tools_dir / "music_tools.py"
    }
    
    for name, path in tool_modules.items():
        if path.exists():
            client.register_tools_module(name, str(path))
        else:
            logger.warning(f"工具模块文件不存在: {path}")
            print(f"⚠️  工具模块文件不存在: {path}")
    
    logger.info(f"简化版 MCP 客户端创建完成,共加载 {len(client.tools)} 个工具")
    return client

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 WALL-E 简化版 MCP 客户端测试")
    print("=" * 50)
    
    client = create_simple_mcp_client()
    
    print("\n📋 可用工具:")
    for tool in sorted(client.list_tools()):
        print(f"  - {tool}")
        doc = client.get_tool_info(tool)
        if doc:
            first_line = doc.strip().split('\n')[0]
            print(f"    {first_line}")
    
    print("\n🧪 测试工具调用:")
    print("\n1. 测试导航工具:")
    result = client.call_tool("navigate", origin="上海", destination="北京")
    print(f"   {result}")
    
    print("\n2. 测试天气工具:")
    result = client.call_tool("get_weather", city="上海", date="明天")
    print(f"   {result}")
    
    print("\n3. 测试音乐工具:")
    result = client.call_tool("play_music", song="晴天", artist="周杰伦")
    print(f"   {result}")
