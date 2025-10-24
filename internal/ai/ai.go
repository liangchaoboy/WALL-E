package ai

import (
	"context"
	"fmt"
)

// Provider 定义 AI 提供商类型
type Provider string

const (
	ProviderChatGPT  Provider = "chatgpt"
	ProviderClaude   Provider = "claude"
	ProviderDeepSeek Provider = "deepseek"
)

// Client 定义 AI 客户端接口
type Client interface {
	// ExtractNavigationIntent 从用户输入中提取导航意图
	ExtractNavigationIntent(ctx context.Context, text string) (*NavigationIntent, error)

	// GetProviderName 获取提供商名称
	GetProviderName() string
}

// NavigationIntent 导航意图结构
type NavigationIntent struct {
	Start string `json:"start"` // 起点
	End   string `json:"end"`   // 终点
}

// Config AI 配置
type Config struct {
	Provider Provider `json:"provider"`
	APIKey   string   `json:"api_key"`
	Model    string   `json:"model"`
	BaseURL  string   `json:"base_url"`
}

// NewClient 创建 AI 客户端
func NewClient(config Config) (Client, error) {
	switch config.Provider {
	case ProviderChatGPT:
		return NewChatGPTClient(config)
	case ProviderClaude:
		return NewClaudeClient(config)
	case ProviderDeepSeek:
		return NewDeepSeekClient(config)
	default:
		return nil, fmt.Errorf("不支持的 AI 提供商: %s", config.Provider)
	}
}
