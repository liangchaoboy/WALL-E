package stt

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
)

// OpenAIClient OpenAI Whisper 客户端
type OpenAIClient struct {
	apiKey  string
	model   string
	baseURL string
	client  *http.Client
}

// NewOpenAIClient 创建 OpenAI Whisper 客户端
func NewOpenAIClient(config Config) (*OpenAIClient, error) {
	if config.OpenAIKey == "" {
		return nil, fmt.Errorf("OpenAI API Key 不能为空")
	}

	model := config.Model
	if model == "" {
		model = "whisper-1" // 默认模型
	}

	return &OpenAIClient{
		apiKey:  config.OpenAIKey,
		model:   model,
		baseURL: "https://api.openai.com/v1",
		client:  &http.Client{},
	}, nil
}

// WhisperResponse Whisper API 响应
type WhisperResponse struct {
	Text     string `json:"text"`
	Language string `json:"language"`
	Error    *struct {
		Message string `json:"message"`
		Type    string `json:"type"`
	} `json:"error,omitempty"`
}

// TranscribeAudio 转录音频为文字
func (c *OpenAIClient) TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*Result, error) {
	// 读取音频数据
	audioData, err := io.ReadAll(audio)
	if err != nil {
		return nil, fmt.Errorf("读取音频数据失败: %w", err)
	}

	// 创建 multipart form
	var requestBody bytes.Buffer
	writer := multipart.NewWriter(&requestBody)

	// 添加文件
	part, err := writer.CreateFormFile("file", "audio."+format)
	if err != nil {
		return nil, fmt.Errorf("创建表单文件失败: %w", err)
	}

	if _, err := part.Write(audioData); err != nil {
		return nil, fmt.Errorf("写入音频数据失败: %w", err)
	}

	// 添加模型参数
	if err := writer.WriteField("model", c.model); err != nil {
		return nil, fmt.Errorf("写入模型参数失败: %w", err)
	}

	// 添加语言参数（中文）
	if err := writer.WriteField("language", "zh"); err != nil {
		return nil, fmt.Errorf("写入语言参数失败: %w", err)
	}

	// 关闭 writer
	if err := writer.Close(); err != nil {
		return nil, fmt.Errorf("关闭 writer 失败: %w", err)
	}

	// 创建 HTTP 请求
	req, err := http.NewRequestWithContext(
		ctx,
		"POST",
		c.baseURL+"/audio/transcriptions",
		&requestBody,
	)
	if err != nil {
		return nil, fmt.Errorf("创建请求失败: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+c.apiKey)
	req.Header.Set("Content-Type", writer.FormDataContentType())

	// 发送请求
	resp, err := c.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("请求失败: %w", err)
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("读取响应失败: %w", err)
	}

	// 检查 HTTP 状态码
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("OpenAI API 错误 (状态码 %d): %s", resp.StatusCode, string(body))
	}

	// 解析响应
	var whisperResp WhisperResponse
	if err := json.Unmarshal(body, &whisperResp); err != nil {
		return nil, fmt.Errorf("解析响应失败: %w", err)
	}

	// 检查错误
	if whisperResp.Error != nil {
		return nil, fmt.Errorf("OpenAI Whisper 错误: %s", whisperResp.Error.Message)
	}

	return &Result{
		Text:     whisperResp.Text,
		Language: whisperResp.Language,
		Provider: ProviderOpenAI,
	}, nil
}

// GetProviderName 获取提供商名称
func (c *OpenAIClient) GetProviderName() string {
	return "OpenAI Whisper"
}
