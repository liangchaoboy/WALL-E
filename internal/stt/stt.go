package stt

import (
	"context"
	"fmt"
	"io"
)

// Provider STT 提供商类型
type Provider string

const (
	// ProviderOpenAI OpenAI Whisper API
	ProviderOpenAI Provider = "openai"
	// ProviderLocal 本地 STT（降级方案）
	ProviderLocal Provider = "local"
	// ProviderAliyun 阿里云实时语音识别
	ProviderAliyun Provider = "aliyun"
	// ProviderAuto 自动选择（优先 AI，失败后降级本地）
	ProviderAuto Provider = "auto"
)

// Result STT 结果
type Result struct {
	Text     string   `json:"text"`     // 转换的文字
	Language string   `json:"language"` // 识别的语言
	Provider Provider `json:"provider"` // 使用的提供商
}

// Client STT 客户端接口
type Client interface {
	// TranscribeAudio 转录音频为文字
	// audio: 音频数据流
	// format: 音频格式（如 "mp3", "wav", "webm"）
	TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*Result, error)

	// GetProviderName 获取提供商名称
	GetProviderName() string
}

// Config STT 配置
type Config struct {
	Provider Provider `json:"provider"` // STT 提供商

	// OpenAI Whisper 配置
	OpenAIKey string `json:"openai_key"` // OpenAI API Key
	Model     string `json:"model"`      // 模型名称（whisper-1）

	// 阿里云语音识别配置
	AliyunAPIKey string `json:"aliyun_api_key"` // 阿里云 API Key
	AliyunModel  string `json:"aliyun_model"`   // 阿里云模型名称

	// 本地 STT 配置
	LocalModelPath string `json:"local_model_path"` // 本地模型路径

	// 降级配置
	EnableFallback bool `json:"enable_fallback"` // 启用降级（AI失败后用本地）
}

// NewClient 创建 STT 客户端
func NewClient(config Config) (Client, error) {
	switch config.Provider {
	case ProviderOpenAI:
		return NewOpenAIClient(config)
	case ProviderLocal:
		return NewLocalClient(config)
	case ProviderAliyun:
		return NewAliyunClient(config)
	case ProviderAuto:
		return NewAutoClient(config)
	default:
		return nil, fmt.Errorf("不支持的 STT 提供商: %s", config.Provider)
	}
}

// AutoClient 自动降级客户端
type AutoClient struct {
	primaryClient  Client // 主客户端（AI）
	fallbackClient Client // 降级客户端（本地）
	enableFallback bool
}

// NewAutoClient 创建自动降级客户端
func NewAutoClient(config Config) (*AutoClient, error) {
	// 创建主客户端（OpenAI Whisper）
	primaryConfig := config
	primaryConfig.Provider = ProviderOpenAI
	primaryClient, err := NewOpenAIClient(primaryConfig)
	if err != nil {
		return nil, fmt.Errorf("创建 OpenAI 客户端失败: %w", err)
	}

	// 创建降级客户端（本地）
	var fallbackClient Client
	if config.EnableFallback {
		fallbackConfig := config
		fallbackConfig.Provider = ProviderLocal
		fallbackClient, err = NewLocalClient(fallbackConfig)
		if err != nil {
			// 本地客户端创建失败不是致命错误
			fmt.Printf("警告: 创建本地 STT 客户端失败: %v\n", err)
		}
	}

	return &AutoClient{
		primaryClient:  primaryClient,
		fallbackClient: fallbackClient,
		enableFallback: config.EnableFallback && fallbackClient != nil,
	}, nil
}

// TranscribeAudio 转录音频（自动降级）
func (c *AutoClient) TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*Result, error) {
	// 尝试使用主客户端（OpenAI）
	result, err := c.primaryClient.TranscribeAudio(ctx, audio, format)
	if err == nil {
		return result, nil
	}

	// 如果启用降级且有降级客户端
	if c.enableFallback && c.fallbackClient != nil {
		fmt.Printf("OpenAI STT 失败，降级到本地处理: %v\n", err)
		return c.fallbackClient.TranscribeAudio(ctx, audio, format)
	}

	return nil, fmt.Errorf("STT 转录失败: %w", err)
}

// GetProviderName 获取提供商名称
func (c *AutoClient) GetProviderName() string {
	if c.enableFallback && c.fallbackClient != nil {
		return "Auto (OpenAI → Local)"
	}
	return "Auto (OpenAI only)"
}
