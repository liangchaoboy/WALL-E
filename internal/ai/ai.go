package ai

import (
	"context"
	"fmt"
	"strings"
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

// CleanJSONContent 清理 AI 返回的内容，移除 Markdown 格式
func CleanJSONContent(content string) string {
	// 移除 ```json 和 ``` 标记
	content = strings.TrimSpace(content)

	// 处理 ```json ... ``` 格式
	if strings.HasPrefix(content, "```json") {
		content = strings.TrimPrefix(content, "```json")
		content = strings.TrimSuffix(content, "```")
		content = strings.TrimSpace(content)
	}

	// 处理 ``` ... ``` 格式
	if strings.HasPrefix(content, "```") {
		content = strings.TrimPrefix(content, "```")
		content = strings.TrimSuffix(content, "```")
		content = strings.TrimSpace(content)
	}

	// 移除可能的其他前缀
	prefixes := []string{"json", "JSON", "```json", "```"}
	for _, prefix := range prefixes {
		if strings.HasPrefix(content, prefix) {
			content = strings.TrimPrefix(content, prefix)
			content = strings.TrimSpace(content)
		}
	}

	return content
}
