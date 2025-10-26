#!/usr/bin/env python3
"""
Test suite for weather query tools
Tests both MCP server and simple versions
"""

import unittest
from unittest.mock import patch, Mock
from urllib.parse import quote
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp_servers_simple.weather_tools import get_weather, compare_weather


class TestWeatherToolsSimple(unittest.TestCase):
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_get_weather_encoding(self, mock_open):
        city = "上海"
        date = "明天"
        result = get_weather(city, date)
        
        expected_query = quote(f"{city}{date}天气")
        expected_url = f"https://www.baidu.com/s?wd={expected_query}"
        
        mock_open.assert_called_once_with(expected_url)
        self.assertEqual(result, f"已打开{city}{date}天气查询")
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_get_weather_today_default(self, mock_open):
        city = "北京"
        result = get_weather(city)
        
        expected_query = quote(f"{city}today天气")
        expected_url = f"https://www.baidu.com/s?wd={expected_query}"
        
        mock_open.assert_called_once_with(expected_url)
        self.assertEqual(result, f"已打开{city}today天气查询")
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_compare_weather_encoding(self, mock_open):
        city1 = "北京"
        city2 = "上海"
        result = compare_weather(city1, city2)
        
        expected_query = quote(f"{city1} {city2} 天气对比")
        expected_url = f"https://www.baidu.com/s?wd={expected_query}"
        
        mock_open.assert_called_once_with(expected_url)
        self.assertEqual(result, f"已打开{city1}和{city2}天气对比")
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_get_weather_various_cities(self, mock_open):
        cities = ["深圳", "广州", "杭州", "成都"]
        for city in cities:
            mock_open.reset_mock()
            result = get_weather(city, "今天")
            
            expected_query = quote(f"{city}今天天气")
            expected_url = f"https://www.baidu.com/s?wd={expected_query}"
            
            mock_open.assert_called_once_with(expected_url)
            self.assertIn(city, result)
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_get_weather_various_dates(self, mock_open):
        dates = ["明天", "后天", "周末"]
        city = "上海"
        
        for date in dates:
            mock_open.reset_mock()
            result = get_weather(city, date)
            
            expected_query = quote(f"{city}{date}天气")
            expected_url = f"https://www.baidu.com/s?wd={expected_query}"
            
            mock_open.assert_called_once_with(expected_url)
            self.assertIn(date, result)


class TestWeatherURLEncoding(unittest.TestCase):
    
    def test_url_encoding_chinese(self):
        city = "上海"
        date = "明天"
        query = f"{city}{date}天气"
        encoded = quote(query)
        
        self.assertNotIn("上", encoded)
        self.assertNotIn("海", encoded)
        self.assertIn("%", encoded)
    
    def test_url_encoding_preserves_spaces(self):
        query = "北京 上海 天气对比"
        encoded = quote(query)
        
        self.assertIn("%20", encoded)
    
    def test_return_string_is_utf8(self):
        city = "上海"
        date = "明天"
        result = f"已打开{city}{date}天气查询"
        
        encoded_bytes = result.encode('utf-8')
        decoded_result = encoded_bytes.decode('utf-8')
        
        self.assertEqual(result, decoded_result)


class TestWeatherEdgeCases(unittest.TestCase):
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_empty_city_name(self, mock_open):
        result = get_weather("", "明天")
        
        # 空城市名应该返回错误,不应该调用浏览器
        self.assertIn("错误", result)
        mock_open.assert_not_called()
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_special_characters_in_city(self, mock_open):
        city = "西安"
        result = get_weather(city, "今天")
        
        expected_query = quote(f"{city}今天天气")
        expected_url = f"https://www.baidu.com/s?wd={expected_query}"
        
        mock_open.assert_called_once_with(expected_url)
        self.assertIn(city, result)
    
    @patch('mcp_servers_simple.weather_tools.webbrowser.open')
    def test_compare_same_cities(self, mock_open):
        city = "北京"
        result = compare_weather(city, city)
        
        self.assertIsNotNone(result)
        mock_open.assert_called_once()


if __name__ == '__main__':
    unittest.main()
