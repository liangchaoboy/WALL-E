#!/usr/bin/env python3
"""
Tests for navigation tools
"""

import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import parse_qs, urlparse

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp_servers_simple'))

from navigation_tools import (
    navigate, 
    search_location, 
    _extract_city_name,
    _generate_baidu_url,
    _generate_amap_url,
    _generate_google_url
)


class TestNavigationTools(unittest.TestCase):
    
    def test_extract_city_name_major_cities(self):
        self.assertEqual(_extract_city_name("北京天安门"), "北京")
        self.assertEqual(_extract_city_name("上海东方明珠"), "上海")
        self.assertEqual(_extract_city_name("深圳"), "深圳")
        self.assertEqual(_extract_city_name("杭州西湖"), "杭州")
    
    def test_extract_city_name_short_address(self):
        self.assertEqual(_extract_city_name("北京"), "北京")
        self.assertEqual(_extract_city_name("上海"), "上海")
    
    def test_extract_city_name_unknown_city(self):
        self.assertEqual(_extract_city_name("某个不知名的地方"), "全国")
    
    def test_generate_baidu_url_encoding(self):
        url = _generate_baidu_url("上海", "北京")
        
        self.assertTrue(url.startswith("https://map.baidu.com/"))
        
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # 新的URL格式使用direction端点
        self.assertIn('origin', params)
        self.assertIn('destination', params)
        # 参数应该是URL编码后的值
        self.assertIn("上海", params['origin'][0])
        self.assertIn("北京", params['destination'][0])
    
    def test_generate_baidu_url_with_special_chars(self):
        url = _generate_baidu_url("上海浦东机场", "北京首都机场T3")
        
        self.assertTrue(url.startswith("https://map.baidu.com/"))
        
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # 验证URL格式正确
        self.assertIn('origin', params)
        self.assertIn('destination', params)
        decoded_origin = params['origin'][0]
        decoded_dest = params['destination'][0]
        self.assertIn("浦东机场", decoded_origin)
        self.assertIn("首都机场", decoded_dest)
    
    def test_generate_amap_url(self):
        url = _generate_amap_url("上海", "北京")
        
        self.assertTrue(url.startswith("https://www.amap.com/dir?"))
        
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        self.assertEqual(params['from'][0], "上海")
        self.assertEqual(params['to'][0], "北京")
    
    def test_generate_google_url(self):
        url = _generate_google_url("Shanghai", "Beijing")
        
        self.assertTrue(url.startswith("https://www.google.com/maps/dir/?"))
        
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        self.assertEqual(params['api'][0], "1")
        self.assertEqual(params['origin'][0], "Shanghai")
        self.assertEqual(params['destination'][0], "Beijing")
        self.assertEqual(params['travelmode'][0], "transit")
    
    @patch('navigation_tools.webbrowser.open')
    def test_navigate_baidu_success(self, mock_open):
        mock_open.return_value = True
        
        result = navigate("上海", "北京", "baidu")
        
        self.assertIn("✅ 成功打开 百度地图", result)
        self.assertIn("📍 起点：上海", result)
        self.assertIn("📍 终点：北京", result)
        self.assertIn("🔗 导航链接：", result)
        self.assertIn("地图应用已在浏览器中打开", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://map.baidu.com/"))
        # 验证URL不包含双重编码
        self.assertNotIn("%25", call_args)
    
    @patch('navigation_tools.webbrowser.open')
    def test_navigate_amap_success(self, mock_open):
        mock_open.return_value = True
        
        result = navigate("上海", "北京", "amap")
        
        self.assertIn("✅ 成功打开 高德地图", result)
        self.assertIn("上海", result)
        self.assertIn("北京", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://www.amap.com/dir?"))
    
    @patch('navigation_tools.webbrowser.open')
    def test_navigate_google_success(self, mock_open):
        mock_open.return_value = True
        
        result = navigate("Shanghai", "Beijing", "google")
        
        self.assertIn("✅ 成功打开 Google Maps", result)
        self.assertIn("Shanghai", result)
        self.assertIn("Beijing", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://www.google.com/maps/dir/?"))
    
    @patch('navigation_tools.webbrowser.open')
    def test_navigate_default_to_baidu(self, mock_open):
        mock_open.return_value = True
        
        result = navigate("上海", "北京")
        
        self.assertIn("百度地图", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://map.baidu.com/"))
        # 验证URL不包含双重编码
        self.assertNotIn("%25", call_args)
    
    @patch('navigation_tools.webbrowser.open')
    def test_navigate_invalid_service_defaults_to_baidu(self, mock_open):
        mock_open.return_value = True
        
        result = navigate("上海", "北京", "invalid_service")
        
        self.assertIn("百度地图", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://map.baidu.com/"))
        # 验证URL不包含双重编码
        self.assertNotIn("%25", call_args)
    
    def test_navigate_empty_origin(self):
        result = navigate("", "北京", "baidu")
        
        self.assertEqual(result, "错误: 起点和终点不能为空")
    
    def test_navigate_empty_destination(self):
        result = navigate("上海", "", "baidu")
        
        self.assertEqual(result, "错误: 起点和终点不能为空")
    
    def test_navigate_both_empty(self):
        result = navigate("", "", "baidu")
        
        self.assertEqual(result, "错误: 起点和终点不能为空")
    
    @patch('navigation_tools.webbrowser.open')
    def test_navigate_webbrowser_exception(self, mock_open):
        mock_open.side_effect = Exception("Browser not found")
        
        result = navigate("上海", "北京", "baidu")
        
        self.assertIn("打开地图失败", result)
        self.assertIn("Browser not found", result)
    
    @patch('navigation_tools.webbrowser.open')
    def test_search_location_baidu_success(self, mock_open):
        mock_open.return_value = True
        
        result = search_location("虹桥机场", "baidu")
        
        self.assertIn("✅ 已在百度地图搜索: 虹桥机场", result)
        self.assertIn("🔗", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://map.baidu.com/?query="))
    
    @patch('navigation_tools.webbrowser.open')
    def test_search_location_amap_success(self, mock_open):
        mock_open.return_value = True
        
        result = search_location("虹桥机场", "amap")
        
        self.assertIn("✅ 已在高德地图搜索: 虹桥机场", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://www.amap.com/search?query="))
    
    @patch('navigation_tools.webbrowser.open')
    def test_search_location_google_success(self, mock_open):
        mock_open.return_value = True
        
        result = search_location("Hongqiao Airport", "google")
        
        self.assertIn("✅ 已在Google Maps搜索: Hongqiao Airport", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://www.google.com/maps/search/"))
    
    @patch('navigation_tools.webbrowser.open')
    def test_search_location_with_special_chars(self, mock_open):
        mock_open.return_value = True
        
        result = search_location("上海 浦东机场", "baidu")
        
        self.assertIn("✅", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertIn("%20", call_args)
    
    def test_search_location_empty_query(self):
        result = search_location("", "baidu")
        
        self.assertEqual(result, "错误: 搜索关键词不能为空")
    
    @patch('navigation_tools.webbrowser.open')
    def test_search_location_webbrowser_exception(self, mock_open):
        mock_open.side_effect = Exception("Browser not found")
        
        result = search_location("虹桥机场", "baidu")
        
        self.assertIn("打开地图搜索失败", result)
        self.assertIn("Browser not found", result)


class TestURLEncoding(unittest.TestCase):
    
    def test_baidu_url_proper_encoding(self):
        url = _generate_baidu_url("上海浦东", "北京 朝阳")
        
        self.assertTrue(url.startswith("https://map.baidu.com/"))
        
        # 验证URL不包含双重编码
        # 双重编码会显示为 %25XX (百分号被再次编码)
        self.assertNotIn("%25", url)
    
    def test_urls_with_emoji(self):
        url = _generate_baidu_url("起点🚀", "终点✈️")
        
        self.assertTrue(url.startswith("https://map.baidu.com/"))
        
        # 验证URL格式正确且不包含双重编码
        self.assertNotIn("%25", url)


if __name__ == '__main__':
    unittest.main()
