#!/usr/bin/env python3
"""
Test suite for SimpleMCPClient
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp_client_simple import SimpleMCPClient, create_simple_mcp_client


class TestSimpleMCPClient(unittest.TestCase):
    
    def setUp(self):
        self.client = SimpleMCPClient()
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(len(self.client.tools), 0)
    
    def test_register_tools_module_success(self):
        """测试成功注册工具模块"""
        mock_module = Mock()
        mock_module.TOOLS = {
            'test_tool': lambda: 'result',
            'another_tool': lambda: 'another_result'
        }
        
        with patch('importlib.import_module', return_value=mock_module):
            self.client.register_tools_module('test_module', '/path/to/module.py')
        
        self.assertEqual(len(self.client.tools), 2)
        self.assertIn('test_tool', self.client.tools)
        self.assertIn('another_tool', self.client.tools)
    
    def test_register_tools_module_missing_tools(self):
        """测试模块缺少TOOLS字典"""
        mock_module = Mock(spec=[])
        
        with patch('importlib.import_module', return_value=mock_module):
            self.client.register_tools_module('test_module', '/path/to/module.py')
        
        self.assertEqual(len(self.client.tools), 0)
    
    def test_register_tools_module_import_error(self):
        """测试导入错误"""
        with patch('importlib.import_module', side_effect=ImportError('Module not found')):
            self.client.register_tools_module('test_module', '/path/to/module.py')
        
        self.assertEqual(len(self.client.tools), 0)
    
    def test_list_tools(self):
        """测试列出所有工具"""
        self.client.tools = {
            'tool1': lambda: 'result1',
            'tool2': lambda: 'result2',
            'tool3': lambda: 'result3'
        }
        
        tools = self.client.list_tools()
        self.assertEqual(len(tools), 3)
        self.assertIn('tool1', tools)
        self.assertIn('tool2', tools)
        self.assertIn('tool3', tools)
    
    def test_call_tool_success(self):
        """测试成功调用工具"""
        test_func = Mock(return_value='success')
        self.client.tools = {'test_tool': test_func}
        
        result = self.client.call_tool('test_tool', param1='value1', param2='value2')
        
        self.assertEqual(result, 'success')
        test_func.assert_called_once_with(param1='value1', param2='value2')
    
    def test_call_tool_not_found(self):
        """测试调用不存在的工具"""
        self.client.tools = {'other_tool': lambda: 'result'}
        
        result = self.client.call_tool('missing_tool')
        
        self.assertIn('不存在', result)
        self.assertIn('missing_tool', result)
    
    def test_call_tool_exception(self):
        """测试工具执行异常"""
        error_func = Mock(side_effect=ValueError('Invalid parameter'))
        self.client.tools = {'error_tool': error_func}
        
        result = self.client.call_tool('error_tool', param='value')
        
        self.assertIn('失败', result)
        self.assertIn('Invalid parameter', result)
    
    def test_get_tool_info_with_doc(self):
        """测试获取有文档的工具信息"""
        def documented_tool():
            """这是一个测试工具"""
            return 'result'
        
        self.client.tools = {'doc_tool': documented_tool}
        
        info = self.client.get_tool_info('doc_tool')
        self.assertEqual(info, '这是一个测试工具')
    
    def test_get_tool_info_without_doc(self):
        """测试获取无文档的工具信息"""
        self.client.tools = {'no_doc_tool': lambda: 'result'}
        
        info = self.client.get_tool_info('no_doc_tool')
        self.assertEqual(info, '无文档')
    
    def test_get_tool_info_not_found(self):
        """测试获取不存在工具的信息"""
        info = self.client.get_tool_info('missing_tool')
        self.assertIsNone(info)
    
    def test_call_tool_with_no_params(self):
        """测试不带参数调用工具"""
        test_func = Mock(return_value='no_params')
        self.client.tools = {'test_tool': test_func}
        
        result = self.client.call_tool('test_tool')
        
        self.assertEqual(result, 'no_params')
        test_func.assert_called_once_with()
    
    def test_call_tool_with_kwargs(self):
        """测试使用关键字参数调用工具"""
        test_func = Mock(return_value='with_kwargs')
        self.client.tools = {'test_tool': test_func}
        
        result = self.client.call_tool('test_tool', key1='val1', key2='val2')
        
        self.assertEqual(result, 'with_kwargs')
        test_func.assert_called_once_with(key1='val1', key2='val2')


class TestCreateSimpleMCPClient(unittest.TestCase):
    
    @patch('mcp_client_simple.Path')
    def test_create_with_default_dir(self, mock_path):
        """测试使用默认目录创建客户端"""
        mock_tools_dir = Mock()
        mock_path.return_value.parent = Mock()
        mock_path.return_value.parent.__truediv__ = Mock(return_value=mock_tools_dir)
        
        # Mock file existence
        nav_path = Mock()
        nav_path.exists.return_value = True
        weather_path = Mock()
        weather_path.exists.return_value = True
        music_path = Mock()
        music_path.exists.return_value = True
        
        mock_tools_dir.__truediv__ = Mock(side_effect=[nav_path, weather_path, music_path])
        
        with patch.object(SimpleMCPClient, 'register_tools_module') as mock_register:
            client = create_simple_mcp_client()
            
            # Should register 3 modules
            self.assertEqual(mock_register.call_count, 3)
    
    @patch('mcp_client_simple.Path')
    def test_create_with_custom_dir(self, mock_path):
        """测试使用自定义目录创建客户端"""
        custom_dir = '/custom/tools'
        
        with patch.object(SimpleMCPClient, 'register_tools_module'):
            client = create_simple_mcp_client(tools_dir=custom_dir)
            
            # Verify custom path was used
            mock_path.assert_called_with(custom_dir)
    
    @patch('mcp_client_simple.Path')
    def test_create_with_missing_files(self, mock_path):
        """测试某些文件不存在的情况"""
        mock_tools_dir = Mock()
        mock_path.return_value.parent = Mock()
        mock_path.return_value.parent.__truediv__ = Mock(return_value=mock_tools_dir)
        
        # Only navigation exists
        nav_path = Mock()
        nav_path.exists.return_value = True
        weather_path = Mock()
        weather_path.exists.return_value = False
        music_path = Mock()
        music_path.exists.return_value = False
        
        mock_tools_dir.__truediv__ = Mock(side_effect=[nav_path, weather_path, music_path])
        
        with patch.object(SimpleMCPClient, 'register_tools_module') as mock_register:
            client = create_simple_mcp_client()
            
            # Should only register navigation
            self.assertEqual(mock_register.call_count, 1)


class TestSimpleMCPClientIntegration(unittest.TestCase):
    """集成测试 - 测试与实际工具模块的集成"""
    
    def test_load_actual_tools(self):
        """测试加载实际的工具模块"""
        client = create_simple_mcp_client()
        
        # Verify tools are loaded
        tools = client.list_tools()
        self.assertGreater(len(tools), 0, "Should have loaded some tools")
        
        # Check for expected tools
        expected_tools = ['navigate', 'search_location', 'get_weather', 
                         'compare_weather', 'play_music', 'search_playlist']
        
        for tool in expected_tools:
            self.assertIn(tool, tools, f"Expected tool '{tool}' not found")
    
    @patch('mcp_servers_simple.navigation_tools.webbrowser.open')
    def test_call_actual_navigate_tool(self, mock_open):
        """测试实际调用导航工具"""
        mock_open.return_value = True
        client = create_simple_mcp_client()
        
        result = client.call_tool('navigate', origin='上海', destination='北京')
        
        self.assertIn('成功', result)
        self.assertIn('上海', result)
        self.assertIn('北京', result)
        mock_open.assert_called_once()
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_call_actual_weather_tool(self, mock_open):
        """测试实际调用天气工具"""
        mock_open.return_value = True
        client = create_simple_mcp_client()
        
        result = client.call_tool('get_weather', city='上海', date='明天')
        
        self.assertIn('上海', result)
        self.assertIn('明天', result)
        mock_open.assert_called_once()
    
    @patch('mcp_servers_simple.music_tools.webbrowser.open')
    def test_call_actual_music_tool(self, mock_open):
        """测试实际调用音乐工具"""
        mock_open.return_value = True
        client = create_simple_mcp_client()
        
        result = client.call_tool('play_music', song='晴天', artist='周杰伦')
        
        self.assertIn('晴天', result)
        self.assertIn('周杰伦', result)
        mock_open.assert_called_once()
    
    def test_tool_info_available(self):
        """测试工具信息可用"""
        client = create_simple_mcp_client()
        
        info = client.get_tool_info('navigate')
        self.assertIsNotNone(info)
        self.assertNotEqual(info, '无文档')
    
    def test_error_handling(self):
        """测试错误处理"""
        client = create_simple_mcp_client()
        
        # Call with missing required parameter
        result = client.call_tool('navigate', origin='上海')
        
        # Should return error message, not raise exception
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()

