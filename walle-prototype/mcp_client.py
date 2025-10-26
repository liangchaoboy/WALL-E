#!/usr/bin/env python3
"""
MCP Client for WALL-E
Manages MCP servers and provides unified tool access
"""

import importlib
import sys
import asyncio
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from logger_config import setup_logger

logger = setup_logger("WALL-E.MCPClient", level=os.getenv("LOG_LEVEL", "INFO"))

class MCPClient:
    """MCP Client for managing multiple MCP servers"""
    
    def __init__(self):
        self.servers: Dict[str, Any] = {}
        self.tools: Dict[str, Any] = {}
        
    def register_server(self, server_name: str, server_module_path: str):
        """
        Register an MCP server
        
        Args:
            server_name: Name of the server
            server_module_path: Path to the server module
        """
        try:
            logger.debug(f"尝试注册 MCP Server: {server_name}, 路径: {server_module_path}")
            sys.path.insert(0, str(Path(server_module_path).parent))
            module_name = Path(server_module_path).stem
            module = importlib.import_module(module_name)
            
            if hasattr(module, 'mcp'):
                self.servers[server_name] = module.mcp
                self._discover_tools(server_name, module.mcp)
                logger.info(f"成功注册 MCP Server: {server_name}")
                print(f"✅ 注册 MCP Server: {server_name}")
            else:
                logger.error(f"模块 {module_name} 没有 'mcp' 对象")
                print(f"❌ 模块 {module_name} 没有 'mcp' 对象")
                
        except Exception as e:
            logger.error(f"注册 MCP Server 失败 ({server_name}): {e}", exc_info=True)
            print(f"❌ 注册 MCP Server 失败 ({server_name}): {e}")
    
    def _discover_tools(self, server_name: str, mcp_server: Any):
        """
        Discover tools from an MCP server
        
        Args:
            server_name: Name of the server
            mcp_server: MCP server instance
        """
        try:
            logger.debug(f"开始发现 {server_name} 的工具...")
            # Use asyncio to get tools from MCP server
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tools = loop.run_until_complete(mcp_server.list_tools())
            loop.close()
            
            logger.info(f"从 {server_name} 发现了 {len(tools)} 个工具")
            for tool in tools:
                tool_name = tool.name
                full_tool_name = f"{server_name}.{tool_name}"
                logger.debug(f"注册工具: {full_tool_name}")
                
                # Create synchronous wrapper with proper closure
                def create_sync_wrapper(name):
                    def sync_tool_wrapper(**kwargs):
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            logger.debug(f"调用 MCP 工具: {name}, 参数: {kwargs}")
                            result = loop.run_until_complete(mcp_server.call_tool(name, kwargs))
                            # Extract the actual result from the MCP response
                            if isinstance(result, tuple) and len(result) >= 2:
                                content, metadata = result
                                if isinstance(metadata, dict) and 'result' in metadata:
                                    return metadata['result']
                                elif content and hasattr(content[0], 'text'):
                                    return content[0].text
                            return str(result)
                        finally:
                            loop.close()
                    return sync_tool_wrapper
                
                sync_wrapper = create_sync_wrapper(tool_name)
                self.tools[full_tool_name] = sync_wrapper
                self.tools[tool_name] = sync_wrapper
                
        except Exception as e:
            logger.error(f"工具发现失败 ({server_name}): {e}", exc_info=True)
            print(f"⚠️  工具发现失败 ({server_name}): {e}")
    
    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self.tools.keys())
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call a tool by name
        
        Args:
            tool_name: Name of the tool
            **kwargs: Tool arguments
            
        Returns:
            Tool execution result
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
        """Get tool documentation"""
        if tool_name not in self.tools:
            return None
        
        tool_func = self.tools[tool_name]
        return tool_func.__doc__ or "No documentation available"

def create_mcp_client(servers_dir: str = None) -> MCPClient:
    """
    Create and configure MCP client with default servers
    
    Args:
        servers_dir: Directory containing MCP server modules
        
    Returns:
        Configured MCPClient instance
    """
    logger.info("创建 MCP 客户端...")
    client = MCPClient()
    
    if servers_dir is None:
        servers_dir = Path(__file__).parent / "mcp_servers"
    else:
        servers_dir = Path(servers_dir)
    
    logger.debug(f"MCP Servers 目录: {servers_dir}")
    server_modules = {
        "navigation": servers_dir / "navigation_server.py",
        "weather": servers_dir / "weather_server.py",
        "music": servers_dir / "music_server.py"
    }
    
    for name, path in server_modules.items():
        if path.exists():
            client.register_server(name, str(path))
        else:
            logger.warning(f"MCP Server 文件不存在: {path}")
            print(f"⚠️  MCP Server 文件不存在: {path}")
    
    logger.info(f"MCP 客户端创建完成,共加载 {len(client.servers)} 个 Server")
    return client

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 WALL-E MCP Client 测试")
    print("=" * 50)
    
    client = create_mcp_client()
    
    print("\n📋 可用工具:")
    unique_tools = set()
    for tool in client.list_tools():
        if '.' not in tool:
            unique_tools.add(tool)
    
    for tool in sorted(unique_tools):
        print(f"  - {tool}")
        doc = client.get_tool_info(tool)
        if doc:
            print(f"    {doc.strip().split(chr(10))[0]}")
    
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
