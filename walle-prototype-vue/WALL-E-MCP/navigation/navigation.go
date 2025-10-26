package navigation

import (
	"fmt"

	"walle.qiniu.com/mapprovider"
)

// NavigateMapArgs 地图导航参数
type NavigateMapArgs struct {
	Start       string                  `json:"start"`
	End         string                  `json:"end"`
	MapProvider mapprovider.MapProvider `json:"mapProvider,omitempty"`
}

// NavigateMap 执行地图导航
// 生成导航 URL 并在默认浏览器中打开
func NavigateMap(args NavigateMapArgs) (string, error) {
	// 设置默认地图提供商
	if args.MapProvider == "" {
		args.MapProvider = mapprovider.Baidu
	}

	// 参数验证
	if args.Start == "" || args.End == "" {
		return "", fmt.Errorf("起点和终点不能为空")
	}

	// 生成导航 URL
	params := mapprovider.NavigationParams{
		Start:       args.Start,
		End:         args.End,
		MapProvider: args.MapProvider,
	}

	url, err := mapprovider.GenerateNavigationURL(params)
	if err != nil {
		return "", err
	}

	// 在默认浏览器中打开 URL
	//err = browser.OpenURL(url)
	// if err != nil {
	// 	return "", fmt.Errorf("打开地图失败: %v", err)
	// }

	return url, nil
}
