#!/usr/bin/env python3
"""
Integration tests for WALL-E system
Tests end-to-end functionality across multiple components
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp_client_simple import create_simple_mcp_client
from logger_config import setup_logger


class TestEndToEndIntegration(unittest.TestCase):
    """端到端集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = create_simple_mcp_client()
    
    def test_system_initialization(self):
        """测试系统初始化"""
        # 验证MCP客户端创建成功
        self.assertIsNotNone(self.client)
        
        # 验证工具已加载
        tools = self.client.list_tools()
        self.assertGreater(len(tools), 0, "System should have loaded tools")
        
        # 验证核心工具可用
        required_tools = ['navigate', 'get_weather', 'play_music']
        for tool in required_tools:
            self.assertIn(tool, tools, f"Required tool '{tool}' not available")
    
    @patch('mcp_servers_simple.navigation_tools.webbrowser.open')
    def test_navigation_workflow(self, mock_open):
        """测试导航工作流"""
        mock_open.return_value = True
        
        # 1. 搜索地点
        search_result = self.client.call_tool('search_location', query='虹桥机场')
        self.assertIn('虹桥机场', search_result)
        
        # 2. 导航到地点
        nav_result = self.client.call_tool('navigate', origin='上海东方明珠', destination='虹桥机场')
        self.assertIn('成功', nav_result)
        self.assertIn('虹桥机场', nav_result)
        
        # 验证浏览器被调用了2次
        self.assertEqual(mock_open.call_count, 2)
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_weather_workflow(self, mock_open):
        """测试天气查询工作流"""
        mock_open.return_value = True
        
        # 1. 查询单个城市天气
        result1 = self.client.call_tool('get_weather', city='北京', date='今天')
        self.assertIn('北京', result1)
        
        # 2. 查询另一个城市
        result2 = self.client.call_tool('get_weather', city='上海', date='明天')
        self.assertIn('上海', result2)
        
        # 3. 对比两个城市天气
        compare_result = self.client.call_tool('compare_weather', city1='北京', city2='上海')
        self.assertIn('北京', compare_result)
        self.assertIn('上海', compare_result)
        
        # 验证调用次数
        self.assertEqual(mock_open.call_count, 3)
    
    @patch('mcp_servers_simple.music_tools.webbrowser.open')
    def test_music_workflow(self, mock_open):
        """测试音乐播放工作流"""
        mock_open.return_value = True
        
        # 1. 播放特定歌曲
        play_result = self.client.call_tool('play_music', song='晴天', artist='周杰伦')
        self.assertIn('晴天', play_result)
        
        # 2. 搜索歌单
        playlist_result = self.client.call_tool('search_playlist', keyword='周杰伦')
        self.assertIn('周杰伦', playlist_result)
        
        # 验证调用次数
        self.assertEqual(mock_open.call_count, 2)
    
    @patch('mcp_servers_simple.navigation_tools.webbrowser.open')
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    @patch('mcp_servers_simple.music_tools.webbrowser.open')
    def test_mixed_workflow(self, mock_music, mock_weather, mock_nav):
        """测试混合使用多个工具"""
        mock_nav.return_value = True
        mock_weather.return_value = True
        mock_music.return_value = True
        
        # 模拟用户场景: 计划出行
        # 1. 查询目的地天气
        weather = self.client.call_tool('get_weather', city='杭州', date='明天')
        self.assertIn('杭州', weather)
        
        # 2. 规划导航路线
        nav = self.client.call_tool('navigate', origin='上海', destination='杭州')
        self.assertIn('杭州', nav)
        
        # 3. 准备路上听的音乐
        music = self.client.call_tool('search_playlist', keyword='旅行')
        self.assertIn('旅行', music)
        
        # 验证所有工具都被调用
        mock_weather.assert_called_once()
        mock_nav.assert_called_once()
        mock_music.assert_called_once()


class TestAIIntegration(unittest.TestCase):
    """AI理解与工具调用集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = create_simple_mcp_client()
    
    @patch('mcp_servers_simple.navigation_tools.webbrowser.open')
    def test_ai_intent_to_tool_navigation(self, mock_open):
        """测试AI意图识别到工具调用(导航)"""
        mock_open.return_value = True
        
        # 模拟AI理解结果
        ai_intent = {
            "tool": "navigate",
            "params": {"origin": "北京天安门", "destination": "故宫"}
        }
        
        # 执行工具
        result = self.client.call_tool(ai_intent["tool"], **ai_intent["params"])
        
        self.assertIn('成功', result)
        self.assertIn('天安门', result)
        self.assertIn('故宫', result)
        mock_open.assert_called_once()
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_ai_intent_to_tool_weather(self, mock_open):
        """测试AI意图识别到工具调用(天气)"""
        mock_open.return_value = True
        
        # 模拟AI理解结果
        ai_intent = {
            "tool": "get_weather",
            "params": {"city": "深圳", "date": "后天"}
        }
        
        # 执行工具
        result = self.client.call_tool(ai_intent["tool"], **ai_intent["params"])
        
        self.assertIn('深圳', result)
        mock_open.assert_called_once()
    
    @patch('mcp_servers_simple.music_tools.webbrowser.open')
    def test_ai_intent_to_tool_music(self, mock_open):
        """测试AI意图识别到工具调用(音乐)"""
        mock_open.return_value = True
        
        # 模拟AI理解结果
        ai_intent = {
            "tool": "play_music",
            "params": {"song": "七里香", "artist": "周杰伦", "platform": "qq"}
        }
        
        # 执行工具
        result = self.client.call_tool(ai_intent["tool"], **ai_intent["params"])
        
        self.assertIn('七里香', result)
        mock_open.assert_called_once()
    
    def test_ai_intent_unknown_tool(self):
        """测试AI识别到未知工具"""
        ai_intent = {
            "tool": "unknown_tool",
            "params": {}
        }
        
        # 执行应返回错误消息而不是崩溃
        result = self.client.call_tool(ai_intent["tool"], **ai_intent["params"])
        
        self.assertIn('不存在', result)
    
    def test_ai_intent_missing_params(self):
        """测试AI意图缺少必需参数"""
        ai_intent = {
            "tool": "navigate",
            "params": {"origin": "上海"}  # 缺少destination
        }
        
        # 应该能处理而不崩溃
        result = self.client.call_tool(ai_intent["tool"], **ai_intent["params"])
        
        # 根据实现,可能返回错误或使用默认值
        self.assertIsInstance(result, str)


class TestErrorRecovery(unittest.TestCase):
    """错误恢复测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = create_simple_mcp_client()
    
    @patch('mcp_servers_simple.navigation_tools.webbrowser.open')
    def test_browser_failure_recovery(self, mock_open):
        """测试浏览器打开失败后的恢复"""
        mock_open.side_effect = Exception("Browser not available")
        
        # 第一次调用失败
        result1 = self.client.call_tool('navigate', origin='A', destination='B')
        self.assertIn('失败', result1)
        
        # 系统应该能继续工作
        mock_open.side_effect = None
        mock_open.return_value = True
        
        result2 = self.client.call_tool('search_location', query='测试地点')
        self.assertIn('测试地点', result2)
    
    def test_invalid_input_recovery(self):
        """测试无效输入后的恢复"""
        # 空参数
        result1 = self.client.call_tool('navigate', origin='', destination='')
        self.assertIn('错误', result1)
        
        # 系统应该能继续工作
        with patch('mcp_servers_simple.weather_tools.webbrowser.open'):
            result2 = self.client.call_tool('get_weather', city='北京')
            self.assertIn('北京', result2)
    
    def test_multiple_failures_recovery(self):
        """测试多次失败后的恢复"""
        # 连续多次错误调用
        self.client.call_tool('unknown_tool1')
        self.client.call_tool('unknown_tool2')
        self.client.call_tool('unknown_tool3')
        
        # 系统应该仍然正常工作
        with patch('mcp_servers_simple.music_tools.webbrowser.open'):
            result = self.client.call_tool('play_music', song='test')
            self.assertIsInstance(result, str)


class TestConcurrentOperations(unittest.TestCase):
    """并发操作测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = create_simple_mcp_client()
    
    @patch('mcp_servers_simple.navigation_tools.webbrowser.open')
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_rapid_tool_switching(self, mock_weather, mock_nav):
        """测试快速切换工具"""
        mock_nav.return_value = True
        mock_weather.return_value = True
        
        # 快速连续调用不同工具
        results = []
        results.append(self.client.call_tool('navigate', origin='A', destination='B'))
        results.append(self.client.call_tool('get_weather', city='北京'))
        results.append(self.client.call_tool('navigate', origin='C', destination='D'))
        results.append(self.client.call_tool('get_weather', city='上海'))
        
        # 所有调用都应该成功
        for result in results:
            self.assertIsInstance(result, str)
            self.assertNotIn('错误', result)
    
    @patch('mcp_servers_simple.music_tools.webbrowser.open')
    def test_same_tool_multiple_times(self, mock_open):
        """测试同一工具多次调用"""
        mock_open.return_value = True
        
        songs = ['歌曲1', '歌曲2', '歌曲3', '歌曲4', '歌曲5']
        
        for song in songs:
            result = self.client.call_tool('play_music', song=song)
            self.assertIn(song, result)
        
        # 验证所有调用都执行了
        self.assertEqual(mock_open.call_count, len(songs))


class TestDataFlow(unittest.TestCase):
    """数据流测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = create_simple_mcp_client()
    
    @patch('mcp_servers_simple.navigation_tools.webbrowser.open')
    def test_parameter_passing(self, mock_open):
        """测试参数传递"""
        mock_open.return_value = True
        
        # 测试各种参数类型
        test_cases = [
            {'origin': '上海', 'destination': '北京'},
            {'origin': 'Shanghai', 'destination': 'Beijing'},
            {'origin': '上海浦东机场T2', 'destination': '北京首都机场T3'},
            {'origin': '起点🚀', 'destination': '终点✈️'},
        ]
        
        for params in test_cases:
            result = self.client.call_tool('navigate', **params)
            self.assertIn(params['origin'], result)
            self.assertIn(params['destination'], result)
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_optional_parameters(self, mock_open):
        """测试可选参数"""
        mock_open.return_value = True
        
        # 使用默认参数
        result1 = self.client.call_tool('get_weather', city='北京')
        self.assertIn('北京', result1)
        
        # 指定可选参数
        result2 = self.client.call_tool('get_weather', city='上海', date='明天')
        self.assertIn('上海', result2)
        self.assertIn('明天', result2)
    
    def test_return_value_format(self):
        """测试返回值格式"""
        tools_to_test = ['navigate', 'get_weather', 'play_music']
        
        with patch('mcp_servers_simple.navigation_tools.webbrowser.open'), \
             patch('mcp_servers_simple.weather_tools.webbrowser.open'), \
             patch('mcp_servers_simple.music_tools.webbrowser.open'):
            
            for tool in tools_to_test:
                if tool == 'navigate':
                    result = self.client.call_tool(tool, origin='A', destination='B')
                elif tool == 'get_weather':
                    result = self.client.call_tool(tool, city='北京')
                elif tool == 'play_music':
                    result = self.client.call_tool(tool, song='test')
                
                # 所有工具都应该返回字符串
                self.assertIsInstance(result, str)
                # 返回值不应该为空
                self.assertGreater(len(result), 0)


class TestSystemRobustness(unittest.TestCase):
    """系统健壮性测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = create_simple_mcp_client()
    
    def test_empty_string_handling(self):
        """测试空字符串处理"""
        # 导航工具
        nav_result = self.client.call_tool('navigate', origin='', destination='')
        self.assertIn('错误', nav_result)
        
        # 天气工具
        weather_result = self.client.call_tool('get_weather', city='')
        self.assertIn('错误', weather_result)
        
        # 音乐工具
        music_result = self.client.call_tool('play_music', song='')
        self.assertIn('错误', music_result)
    
    def test_whitespace_handling(self):
        """测试空格处理"""
        with patch('mcp_servers_simple.navigation_tools.webbrowser.open'), \
             patch('mcp_servers_simple.weather_tools.webbrowser.open'), \
             patch('mcp_servers_simple.music_tools.webbrowser.open'):
            
            # 前后空格应该被正确处理
            nav_result = self.client.call_tool('navigate', origin='  上海  ', destination='  北京  ')
            self.assertNotIn('错误', nav_result)
    
    def test_special_characters_handling(self):
        """测试特殊字符处理"""
        with patch('mcp_servers_simple.navigation_tools.webbrowser.open'), \
             patch('mcp_servers_simple.music_tools.webbrowser.open'):
            
            # 包含特殊字符的输入
            nav_result = self.client.call_tool('navigate', origin='上海&浦东', destination='北京@朝阳')
            self.assertIsInstance(nav_result, str)
            
            music_result = self.client.call_tool('play_music', song='Rock&Roll')
            self.assertIsInstance(music_result, str)
    
    def test_very_long_input(self):
        """测试超长输入"""
        with patch('mcp_servers_simple.navigation_tools.webbrowser.open'):
            long_string = "非常" * 100 + "长的地点名称"
            
            result = self.client.call_tool('navigate', origin=long_string, destination='北京')
            # 应该能处理而不崩溃
            self.assertIsInstance(result, str)
    
    def test_unicode_emoji_handling(self):
        """测试Unicode和Emoji处理"""
        with patch('mcp_servers_simple.navigation_tools.webbrowser.open'), \
             patch('mcp_servers_simple.music_tools.webbrowser.open'):
            
            nav_result = self.client.call_tool('navigate', origin='起点🚀', destination='终点✈️')
            self.assertIsInstance(nav_result, str)
            
            music_result = self.client.call_tool('play_music', song='Happy🎵', artist='Artist🎤')
            self.assertIsInstance(music_result, str)


if __name__ == '__main__':
    # 运行所有集成测试
    unittest.main(verbosity=2)

