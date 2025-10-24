package mapprovider

import (
	"strings"
	"testing"
)

func TestGenerateBaiduMapURL(t *testing.T) {
	start := "北京天安门"
	end := "上海东方明珠"

	url := GenerateBaiduMapURL(start, end)

	// 检查基础 URL
	if !strings.HasPrefix(url, "https://map.baidu.com/") {
		t.Errorf("URL 应该以 https://map.baidu.com/ 开头")
	}

	// 检查必要参数
	if !strings.Contains(url, "origin=") {
		t.Error("URL 应该包含 origin 参数")
	}

	if !strings.Contains(url, "destination=") {
		t.Error("URL 应该包含 destination 参数")
	}

	if !strings.Contains(url, "da_src=shareurl") {
		t.Error("URL 应该包含 da_src=shareurl 参数")
	}
}

func TestGenerateAmapURL(t *testing.T) {
	start := "北京天安门"
	end := "上海东方明珠"

	url := GenerateAmapURL(start, end)

	// 检查基础 URL
	if !strings.HasPrefix(url, "https://www.amap.com/dir") {
		t.Errorf("URL 应该以 https://www.amap.com/dir 开头")
	}

	// 检查必要参数
	if !strings.Contains(url, "from=") {
		t.Error("URL 应该包含 from 参数")
	}

	if !strings.Contains(url, "to=") {
		t.Error("URL 应该包含 to 参数")
	}
}

func TestGenerateNavigationURL(t *testing.T) {
	tests := []struct {
		name        string
		params      NavigationParams
		shouldError bool
		urlPrefix   string
	}{
		{
			name: "百度地图",
			params: NavigationParams{
				Start:       "北京",
				End:         "上海",
				MapProvider: Baidu,
			},
			shouldError: false,
			urlPrefix:   "https://map.baidu.com/",
		},
		{
			name: "高德地图",
			params: NavigationParams{
				Start:       "北京",
				End:         "上海",
				MapProvider: Amap,
			},
			shouldError: false,
			urlPrefix:   "https://www.amap.com/dir",
		},
		{
			name: "默认地图提供商",
			params: NavigationParams{
				Start: "北京",
				End:   "上海",
			},
			shouldError: false,
			urlPrefix:   "https://map.baidu.com/",
		},
		{
			name: "起点为空",
			params: NavigationParams{
				Start:       "",
				End:         "上海",
				MapProvider: Baidu,
			},
			shouldError: true,
		},
		{
			name: "终点为空",
			params: NavigationParams{
				Start:       "北京",
				End:         "",
				MapProvider: Baidu,
			},
			shouldError: true,
		},
		{
			name: "不支持的地图提供商",
			params: NavigationParams{
				Start:       "北京",
				End:         "上海",
				MapProvider: "google",
			},
			shouldError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			url, err := GenerateNavigationURL(tt.params)

			if tt.shouldError {
				if err == nil {
					t.Error("期望返回错误，但没有错误")
				}
			} else {
				if err != nil {
					t.Errorf("不期望返回错误，但得到: %v", err)
				}

				if !strings.HasPrefix(url, tt.urlPrefix) {
					t.Errorf("期望 URL 以 %s 开头，实际得到: %s", tt.urlPrefix, url)
				}
			}
		})
	}
}

func TestGetMapProviderName(t *testing.T) {
	tests := []struct {
		provider MapProvider
		expected string
	}{
		{Baidu, "百度地图"},
		{Amap, "高德地图"},
		{"unknown", "unknown"},
	}

	for _, tt := range tests {
		t.Run(string(tt.provider), func(t *testing.T) {
			result := GetMapProviderName(tt.provider)
			if result != tt.expected {
				t.Errorf("期望 %s，实际得到: %s", tt.expected, result)
			}
		})
	}
}

func TestIsValidMapProvider(t *testing.T) {
	tests := []struct {
		provider string
		expected bool
	}{
		{"baidu", true},
		{"amap", true},
		{"google", false},
		{"", false},
		{"BAIDU", false}, // 区分大小写
	}

	for _, tt := range tests {
		t.Run(tt.provider, func(t *testing.T) {
			result := IsValidMapProvider(tt.provider)
			if result != tt.expected {
				t.Errorf("对于提供商 '%s'，期望 %v，实际得到: %v", tt.provider, tt.expected, result)
			}
		})
	}
}
