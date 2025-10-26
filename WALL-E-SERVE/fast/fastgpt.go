package fast

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"time"
)

const (
	ChatMessageRoleSystem    = "system"
	ChatMessageRoleUser      = "user"
	ChatMessageRoleAssistant = "assistant"
	ChatMessageRoleFunction  = "function"
	ChatMessageRoleTool      = "tool"
	ToolTypeFunction         = "function"
)

func getClient(api_key string) *http.Client {
	return &http.Client{
		Transport: NewTransport(api_key),
	}
}

type ToolType string

type FunctionCall struct {
	Name      string `json:"name,omitempty"`
	Arguments string `json:"arguments,omitempty"`
}

type ToolCall struct {
	Id       string       `json:"id"`
	Type     ToolType     `json:"type"`
	Function FunctionCall `json:"function"`
}

type ChatCompletionMessage struct {
	Role       string     `json:"role"`
	Content    string     `json:"content"`
	Name       string     `json:"name,omitempty"`
	ToolCalls  []ToolCall `json:"tool_calls,omitempty"`
	ToolCallID string     `json:"tool_call_id,omitempty"`
}

type AIReqData struct {
	ChatId    string                  `json:"chatId,omitempty"`
	Stream    bool                    `json:"stream,omitempty"`
	Detail    bool                    `json:"detail,omitempty"`
	Variables interface{}             `json:"variables,omitempty"`
	Messages  []ChatCompletionMessage `json:"messages"`
}

// ContentData 用于解析 content 字段中的 JSON 数据
type ContentData struct {
	Data string `json:"data,omitempty"`
	URL  string `json:"url,omitempty"`
}

// ParsedChoice 解析后的选择结果
type ParsedChoice struct {
	OriginalContent string       `json:"original_content"`
	ContentData     *ContentData `json:"content_data,omitempty"`
	IsJSONContent   bool         `json:"is_json_content"`
	TextContent     string       `json:"text_content"`
	FinishReason    string       `json:"finish_reason"`
	Index           int          `json:"index"`
}

// ParsedChatCompletionResult 解析后的完整结果
type ParsedChatCompletionResult struct {
	Id      string         `json:"id"`
	Model   string         `json:"model"`
	Usage   Usage          `json:"usage"`
	Choices []Choice       `json:"choices"` // 原始选择数据
	Parsed  []ParsedChoice `json:"parsed"`  // 解析后的选择数据
}

type Transport struct {
	apiKey       string
	roundTripper http.RoundTripper
}

func NewTransport(apiKey string) *Transport {
	return &Transport{
		apiKey: apiKey,
		roundTripper: &http.Transport{
			DialContext: (&net.Dialer{
				Timeout:   90 * time.Second,
				KeepAlive: 120 * time.Second,
			}).DialContext,
			ForceAttemptHTTP2:     true,
			MaxIdleConns:          100,
			IdleConnTimeout:       90 * time.Second,
			TLSHandshakeTimeout:   10 * time.Second,
			ExpectContinueTimeout: 1 * time.Second,
			ResponseHeaderTimeout: 300 * time.Second,
		},
	}
}

func (t *Transport) RoundTrip(req *http.Request) (*http.Response, error) {
	req.Header.Set("Authorization", "Bearer "+t.apiKey)
	return t.roundTripper.RoundTrip(req)
}

// parseContent 解析 content 字段，处理两种模式
func parseContent(content string) (textContent string, contentData *ContentData, isJSON bool) {
	// 先尝试解析为 JSON
	var data ContentData
	if err := json.Unmarshal([]byte(content), &data); err == nil {
		// 如果解析成功，检查是否有预期的字段
		if data.Data != "" || data.URL != "" {
			return data.Data, &data, true
		}
	}
	// 如果不是 JSON 或没有预期字段，当作纯文本处理
	return content, nil, false
}

// ChatFromGPT 调用 GPT 接口并返回解析后的结果
func ChatFromGPT(request AIReqData) (result *ParsedChatCompletionResult, err error) {
	requestBody, err := json.Marshal(request)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	req, err := http.NewRequest("POST", "http://8.219.59.3:3000/api/v1/chat/completions", bytes.NewBuffer(requestBody))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")

	apiKey := os.Getenv("FASTGPT_API_KEY")
	if apiKey == "" {
		return nil, errors.New("FASTGPT_API_KEY not set")
	}
	log.Print(apiKey)

	fastclient := getClient(apiKey)

	resp, err := fastclient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to send request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("failed to create chat completion: %s", resp.Status)
	}

	// 先解析原始结果
	var rawResult ChatCompletionResult
	if err := json.NewDecoder(resp.Body).Decode(&rawResult); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	// 创建解析后的结果
	parsedResult := &ParsedChatCompletionResult{
		Id:      rawResult.Id,
		Model:   rawResult.Model,
		Usage:   rawResult.Usage,
		Choices: rawResult.Choices,
		Parsed:  make([]ParsedChoice, len(rawResult.Choices)),
	}

	// 解析每个 choice 的 content
	for i, choice := range rawResult.Choices {
		textContent, contentData, isJSON := parseContent(choice.Message.Content)

		parsedResult.Parsed[i] = ParsedChoice{
			OriginalContent: choice.Message.Content,
			ContentData:     contentData,
			IsJSONContent:   isJSON,
			TextContent:     textContent,
			FinishReason:    choice.FinishReason,
			Index:           choice.Index,
		}
	}

	return parsedResult, nil
}

// 原有的结构体保持不变
type Usage struct {
	PromptTokens     int `json:"prompt_tokens"`
	CompletionTokens int `json:"completion_tokens"`
	TotalTokens      int `json:"total_tokens"`
}

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type Choice struct {
	Message      Message `json:"message"`
	FinishReason string  `json:"finish_reason"`
	Index        int     `json:"index"`
}

type ChatCompletionResult struct {
	Id      string   `json:"id"`
	Model   string   `json:"model"`
	Usage   Usage    `json:"usage"`
	Choices []Choice `json:"choices"`
}

// 处理导航请求的核心逻辑
func ChatCompletion(text string) (string, string, error) {
	if text == "" {
		return "", "", errors.New("empty input text")
	}

	request := AIReqData{
		Stream:   false,
		Detail:   false,
		Messages: []ChatCompletionMessage{{Role: ChatMessageRoleUser, Content: text}},
	}

	result, err := ChatFromGPT(request)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	if result.Parsed[0].IsJSONContent {
		return result.Parsed[0].ContentData.Data, result.Parsed[0].ContentData.URL, nil
	} else {
		// 纯文本模式
		return result.Parsed[0].TextContent, "", nil
	}
}
