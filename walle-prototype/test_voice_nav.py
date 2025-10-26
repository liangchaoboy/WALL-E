#!/usr/bin/env python3
"""
Test suite for voice_nav.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


class TestVoiceNav(unittest.TestCase):
    
    @patch('voice_nav.sr.Recognizer')
    @patch('voice_nav.sr.Microphone')
    def test_listen_success(self, mock_mic, mock_recognizer_class):
        from voice_nav import listen
        
        mock_recognizer = Mock()
        mock_recognizer_class.return_value = mock_recognizer
        
        mock_audio = Mock()
        mock_recognizer.listen.return_value = mock_audio
        mock_recognizer.recognize_google.return_value = '从上海到北京'
        
        result = listen()
        
        self.assertEqual(result, '从上海到北京')
        mock_recognizer.listen.assert_called_once()
        mock_recognizer.recognize_google.assert_called_once_with(mock_audio, language='zh-CN')
    
    @patch('voice_nav.sr.Recognizer')
    @patch('voice_nav.sr.Microphone')
    def test_listen_timeout(self, mock_mic, mock_recognizer_class):
        from voice_nav import listen
        import speech_recognition as sr
        
        mock_recognizer = Mock()
        mock_recognizer_class.return_value = mock_recognizer
        mock_recognizer.listen.side_effect = sr.WaitTimeoutError()
        
        result = listen()
        
        self.assertIsNone(result)
    
    @patch('voice_nav.sr.Recognizer')
    @patch('voice_nav.sr.Microphone')
    def test_listen_unknown_value(self, mock_mic, mock_recognizer_class):
        from voice_nav import listen
        import speech_recognition as sr
        
        mock_recognizer = Mock()
        mock_recognizer_class.return_value = mock_recognizer
        
        mock_audio = Mock()
        mock_recognizer.listen.return_value = mock_audio
        mock_recognizer.recognize_google.side_effect = sr.UnknownValueError()
        
        result = listen()
        
        self.assertIsNone(result)
    
    @patch('voice_nav.client')
    def test_understand_navigation(self, mock_client):
        from voice_nav import understand
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"action":"nav","from":"上海","to":"北京"}'
        mock_client.chat.completions.create.return_value = mock_response
        
        result = understand('从上海到北京')
        
        self.assertEqual(result['action'], 'nav')
        self.assertEqual(result['from'], '上海')
        self.assertEqual(result['to'], '北京')
    
    @patch('voice_nav.client')
    def test_understand_unknown(self, mock_client):
        from voice_nav import understand
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"action":"unknown"}'
        mock_client.chat.completions.create.return_value = mock_response
        
        result = understand('今天天气怎么样')
        
        self.assertEqual(result['action'], 'unknown')
    
    @patch('voice_nav.client')
    def test_understand_exception(self, mock_client):
        from voice_nav import understand
        
        mock_client.chat.completions.create.side_effect = Exception('API Error')
        
        result = understand('测试')
        
        self.assertEqual(result['action'], 'unknown')
    
    @patch('voice_nav.webbrowser.open')
    def test_navigate(self, mock_open):
        from voice_nav import navigate
        
        navigate('上海', '北京')
        
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        self.assertIn('上海', call_args)
        self.assertIn('北京', call_args)
        self.assertIn('baidu.com', call_args)


class TestVoiceNavMain(unittest.TestCase):
    
    @patch('voice_nav.listen')
    @patch('voice_nav.understand')
    @patch('voice_nav.navigate')
    def test_main_navigation_flow(self, mock_navigate, mock_understand, mock_listen):
        from voice_nav import main
        
        mock_listen.side_effect = ['从上海到北京', '退出']
        mock_understand.return_value = {'action': 'nav', 'from': '上海', 'to': '北京'}
        
        main()
        
        self.assertEqual(mock_listen.call_count, 2)
        mock_understand.assert_called_once_with('从上海到北京')
        mock_navigate.assert_called_once_with('上海', '北京')
    
    @patch('voice_nav.listen')
    @patch('voice_nav.understand')
    @patch('voice_nav.navigate')
    def test_main_unknown_action(self, mock_navigate, mock_understand, mock_listen):
        from voice_nav import main
        
        mock_listen.side_effect = ['播放音乐', '退出']
        mock_understand.return_value = {'action': 'unknown'}
        
        main()
        
        self.assertEqual(mock_listen.call_count, 2)
        mock_navigate.assert_not_called()
    
    @patch('voice_nav.listen')
    def test_main_no_text(self, mock_listen):
        from voice_nav import main
        
        mock_listen.side_effect = [None, '退出']
        
        main()
        
        self.assertEqual(mock_listen.call_count, 2)


if __name__ == '__main__':
    unittest.main()
