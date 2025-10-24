package parser

import (
	"testing"
)

func TestParseNavigationIntent(t *testing.T) {
	tests := []struct {
		name          string
		input         string
		expectedStart *string
		expectedEnd   *string
		minConfidence float64
	}{
		{
			name:          "从A到B格式",
			input:         "从北京到上海",
			expectedStart: stringPtr("北京"),
			expectedEnd:   stringPtr("上海"),
			minConfidence: 0.8,
		},
		{
			name:          "从A去B格式",
			input:         "从天安门去东方明珠",
			expectedStart: stringPtr("天安门"),
			expectedEnd:   stringPtr("东方明珠"),
			minConfidence: 0.8,
		},
		{
			name:          "帮我从A到B格式",
			input:         "帮我从北京七牛云到上海七牛云",
			expectedStart: stringPtr("北京七牛云"),
			expectedEnd:   stringPtr("上海七牛云"),
			minConfidence: 0.8,
		},
		{
			name:          "去B格式",
			input:         "去杭州西湖",
			expectedStart: nil,
			expectedEnd:   stringPtr("杭州西湖"),
			minConfidence: 0.6,
		},
		{
			name:          "到B导航格式",
			input:         "到上海浦东机场导航",
			expectedStart: nil,
			expectedEnd:   stringPtr("上海浦东机场"),
			minConfidence: 0.6,
		},
		{
			name:          "A到B导航格式",
			input:         "北京到上海导航",
			expectedStart: stringPtr("北京"),
			expectedEnd:   stringPtr("上海"),
			minConfidence: 0.8,
		},
		{
			name:          "空字符串",
			input:         "",
			expectedStart: nil,
			expectedEnd:   nil,
			minConfidence: 0,
		},
		{
			name:          "无效输入",
			input:         "今天天气真好",
			expectedStart: nil,
			expectedEnd:   nil,
			minConfidence: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ParseNavigationIntent(tt.input)

			// 检查起点
			if tt.expectedStart == nil {
				if result.Start != nil {
					t.Errorf("期望起点为 nil，实际得到: %s", *result.Start)
				}
			} else {
				if result.Start == nil {
					t.Errorf("期望起点为 %s，实际得到: nil", *tt.expectedStart)
				} else if *result.Start != *tt.expectedStart {
					t.Errorf("期望起点为 %s，实际得到: %s", *tt.expectedStart, *result.Start)
				}
			}

			// 检查终点
			if tt.expectedEnd == nil {
				if result.End != nil {
					t.Errorf("期望终点为 nil，实际得到: %s", *result.End)
				}
			} else {
				if result.End == nil {
					t.Errorf("期望终点为 %s，实际得到: nil", *tt.expectedEnd)
				} else if *result.End != *tt.expectedEnd {
					t.Errorf("期望终点为 %s，实际得到: %s", *tt.expectedEnd, *result.End)
				}
			}

			// 检查置信度
			if result.Confidence < tt.minConfidence {
				t.Errorf("期望置信度 >= %.2f，实际得到: %.2f", tt.minConfidence, result.Confidence)
			}
		})
	}
}

func TestIsValidLocation(t *testing.T) {
	tests := []struct {
		name     string
		location string
		expected bool
	}{
		{
			name:     "有效地点",
			location: "北京天安门",
			expected: true,
		},
		{
			name:     "空字符串",
			location: "",
			expected: false,
		},
		{
			name:     "太短",
			location: "a",
			expected: false,
		},
		{
			name:     "无意义的词-这里",
			location: "这里",
			expected: false,
		},
		{
			name:     "无意义的词-那里",
			location: "那里",
			expected: false,
		},
		{
			name:     "正常城市名",
			location: "上海",
			expected: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsValidLocation(tt.location)
			if result != tt.expected {
				t.Errorf("期望 %v，实际得到: %v", tt.expected, result)
			}
		})
	}
}

// 辅助函数：创建字符串指针
func stringPtr(s string) *string {
	return &s
}
