package parser

import (
	"fmt"
	"regexp"
	"strings"
)

// NavigationIntent 导航意图
type NavigationIntent struct {
	Start      *string `json:"start"`      // 起点（可为空）
	End        *string `json:"end"`        // 终点（可为空）
	Confidence float64 `json:"confidence"` // 置信度 (0-1)
}

// 常见的导航关键词模式
var navigationPatterns = []*regexp.Regexp{
	// "从 A 到 B" 模式 - 使用否定字符类来避免过度匹配
	regexp.MustCompile(`(?:从|自)([^到去至往导航路线]+)(?:到|去|至|往)([^导航路线怎]+)(?:导航|路线|怎么走)?$`),
	// "去 B" 模式（只有终点）
	regexp.MustCompile(`^(?:去|到|前往)([^导航路线怎]+)(?:导航|路线|怎么走)?$`),
	// "A 到 B 导航" 模式
	regexp.MustCompile(`^([^到去至往导航路线]+)(?:到|去|至|往)([^导航路线怎]+)(?:导航|路线|怎么走)$`),
	// "帮我从 A 到 B" 模式
	regexp.MustCompile(`帮我?(?:从|自)([^到去至往]+)(?:到|去|至|往)(.+)$`),
}

// ParseNavigationIntent 从自然语言中提取导航意图
func ParseNavigationIntent(text string) NavigationIntent {
	if text == "" {
		return NavigationIntent{
			Start:      nil,
			End:        nil,
			Confidence: 0,
		}
	}

	// 清理输入文本（移除空白字符）
	cleanText := strings.TrimSpace(text)
	cleanText = strings.ReplaceAll(cleanText, " ", "")
	cleanText = strings.ReplaceAll(cleanText, "\t", "")
	cleanText = strings.ReplaceAll(cleanText, "\n", "")

	// 尝试匹配各种模式
	for _, pattern := range navigationPatterns {
		matches := pattern.FindStringSubmatch(cleanText)

		if len(matches) > 0 {
			// 两个捕获组：起点和终点
			if len(matches) == 3 {
				start := strings.TrimSpace(matches[1])
				end := strings.TrimSpace(matches[2])

				if start != "" && end != "" {
					return NavigationIntent{
						Start:      &start,
						End:        &end,
						Confidence: 0.9,
					}
				}
			}

			// 一个捕获组：只有终点
			if len(matches) == 2 {
				end := strings.TrimSpace(matches[1])

				if end != "" {
					return NavigationIntent{
						Start:      nil, // 起点为空，可能需要用户补充或使用当前位置
						End:        &end,
						Confidence: 0.7,
					}
				}
			}
		}
	}

	// 未能解析
	return NavigationIntent{
		Start:      nil,
		End:        nil,
		Confidence: 0,
	}
}

// IsValidLocation 验证地址是否有效（基本检查）
func IsValidLocation(location string) bool {
	if location == "" {
		return false
	}

	trimmed := strings.TrimSpace(location)

	// 基本验证：长度检查
	if len(trimmed) < 2 || len(trimmed) > 100 {
		return false
	}

	// 过滤无意义的词
	invalidWords := []string{"这里", "那里", "这", "那", "哪里"}
	for _, word := range invalidWords {
		if trimmed == word {
			return false
		}
	}

	return true
}

// FormatNavigationIntent 格式化解析结果为可读字符串
func FormatNavigationIntent(intent NavigationIntent) string {
	var parts []string

	if intent.Start != nil {
		parts = append(parts, "起点："+*intent.Start)
	} else {
		parts = append(parts, "起点：未指定")
	}

	if intent.End != nil {
		parts = append(parts, "终点："+*intent.End)
	} else {
		parts = append(parts, "终点：未指定")
	}

	confidence := int(intent.Confidence * 100)
	parts = append(parts, fmt.Sprintf("置信度：%d%%", confidence))

	return strings.Join(parts, "\n")
}
