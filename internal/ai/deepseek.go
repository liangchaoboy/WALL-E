package ai

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

// DeepSeekClient DeepSeek 客户端实现
type DeepSeekClient struct {
	config Config
	client *http.Client
}

// NewDeepSeekClient 创建 DeepSeek 客户端
func NewDeepSeekClient(config Config) (*DeepSeekClient, error) {
	if config.APIKey == "" {
		return nil, fmt.Errorf("DeepSeek API Key 不能为空")
	}

	if config.Model == "" {
		config.Model = "deepseek-chat"
	}

	if config.BaseURL == "" {
		config.BaseURL = "https://api.deepseek.com/v1"
	}

	return &DeepSeekClient{
		config: config,
		client: &http.Client{},
	}, nil
}

// GetProviderName 获取提供商名称
func (c *DeepSeekClient) GetProviderName() string {
	return "DeepSeek"
}

// ExtractNavigationIntent 从文本中提取导航意图
func (c *DeepSeekClient) ExtractNavigationIntent(ctx context.Context, text string) (*NavigationIntent, error) {
	// 构建提示词
	systemPrompt := `你是一个智能导航助手。用户会说出导航需求，你需要提取起点和终点。
请以 JSON 格式返回结果，格式如下：
{"start": "起点地址", "end": "终点地址"}

规则：
1. 如果用户只说了目的地，起点设为"当前位置"
2. 提取具体的地址、地点名称
3. 只返回 JSON，不要其他文字

示例：
用户："我要从北京去上海"
返回：{"start": "北京", "end": "上海"}

用户："去天安门"
返回：{"start": "当前位置", "end": "天安门"}`

	// 构建请求
	reqBody := map[string]interface{}{
		"model": c.config.Model,
		"messages": []map[string]string{
			{"role": "system", "content": systemPrompt},
			{"role": "user", "content": text},
		},
		"temperature": 0.3,
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return nil, fmt.Errorf("序列化请求失败: %w", err)
	}

	// 发送请求
	url := fmt.Sprintf("%s/chat/completions", c.config.BaseURL)
	req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("创建请求失败: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.config.APIKey))

	resp, err := c.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("请求失败: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("API 返回错误 %d: %s", resp.StatusCode, string(body))
	}

	// 解析响应
	var result struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("解析响应失败: %w", err)
	}

	if len(result.Choices) == 0 {
		return nil, fmt.Errorf("API 返回空结果")
	}

	// 提取 JSON
	content := strings.TrimSpace(result.Choices[0].Message.Content)

	// 尝试解析 JSON
	var intent NavigationIntent
	if err := json.Unmarshal([]byte(content), &intent); err != nil {
		return nil, fmt.Errorf("解析导航意图失败: %w, 原始内容: %s", err, content)
	}

	return &intent, nil
}
