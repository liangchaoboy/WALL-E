package main

import (
	"context"
	"fmt"
	"log"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"walle.qiniu.com/mapprovider"
	"walle.qiniu.com/navigation"
)

func main() {
	// 创建 MCP 服务器
	s := server.NewMCPServer(
		"map-navigation-mcp",
		"1.0.0",
		server.WithLogging(),
	)

	// 注册工具：地图导航
	navigateMapTool := mcp.NewTool("navigate_map",
		mcp.WithDescription("当用户想要导航、查看路线、去某地、从A到B时，使用此工具打开地图应用。支持百度地图（国内）、高德地图（国内）和 Google Maps（国际路线）。这是一个主动操作工具，会直接在浏览器中打开地图。"),
		mcp.WithString("start",
			mcp.Required(),
			mcp.Description("导航起点。可以是城市名、地标、地址。例：'北京'、'北京天安门'、'上海浦东机场'。如果用户没有指定起点，可以问用户或设为'当前位置'。"),
		),
		mcp.WithString("end",
			mcp.Required(),
			mcp.Description("导航终点。可以是城市名、地标、地址。例：'上海'、'上海东方明珠'、'杭州西湖'、'东京浅草寺'。这是用户想去的目的地。"),
		),
		mcp.WithString("mapProvider",
			mcp.Description("地图服务选择。baidu=百度地图（国内首选），amap=高德地图（国内首选），google=Google Maps（国际路线必须用，如北京→东京、上海→纽约）。默认baidu。"),
			mcp.Enum("baidu", "amap", "google"),
		),
	)

	// 添加工具到服务器
	s.AddTool(navigateMapTool, handleNavigateMap)

	// 启动服务器
	log.Println("🚀 MCP 地图导航服务器已启动")
	log.Println("📍 支持的地图：百度地图、高德地图、Google Maps")
	log.Println("🔧 可用工具：navigate_map, parse_navigation_intent")

	sseServer := server.NewSSEServer(s, server.WithBaseURL(""))
	log.Println("🚀 MCP 地图导航服务器:10087")
	err := sseServer.Start(fmt.Sprintf(":%d", 10087))
	if err != nil {
		log.Fatal(err)
	}
}

// handleNavigateMap 处理地图导航工具调用
func handleNavigateMap(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	// 将 Arguments 转换为 map
	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("无效的参数格式"), nil
	}

	// 解析参数
	var navArgs navigation.NavigateMapArgs

	if start, ok := args["start"].(string); ok {
		navArgs.Start = start
	}

	if end, ok := args["end"].(string); ok {
		navArgs.End = end
	}

	if provider, ok := args["mapProvider"].(string); ok {
		navArgs.MapProvider = mapprovider.MapProvider(provider)
	}

	// 执行导航
	result, err := navigation.NavigateMap(navArgs)
	if err != nil {
		return mcp.NewToolResultError(err.Error()), nil
	}

	return mcp.NewToolResultText(result), nil
}
