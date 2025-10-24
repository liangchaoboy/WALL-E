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

// ClaudeClient Claude 客户端实现
type ClaudeClient struct {
	config Config
	client *http.Client
}

// NewClaudeClient 创建 Claude 客户端
func NewClaudeClient(config Config) (*ClaudeClient, error) {
	if config.APIKey == "" {
		return nil, fmt.Errorf("Claude API Key 不能为空")
	}

	if config.Model == "" {
		config.Model = "claude-3-5-sonnet-20241022"
	}

	if config.BaseURL == "" {
		config.BaseURL = "https://api.anthropic.com/v1"
	}

	return &ClaudeClient{
		config: config,
		client: &http.Client{},
	}, nil
}

// GetProviderName 获取提供商名称
func (c *ClaudeClient) GetProviderName() string {
	return "Claude"
}

// ExtractNavigationIntent 从文本中提取导航意图
func (c *ClaudeClient) ExtractNavigationIntent(ctx context.Context, text string) (*NavigationIntent, error) {
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
		"model":      c.config.Model,
		"max_tokens": 1024,
		"system":     systemPrompt,
		"messages": []map[string]string{
			{"role": "user", "content": text},
		},
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return nil, fmt.Errorf("序列化请求失败: %w", err)
	}

	// 发送请求
	url := fmt.Sprintf("%s/messages", c.config.BaseURL)
	req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("创建请求失败: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("x-api-key", c.config.APIKey)
	req.Header.Set("anthropic-version", "2023-06-01")

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
		Content []struct {
			Type string `json:"type"`
			Text string `json:"text"`
		} `json:"content"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("解析响应失败: %w", err)
	}

	if len(result.Content) == 0 {
		return nil, fmt.Errorf("API 返回空结果")
	}

	// 提取文本内容
	content := strings.TrimSpace(result.Content[0].Text)

	// 清理内容，移除 Markdown 代码块格式
	content = CleanJSONContent(content)

	// 尝试解析 JSON
	var intent NavigationIntent
	if err := json.Unmarshal([]byte(content), &intent); err != nil {
		return nil, fmt.Errorf("解析导航意图失败: %w, 原始内容: %s", err, content)
	}

	return &intent, nil
}
