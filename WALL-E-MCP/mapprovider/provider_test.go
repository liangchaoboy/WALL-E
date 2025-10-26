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
	if !strings.HasPrefix(url, "http://api.map.baidu.com/direction") {
		t.Errorf("URL 应该以 http://api.map.baidu.com/direction 开头，实际得到: %s", url)
	}

	// 检查必要参数
	if !strings.Contains(url, "origin=") {
		t.Error("URL 应该包含 origin 参数")
	}

	if !strings.Contains(url, "destination=") {
		t.Error("URL 应该包含 destination 参数")
	}

	if !strings.Contains(url, "mode=") {
		t.Error("URL 应该包含 mode 参数")
	}

	if !strings.Contains(url, "src=") {
		t.Error("URL 应该包含 src 参数")
	}

	if !strings.Contains(url, "region=") {
		t.Error("URL 应该包含 region 参数")
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

func TestGenerateGoogleMapsURL(t *testing.T) {
	start := "南京"
	end := "东京"

	url := GenerateGoogleMapsURL(start, end)

	// 检查基础 URL
	if !strings.HasPrefix(url, "https://www.google.com/maps/dir/") {
		t.Errorf("URL 应该以 https://www.google.com/maps/dir/ 开头")
	}

	// 检查必要参数
	if !strings.Contains(url, "api=1") {
		t.Error("URL 应该包含 api=1 参数")
	}

	if !strings.Contains(url, "origin=") {
		t.Error("URL 应该包含 origin 参数")
	}

	if !strings.Contains(url, "destination=") {
		t.Error("URL 应该包含 destination 参数")
	}

	if !strings.Contains(url, "travelmode=") {
		t.Error("URL 应该包含 travelmode 参数")
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
			urlPrefix:   "http://api.map.baidu.com/direction",
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
			name: "Google Maps",
			params: NavigationParams{
				Start:       "南京",
				End:         "东京",
				MapProvider: Google,
			},
			shouldError: false,
			urlPrefix:   "https://www.google.com/maps/dir/",
		},
		{
			name: "默认地图提供商",
			params: NavigationParams{
				Start: "北京",
				End:   "上海",
			},
			shouldError: false,
			urlPrefix:   "http://api.map.baidu.com/direction",
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
				MapProvider: "bing",
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
		{Google, "Google Maps"},
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
		{"google", true},
		{"bing", false},
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

func TestExtractCityName(t *testing.T) {
	tests := []struct {
		name     string
		address  string
		expected string
	}{
		{"Complete address with city", "上海东方明珠", "上海"},
		{"Complete address with city", "北京天安门", "北京"},
		{"City name only", "北京", "北京"},
		{"City name only", "上海", "上海"},
		{"City with district", "深圳南山区", "深圳"},
		{"Unknown city", "小城市", "小城市"},
		{"Long unknown address", "某个不知名的地方", "全国"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := extractCityName(tt.address)
			if result != tt.expected {
				t.Errorf("地址 '%s': 期望提取城市 '%s'，实际得到: '%s'", tt.address, tt.expected, result)
			}
		})
	}
}
