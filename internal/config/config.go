package config
package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

// Config 应用配置
type Config struct {
	Server ServerConfig `yaml:"server"`
	STT    STTConfig    `yaml:"stt"`
	AI     AIConfig     `yaml:"ai"`
	Map    MapConfig    `yaml:"map"`
}

// ServerConfig HTTP 服务器配置
type ServerConfig struct {
	Port int    `yaml:"port"`
	Host string `yaml:"host"`
}

// STTConfig STT 配置
type STTConfig struct {
	Provider       string `yaml:"provider"`        // auto, openai, local
	OpenAIKey      string `yaml:"openai_key"`
	Model          string `yaml:"model"`
	EnableFallback bool   `yaml:"enable_fallback"`
	LocalModelPath string `yaml:"local_model_path"`
}

// AIConfig AI 配置
type AIConfig struct {
	DefaultProvider string            `yaml:"default_provider"` // chatgpt, claude, deepseek
	ChatGPT         AIProviderConfig  `yaml:"chatgpt"`
	Claude          AIProviderConfig  `yaml:"claude"`
	DeepSeek        AIProviderConfig  `yaml:"deepseek"`
}

// AIProviderConfig AI 提供商配置
type AIProviderConfig struct {
	APIKey  string `yaml:"api_key"`
	Model   string `yaml:"model"`
	BaseURL string `yaml:"base_url"`
}

// MapConfig 地图配置
type MapConfig struct {
	DefaultProvider string `yaml:"default_provider"` // baidu, amap, google
}

// Load 加载配置文件
func Load(path string) (*Config, error) {
	// 读取配置文件
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("读取配置文件失败: %w", err)
	}

	// 解析 YAML
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("解析配置文件失败: %w", err)
	}

	// 处理环境变量
	cfg.processEnvVars()

	// 验证配置
	if err := cfg.Validate(); err != nil {
		return nil, fmt.Errorf("配置验证失败: %w", err)
	}

	return &cfg, nil
}

// processEnvVars 处理环境变量
func (c *Config) processEnvVars() {
	// STT OpenAI Key
	if c.STT.OpenAIKey != "" && c.STT.OpenAIKey[0] == '$' {
		c.STT.OpenAIKey = os.Getenv(c.STT.OpenAIKey[2 : len(c.STT.OpenAIKey)-1])
	}

	// AI ChatGPT
	if c.AI.ChatGPT.APIKey != "" && c.AI.ChatGPT.APIKey[0] == '$' {
		c.AI.ChatGPT.APIKey = os.Getenv(c.AI.ChatGPT.APIKey[2 : len(c.AI.ChatGPT.APIKey)-1])
	}

	// AI Claude
	if c.AI.Claude.APIKey != "" && c.AI.Claude.APIKey[0] == '$' {
		c.AI.Claude.APIKey = os.Getenv(c.AI.Claude.APIKey[2 : len(c.AI.Claude.APIKey)-1])
	}

	// AI DeepSeek
	if c.AI.DeepSeek.APIKey != "" && c.AI.DeepSeek.APIKey[0] == '$' {
		c.AI.DeepSeek.APIKey = os.Getenv(c.AI.DeepSeek.APIKey[2 : len(c.AI.DeepSeek.APIKey)-1])
	}
}

// Validate 验证配置
func (c *Config) Validate() error {
	// 验证服务器配置
	if c.Server.Port <= 0 || c.Server.Port > 65535 {
		return fmt.Errorf("无效的端口号: %d", c.Server.Port)
	}

	// 验证 AI 默认提供商
	if c.AI.DefaultProvider != "chatgpt" && c.AI.DefaultProvider != "claude" && c.AI.DefaultProvider != "deepseek" {
		return fmt.Errorf("无效的 AI 提供商: %s", c.AI.DefaultProvider)
	}

	// 验证地图默认提供商
	if c.Map.DefaultProvider != "baidu" && c.Map.DefaultProvider != "amap" && c.Map.DefaultProvider != "google" {
		return fmt.Errorf("无效的地图提供商: %s", c.Map.DefaultProvider)
	}

	return nil
}

// Default 返回默认配置
func Default() *Config {
	return &Config{
		Server: ServerConfig{
			Port: 8080,
			Host: "0.0.0.0",
		},
		STT: STTConfig{
			Provider:       "auto",
			Model:          "whisper-1",
			EnableFallback: true,
		},
		AI: AIConfig{
			DefaultProvider: "chatgpt",
			ChatGPT: AIProviderConfig{
				Model:   "gpt-3.5-turbo",
				BaseURL: "https://api.openai.com/v1",
			},
			Claude: AIProviderConfig{
				Model:   "claude-3-5-sonnet-20241022",
				BaseURL: "https://api.anthropic.com/v1",
			},
			DeepSeek: AIProviderConfig{
				Model:   "deepseek-chat",
				BaseURL: "https://api.deepseek.com/v1",
			},
		},
		Map: MapConfig{
			DefaultProvider: "baidu",
		},
	}
}
