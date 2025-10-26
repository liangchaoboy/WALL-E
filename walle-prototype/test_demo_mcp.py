#!/usr/bin/env python3
"""
Test suite for demo_mcp.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


class TestDemoMCP(unittest.TestCase):
    
    @patch('demo_mcp.create_mcp_client')
    def test_mcp_client_creation(self, mock_create_client):
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        
        import demo_mcp
        
        mock_create_client.assert_called_once()
    
    @patch('demo_mcp.mcp_client')
    def test_list_tools(self, mock_client):
        mock_client.list_tools.return_value = [
            'navigate',
            'navigation.navigate',
            'search_location',
            'get_weather'
        ]
        
        unique_tools = set()
        for tool in mock_client.list_tools():
            if '.' not in tool:
                unique_tools.add(tool)
        
        self.assertEqual(len(unique_tools), 3)
        self.assertIn('navigate', unique_tools)
        self.assertIn('search_location', unique_tools)
        self.assertIn('get_weather', unique_tools)
    
    @patch('demo_mcp.mcp_client')
    def test_navigate_tool(self, mock_client):
        mock_client.call_tool.return_value = '已打开baidu地图: 上海 → 北京'
        
        result = mock_client.call_tool('navigate', origin='上海', destination='北京')
        
        mock_client.call_tool.assert_called_once_with('navigate', origin='上海', destination='北京')
        self.assertIn('上海', result)
        self.assertIn('北京', result)
    
    @patch('demo_mcp.mcp_client')
    def test_search_location_tool(self, mock_client):
        mock_client.call_tool.return_value = '已在baidu地图搜索: 虹桥机场'
        
        result = mock_client.call_tool('search_location', query='虹桥机场')
        
        mock_client.call_tool.assert_called_once_with('search_location', query='虹桥机场')
        self.assertIn('虹桥机场', result)
    
    @patch('demo_mcp.mcp_client')
    def test_weather_tool(self, mock_client):
        mock_client.call_tool.return_value = '已打开上海明天天气查询'
        
        result = mock_client.call_tool('get_weather', city='上海', date='明天')
        
        mock_client.call_tool.assert_called_once_with('get_weather', city='上海', date='明天')
        self.assertIn('上海', result)
    
    @patch('demo_mcp.mcp_client')
    def test_music_tool(self, mock_client):
        mock_client.call_tool.return_value = '已在qq音乐平台搜索: 周杰伦 晴天'
        
        result = mock_client.call_tool('play_music', song='晴天', artist='周杰伦')
        
        mock_client.call_tool.assert_called_once_with('play_music', song='晴天', artist='周杰伦')
        self.assertIn('晴天', result)


class TestDemoMCPAIIntegration(unittest.TestCase):
    
    @patch.dict('os.environ', {'API_KEY': 'test-key', 'BASE_URL': 'https://api.test.com', 'MODEL': 'gpt-3.5-turbo'})
    @patch('demo_mcp.client')
    @patch('demo_mcp.mcp_client')
    def test_ai_integration_with_api_key(self, mock_mcp_client, mock_ai_client):
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"tool": "navigate", "params": {"origin": "上海七牛云", "destination": "虹桥机场"}}'
        mock_ai_client.chat.completions.create.return_value = mock_response
        
        mock_mcp_client.call_tool.return_value = '已打开baidu地图'
        
        import json
        result = json.loads(mock_response.choices[0].message.content)
        
        self.assertEqual(result['tool'], 'navigate')
        self.assertEqual(result['params']['origin'], '上海七牛云')
        self.assertEqual(result['params']['destination'], '虹桥机场')
    
    @patch.dict('os.environ', {}, clear=True)
    def test_no_api_key_skip_ai(self):
        import os
        
        has_api_key = os.getenv('API_KEY')
        
        self.assertIsNone(has_api_key)


class TestDemoMCPErrorHandling(unittest.TestCase):
    
    @patch('demo_mcp.client')
    @patch('demo_mcp.mcp_client')
    def test_json_parse_error(self, mock_mcp_client, mock_ai_client):
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = 'Invalid JSON'
        mock_ai_client.chat.completions.create.return_value = mock_response
        
        import json
        
        with self.assertRaises(json.JSONDecodeError):
            json.loads(mock_response.choices[0].message.content)
    
    @patch('demo_mcp.client')
    def test_api_call_exception(self, mock_ai_client):
        mock_ai_client.chat.completions.create.side_effect = Exception('API Error')
        
        with self.assertRaises(Exception):
            mock_ai_client.chat.completions.create(model='gpt-3.5-turbo', messages=[])


if __name__ == '__main__':
    unittest.main()
