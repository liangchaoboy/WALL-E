package mapprovider

import (
	"fmt"
	"net/url"
)

// MapProvider 地图提供商类型
type MapProvider string

const (
	// Baidu 百度地图
	Baidu MapProvider = "baidu"
	// Amap 高德地图
	Amap MapProvider = "amap"
)

// NavigationParams 导航参数
type NavigationParams struct {
	Start       string      `json:"start"`       // 起点
	End         string      `json:"end"`         // 终点
	MapProvider MapProvider `json:"mapProvider"` // 地图提供商
}

// GenerateBaiduMapURL 生成百度地图导航 URL
// Web 端路线规划 URL 格式（官方 API）：
// http://api.map.baidu.com/direction?origin=起点&destination=终点&mode=driving&region=城市&output=html&src=webapp
func GenerateBaiduMapURL(start, end string) string {
	baseURL := "http://api.map.baidu.com/direction"
	params := url.Values{}

	// 起点和终点（支持地名）
	params.Add("origin", start)
	params.Add("destination", end)

	// 路线模式：driving(驾车)、transit(公交)、walking(步行)、riding(骑行)
	params.Add("mode", "transit")

	// 必须参数
	params.Add("output", "html")
	params.Add("src", "webapp.qwall2.navigation")

	return fmt.Sprintf("%s?%s", baseURL, params.Encode())
}

// GenerateAmapURL 生成高德地图导航 URL
// Web 端路线规划 URL 格式：
// https://www.amap.com/dir?from=起点&to=终点
func GenerateAmapURL(start, end string) string {
	baseURL := "https://www.amap.com/dir"
	params := url.Values{}
	params.Add("from", start)
	params.Add("to", end)
	// 可选参数：
	// params.Add("policy", "0") // 路线策略：0-推荐，1-避开收费，2-避开拥堵
	// params.Add("type", "car")  // 出行方式：car-驾车，bus-公交，walk-步行

	return fmt.Sprintf("%s?%s", baseURL, params.Encode())
}

// GenerateNavigationURL 根据地图提供商生成导航 URL
func GenerateNavigationURL(params NavigationParams) (string, error) {
	if params.Start == "" || params.End == "" {
		return "", fmt.Errorf("起点和终点不能为空")
	}

	// 默认使用百度地图
	if params.MapProvider == "" {
		params.MapProvider = Baidu
	}

	switch params.MapProvider {
	case Baidu:
		return GenerateBaiduMapURL(params.Start, params.End), nil
	case Amap:
		return GenerateAmapURL(params.Start, params.End), nil
	default:
		return "", fmt.Errorf("不支持的地图提供商: %s", params.MapProvider)
	}
}

// GetMapProviderName 获取地图提供商的友好名称
func GetMapProviderName(provider MapProvider) string {
	names := map[MapProvider]string{
		Baidu: "百度地图",
		Amap:  "高德地图",
	}

	if name, ok := names[provider]; ok {
		return name
	}
	return string(provider)
}

// IsValidMapProvider 验证地图提供商是否有效
func IsValidMapProvider(provider string) bool {
	return provider == string(Baidu) || provider == string(Amap)
}
