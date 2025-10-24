package stt

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// AliyunClient 阿里云语音识别客户端
type AliyunClient struct {
	apiKey string
	model  string
	client *http.Client
}

// NewAliyunClient 创建阿里云语音识别客户端
func NewAliyunClient(config Config) (*AliyunClient, error) {
	if config.AliyunAPIKey == "" {
		return nil, fmt.Errorf("阿里云 API Key 不能为空")
	}

	model := config.AliyunModel
	if model == "" {
		model = "paraformer-realtime-v2" // 默认使用 Paraformer V2 模型
	}

	return &AliyunClient{
		apiKey: config.AliyunAPIKey,
		model:  model,
		client: &http.Client{
			Timeout: 30 * time.Second,
		},
	}, nil
}

// AliyunRequest 阿里云语音识别请求
type AliyunRequest struct {
	Model      string `json:"model"`
	Format     string `json:"format"`
	SampleRate int    `json:"sample_rate"`
	Language   string `json:"language"`
	URL        string `json:"url"` // 使用 URL 而不是 base64 数据
}

// AliyunResponse 阿里云语音识别响应
type AliyunResponse struct {
	Output struct {
		Result []struct {
			Sentence struct {
				Text string `json:"text"`
			} `json:"sentence"`
		} `json:"result"`
	} `json:"output"`
	RequestID string `json:"request_id"`
	Code      string `json:"code"`
	Message   string `json:"message"`
}

// TranscribeAudio 使用阿里云语音识别转录音频
func (c *AliyunClient) TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*Result, error) {
	// 读取音频数据
	audioData, err := io.ReadAll(audio)
	if err != nil {
		return nil, fmt.Errorf("读取音频数据失败: %w", err)
	}

	// 将音频数据转换为 base64
	audioBase64 := base64.StdEncoding.EncodeToString(audioData)

	// 构建请求 - 使用正确的阿里云 DashScope API 格式
	req := map[string]interface{}{
		"model": c.model,
		"input": map[string]interface{}{
			"format":      format,
			"sample_rate": 16000,
			"language":    "zh",
			"data":        audioBase64,
		},
	}

	// 序列化请求
	jsonData, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("序列化请求失败: %w", err)
	}

	// 创建 HTTP 请求 - 使用正确的 DashScope API 端点
	httpReq, err := http.NewRequestWithContext(ctx, "POST",
		"https://dashscope.aliyuncs.com/api/v1/services/aigc/speech-generation/speech-recognition",
		bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("创建请求失败: %w", err)
	}

	// 设置请求头
	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Authorization", "Bearer "+c.apiKey)

	// 发送请求
	resp, err := c.client.Do(httpReq)
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
		return nil, fmt.Errorf("阿里云 API 错误 (状态码 %d): %s", resp.StatusCode, string(body))
	}

	// 解析响应
	var aliyunResp AliyunResponse
	if err := json.Unmarshal(body, &aliyunResp); err != nil {
		return nil, fmt.Errorf("解析响应失败: %w", err)
	}

	// 检查业务状态码
	if aliyunResp.Code != "" && aliyunResp.Code != "200" {
		return nil, fmt.Errorf("阿里云语音识别错误: %s", aliyunResp.Message)
	}

	// 提取识别结果
	if len(aliyunResp.Output.Result) == 0 {
		return nil, fmt.Errorf("阿里云返回空结果")
	}

	// 合并所有识别结果
	var text string
	for _, result := range aliyunResp.Output.Result {
		text += result.Sentence.Text
	}

	return &Result{
		Text:     text,
		Language: "zh",
		Provider: ProviderAliyun,
	}, nil
}

// GetProviderName 获取提供商名称
func (c *AliyunClient) GetProviderName() string {
	return fmt.Sprintf("阿里云语音识别 (%s)", c.model)
}
