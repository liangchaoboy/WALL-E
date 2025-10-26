#!/usr/bin/env python3
"""
Test suite for MCP Client
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp_client import MCPClient, create_mcp_client


class TestMCPClient(unittest.TestCase):
    
    def setUp(self):
        self.client = MCPClient()
    
    def test_init(self):
        self.assertEqual(len(self.client.servers), 0)
        self.assertEqual(len(self.client.tools), 0)
    
    def test_register_server_success(self):
        mock_module = Mock()
        mock_mcp = Mock()
        mock_mcp._tools = {'test_tool': lambda: 'result'}
        mock_module.mcp = mock_mcp
        
        with patch('importlib.import_module', return_value=mock_module):
            self.client.register_server('test_server', '/path/to/server.py')
        
        self.assertIn('test_server', self.client.servers)
        self.assertIn('test_tool', self.client.tools)
        self.assertIn('test_server.test_tool', self.client.tools)
    
    def test_register_server_missing_mcp(self):
        mock_module = Mock(spec=[])
        
        with patch('importlib.import_module', return_value=mock_module):
            self.client.register_server('test_server', '/path/to/server.py')
        
        self.assertNotIn('test_server', self.client.servers)
    
    def test_register_server_import_error(self):
        with patch('importlib.import_module', side_effect=ImportError('Module not found')):
            self.client.register_server('test_server', '/path/to/server.py')
        
        self.assertNotIn('test_server', self.client.servers)
    
    def test_list_tools(self):
        self.client.tools = {
            'tool1': lambda: 'result1',
            'server.tool1': lambda: 'result1',
            'tool2': lambda: 'result2'
        }
        
        tools = self.client.list_tools()
        self.assertEqual(len(tools), 3)
        self.assertIn('tool1', tools)
        self.assertIn('tool2', tools)
    
    def test_call_tool_success(self):
        test_func = Mock(return_value='success')
        self.client.tools = {'test_tool': test_func}
        
        result = self.client.call_tool('test_tool', param1='value1')
        
        self.assertEqual(result, 'success')
        test_func.assert_called_once_with(param1='value1')
    
    def test_call_tool_not_found(self):
        self.client.tools = {'other_tool': lambda: 'result'}
        
        result = self.client.call_tool('missing_tool')
        
        self.assertIn('不存在', result)
        self.assertIn('missing_tool', result)
    
    def test_call_tool_exception(self):
        error_func = Mock(side_effect=ValueError('Invalid parameter'))
        self.client.tools = {'error_tool': error_func}
        
        result = self.client.call_tool('error_tool')
        
        self.assertIn('失败', result)
        self.assertIn('Invalid parameter', result)
    
    def test_get_tool_info_with_doc(self):
        def documented_tool():
            """This is a test tool"""
            return 'result'
        
        self.client.tools = {'doc_tool': documented_tool}
        
        info = self.client.get_tool_info('doc_tool')
        self.assertEqual(info, 'This is a test tool')
    
    def test_get_tool_info_without_doc(self):
        self.client.tools = {'no_doc_tool': lambda: 'result'}
        
        info = self.client.get_tool_info('no_doc_tool')
        self.assertEqual(info, 'No documentation available')
    
    def test_get_tool_info_not_found(self):
        info = self.client.get_tool_info('missing_tool')
        self.assertIsNone(info)


class TestCreateMCPClient(unittest.TestCase):
    
    @patch('mcp_client.Path')
    @patch('mcp_client.MCPClient')
    def test_create_with_default_dir(self, mock_client_class, mock_path):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_servers_dir = Mock()
        mock_path.return_value.parent = Mock()
        mock_path.return_value.parent.__truediv__ = Mock(return_value=mock_servers_dir)
        
        nav_path = Mock()
        nav_path.exists.return_value = True
        weather_path = Mock()
        weather_path.exists.return_value = True
        music_path = Mock()
        music_path.exists.return_value = False
        
        mock_servers_dir.__truediv__ = Mock(side_effect=[nav_path, weather_path, music_path])
        
        result = create_mcp_client()
        
        self.assertEqual(result, mock_client)
        self.assertEqual(mock_client.register_server.call_count, 2)
    
    @patch('mcp_client.Path')
    @patch('mcp_client.MCPClient')
    def test_create_with_custom_dir(self, mock_client_class, mock_path):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        custom_dir = '/custom/servers'
        
        result = create_mcp_client(servers_dir=custom_dir)
        
        self.assertEqual(result, mock_client)
        mock_path.assert_called_with(custom_dir)


if __name__ == '__main__':
    unittest.main()
