#!/usr/bin/env python3
"""
WALL-E 日志配置模块
提供统一的日志配置和格式化
"""

import logging
import sys
from typing import Optional

def setup_logger(
    name: str = "WALL-E",
    level: str = "INFO",
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    配置并返回 logger 实例
    
    Args:
        name: Logger 名称
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: 自定义格式字符串
        
    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(
        format_string,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str = "WALL-E") -> logging.Logger:
    """
    获取已配置的 logger 实例
    
    Args:
        name: Logger 名称
        
    Returns:
        Logger 实例
    """
    return logging.getLogger(name)
