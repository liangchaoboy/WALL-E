#!/usr/bin/env python3
"""
AI集成测试 - 使用Mock避免真实API调用
用于验证AI理解到工具调用的完整流程
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp_client_simple import create_simple_mcp_client


class TestAIIntegrationWithMock(unittest.TestCase):
    """AI集成测试 - 使用Mock"""
    
    def setUp(self):
        """设置测试环境"""
        self.mcp_client = create_simple_mcp_client()
    
    def test_ai_navigation_intent(self):
        """测试AI导航意图识别和工具调用"""
        # 模拟AI理解结果
        ai_intent = {
            "tool": "navigate",
            "params": {"origin": "上海七牛云", "destination": "虹桥机场"}
        }
        
        # 使用Mock阻止实际浏览器打开
        with patch('mcp_servers_simple.navigation_tools.webbrowser.open') as mock_open:
            mock_open.return_value = True
            
            # 执行工具调用
            result = self.mcp_client.call_tool(
                ai_intent["tool"], 
                **ai_intent["params"]
            )
            
            # 验证结果
            self.assertIn("成功", result)
            self.assertIn("虹桥机场", result)
            mock_open.assert_called_once()
    
    def test_ai_weather_intent(self):
        """测试AI天气查询意图"""
        ai_intent = {
            "tool": "get_weather",
            "params": {"city": "北京", "date": "明天"}
        }
        
        with patch('mcp_servers_simple.weather_tools.webbrowser.open') as mock_open:
            mock_open.return_value = True
            
            result = self.mcp_client.call_tool(
                ai_intent["tool"],
                **ai_intent["params"]
            )
            
            self.assertIn("北京", result)
            self.assertIn("明天", result)
            mock_open.assert_called_once()
    
    def test_ai_music_intent(self):
        """测试AI音乐播放意图"""
        ai_intent = {
            "tool": "play_music",
            "params": {"song": "七里香", "artist": "周杰伦"}
        }
        
        with patch('mcp_servers_simple.music_tools.webbrowser.open') as mock_open:
            mock_open.return_value = True
            
            result = self.mcp_client.call_tool(
                ai_intent["tool"],
                **ai_intent["params"]
            )
            
            self.assertIn("七里香", result)
            self.assertIn("周杰伦", result)
            mock_open.assert_called_once()
    
    def test_ai_mixed_workflow(self):
        """测试AI多步骤工作流"""
        # 模拟AI理解的多步骤操作
        workflow = [
            {
                "tool": "get_weather",
                "params": {"city": "北京", "date": "明天"}
            },
            {
                "tool": "navigate",
                "params": {"origin": "家", "destination": "北京"}
            },
            {
                "tool": "search_playlist",
                "params": {"keyword": "旅行音乐"}
            }
        ]
        
        with patch('mcp_servers_simple.weather_tools.webbrowser.open'), \
             patch('mcp_servers_simple.navigation_tools.webbrowser.open'), \
             patch('mcp_servers_simple.music_tools.webbrowser.open'):
            
            results = []
            for step in workflow:
                result = self.mcp_client.call_tool(step["tool"], **step["params"])
                results.append(result)
            
            # 验证所有步骤都成功
            self.assertEqual(len(results), 3)
            for result in results:
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)


if __name__ == '__main__':
    print("=" * 60)
    print("🧪 AI集成测试 (使用Mock)")
    print("=" * 60)
    print("\n✅ 这个测试不需要真实的API key")
    print("✅ 验证AI理解到工具执行的完整流程\n")
    
    unittest.main(verbosity=2)

