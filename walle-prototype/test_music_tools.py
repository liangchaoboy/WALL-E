#!/usr/bin/env python3
"""
Tests for music tools
"""

import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import parse_qs, urlparse, unquote

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp_servers_simple'))

from music_tools import play_music, search_playlist


class TestMusicTools(unittest.TestCase):
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_qq_success(self, mock_open):
        """测试QQ音乐播放功能"""
        mock_open.return_value = True
        
        result = play_music("晴天", "周杰伦", "qq")
        
        self.assertIn("已在qq音乐平台搜索", result)
        self.assertIn("周杰伦 晴天", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://y.qq.com/n/ryqq/search?w="))
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_netease_success(self, mock_open):
        """测试网易云音乐播放功能"""
        mock_open.return_value = True
        
        result = play_music("晴天", "周杰伦", "netease")
        
        self.assertIn("已在netease音乐平台搜索", result)
        self.assertIn("周杰伦 晴天", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://music.163.com/"))
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_spotify_success(self, mock_open):
        """测试Spotify播放功能"""
        mock_open.return_value = True
        
        result = play_music("Sunny Day", "Jay Chou", "spotify")
        
        self.assertIn("已在spotify音乐平台搜索", result)
        self.assertIn("Jay Chou Sunny Day", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://open.spotify.com/search/"))
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_without_artist(self, mock_open):
        """测试只提供歌曲名"""
        mock_open.return_value = True
        
        result = play_music("晴天", "", "qq")
        
        self.assertIn("已在qq音乐平台搜索", result)
        self.assertIn("晴天", result)
        
        mock_open.assert_called_once()
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_default_platform(self, mock_open):
        """测试默认平台(QQ音乐)"""
        mock_open.return_value = True
        
        result = play_music("晴天", "周杰伦")
        
        self.assertIn("qq", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://y.qq.com/"))
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_invalid_platform_defaults_to_qq(self, mock_open):
        """测试无效平台默认为QQ音乐"""
        mock_open.return_value = True
        
        result = play_music("晴天", "周杰伦", "invalid_platform")
        
        self.assertIn("invalid_platform", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://y.qq.com/"))
    
    def test_play_music_empty_song(self):
        """测试空歌曲名"""
        result = play_music("", "周杰伦", "qq")
        
        self.assertEqual(result, "错误: 歌曲名称不能为空")
    
    def test_play_music_whitespace_song(self):
        """测试纯空格歌曲名"""
        result = play_music("   ", "周杰伦", "qq")
        
        self.assertEqual(result, "错误: 歌曲名称不能为空")
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_url_encoding(self, mock_open):
        """测试URL编码"""
        mock_open.return_value = True
        
        play_music("七里香", "周杰伦", "qq")
        
        call_args = mock_open.call_args[0][0]
        # URL应该包含编码后的中文
        self.assertIn("%", call_args)
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_special_characters(self, mock_open):
        """测试特殊字符处理"""
        mock_open.return_value = True
        
        result = play_music("Rock & Roll", "Artist & Band", "qq")
        
        self.assertIn("已在qq音乐平台搜索", result)
        mock_open.assert_called_once()
    
    @patch('music_tools.webbrowser.open')
    def test_play_music_webbrowser_exception(self, mock_open):
        """测试浏览器打开失败"""
        mock_open.side_effect = Exception("Browser not found")
        
        result = play_music("晴天", "周杰伦", "qq")
        
        self.assertIn("失败", result)
        self.assertIn("Browser not found", result)
    
    @patch('music_tools.webbrowser.open')
    def test_search_playlist_qq_success(self, mock_open):
        """测试QQ音乐歌单搜索"""
        mock_open.return_value = True
        
        result = search_playlist("流行音乐", "qq")
        
        self.assertIn("已在qq搜索歌单", result)
        self.assertIn("流行音乐", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://y.qq.com/"))
        self.assertIn("playlist", call_args)
    
    @patch('music_tools.webbrowser.open')
    def test_search_playlist_netease_success(self, mock_open):
        """测试网易云歌单搜索"""
        mock_open.return_value = True
        
        result = search_playlist("流行音乐", "netease")
        
        self.assertIn("已在netease搜索歌单", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://music.163.com/"))
    
    @patch('music_tools.webbrowser.open')
    def test_search_playlist_spotify_success(self, mock_open):
        """测试Spotify歌单搜索"""
        mock_open.return_value = True
        
        result = search_playlist("Pop Music", "spotify")
        
        self.assertIn("已在spotify搜索歌单", result)
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertTrue(call_args.startswith("https://open.spotify.com/"))
        self.assertIn("playlist", call_args.lower())
    
    def test_search_playlist_empty_keyword(self):
        """测试空关键词"""
        result = search_playlist("", "qq")
        
        self.assertEqual(result, "错误: 搜索关键词不能为空")
    
    def test_search_playlist_whitespace_keyword(self):
        """测试纯空格关键词"""
        result = search_playlist("   ", "qq")
        
        self.assertEqual(result, "错误: 搜索关键词不能为空")
    
    @patch('music_tools.webbrowser.open')
    def test_search_playlist_default_platform(self, mock_open):
        """测试默认平台"""
        mock_open.return_value = True
        
        result = search_playlist("流行音乐")
        
        self.assertIn("qq", result)
        mock_open.assert_called_once()
    
    @patch('music_tools.webbrowser.open')
    def test_search_playlist_webbrowser_exception(self, mock_open):
        """测试浏览器打开失败"""
        mock_open.side_effect = Exception("Browser error")
        
        result = search_playlist("流行音乐", "qq")
        
        self.assertIn("失败", result)
        self.assertIn("Browser error", result)


class TestMusicURLEncoding(unittest.TestCase):
    """测试音乐工具的URL编码"""
    
    @patch('music_tools.webbrowser.open')
    def test_chinese_encoding(self, mock_open):
        """测试中文编码"""
        play_music("七里香", "周杰伦", "qq")
        
        call_args = mock_open.call_args[0][0]
        # 验证URL包含正确编码的中文
        parsed = urlparse(call_args)
        self.assertIn("w=", parsed.query)
    
    @patch('music_tools.webbrowser.open')
    def test_space_encoding(self, mock_open):
        """测试空格编码"""
        play_music("Bohemian Rhapsody", "Queen", "spotify")
        
        call_args = mock_open.call_args[0][0]
        # 空格应被编码
        self.assertIn("%20", call_args)
    
    @patch('music_tools.webbrowser.open')
    def test_special_char_encoding(self, mock_open):
        """测试特殊字符编码"""
        play_music("Rock&Roll", "Artist", "qq")
        
        call_args = mock_open.call_args[0][0]
        # &应被编码
        self.assertIn("%26", call_args)


class TestMusicEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    @patch('music_tools.webbrowser.open')
    def test_very_long_song_name(self, mock_open):
        """测试很长的歌曲名"""
        long_name = "这是一个非常非常非常非常非常非常长的歌曲名字" * 5
        result = play_music(long_name, "Artist", "qq")
        
        self.assertIn("已在qq音乐平台搜索", result)
        mock_open.assert_called_once()
    
    @patch('music_tools.webbrowser.open')
    def test_emoji_in_song_name(self, mock_open):
        """测试歌曲名包含emoji"""
        result = play_music("Happy Song 🎵", "Artist 🎤", "qq")
        
        self.assertIn("已在qq音乐平台搜索", result)
        mock_open.assert_called_once()
    
    @patch('music_tools.webbrowser.open')
    def test_numeric_song_name(self, mock_open):
        """测试纯数字歌曲名"""
        result = play_music("1989", "Taylor Swift", "spotify")
        
        self.assertIn("已在spotify音乐平台搜索", result)
        mock_open.assert_called_once()
    
    @patch('music_tools.webbrowser.open')
    def test_whitespace_trimming(self, mock_open):
        """测试空格修剪"""
        result = play_music("  晴天  ", "  周杰伦  ", "qq")
        
        self.assertIn("已在qq音乐平台搜索", result)
        # 验证确实调用了浏览器
        mock_open.assert_called_once()


if __name__ == '__main__':
    unittest.main()

