package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/sanmu/qwall2/pkg/mapprovider"
	"github.com/sanmu/qwall2/pkg/navigation"
	"github.com/sanmu/qwall2/pkg/parser"
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
		mcp.WithDescription("打开地图应用并开始从起点到终点的导航。支持百度地图和高德地图。"),
		mcp.WithString("start",
			mcp.Required(),
			mcp.Description("导航起点地址或地点名称（例如：北京天安门、上海浦东机场）"),
		),
		mcp.WithString("end",
			mcp.Required(),
			mcp.Description("导航终点地址或地点名称（例如：上海东方明珠、杭州西湖）"),
		),
		mcp.WithString("mapProvider",
			mcp.Description("地图提供商：baidu（百度地图）或 amap（高德地图）。默认为 baidu。"),
			mcp.Enum("baidu", "amap"),
		),
	)

	// 注册工具：自然语言解析
	parseIntentTool := mcp.NewTool("parse_navigation_intent",
		mcp.WithDescription("从自然语言文本中提取导航意图，识别起点和终点。适用于处理用户的语音或文字输入。"),
		mcp.WithString("text",
			mcp.Required(),
			mcp.Description("用户输入的自然语言文本（例如：从北京到上海、帮我去杭州西湖）"),
		),
	)

	// 添加工具到服务器
	s.AddTool(navigateMapTool, handleNavigateMap)
	s.AddTool(parseIntentTool, handleParseIntent)

	// 启动服务器
	log.Println("🚀 MCP 地图导航服务器已启动")
	log.Println("📍 支持的地图：百度地图、高德地图")
	log.Println("🔧 可用工具：navigate_map, parse_navigation_intent")

	if err := server.ServeStdio(s); err != nil {
		log.Fatalf("❌ 服务器启动失败: %v", err)
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

// handleParseIntent 处理自然语言解析工具调用
func handleParseIntent(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	// 将 Arguments 转换为 map
	args, ok := request.Params.Arguments.(map[string]interface{})
	if !ok {
		return mcp.NewToolResultError("无效的参数格式"), nil
	}

	// 获取输入文本
	text, ok := args["text"].(string)
	if !ok || text == "" {
		return mcp.NewToolResultError("请提供有效的文本输入"), nil
	}

	// 解析导航意图
	intent := parser.ParseNavigationIntent(text)
	formatted := parser.FormatNavigationIntent(intent)

	// 构建详细的响应
	response := fmt.Sprintf("🔍 导航意图解析结果：\n\n%s\n\n", formatted)

	if intent.Start != nil && intent.End != nil {
		// 验证地址
		startValid := parser.IsValidLocation(*intent.Start)
		endValid := parser.IsValidLocation(*intent.End)

		if startValid && endValid {
			response += "✅ 起点和终点已成功识别\n"
			response += "💡 建议：可以使用 navigate_map 工具开始导航\n"
			response += "\n示例调用：\n"

			// 生成示例 JSON
			example := map[string]string{
				"start":       *intent.Start,
				"end":         *intent.End,
				"mapProvider": "baidu",
			}
			exampleJSON, _ := json.MarshalIndent(example, "", "  ")
			response += string(exampleJSON)
		} else {
			response += "⚠️ 地址验证失败，请确认输入的地点名称是否正确"
		}
	} else if intent.End != nil && intent.Start == nil {
		response += "⚠️ 只识别到终点，起点未指定\n"
		response += "💡 建议：请补充起点信息，或使用当前位置作为起点"
	} else {
		response += "❌ 未能识别有效的导航信息\n"
		response += "💡 建议：请使用类似\"从A到B\"或\"去某地\"的表达方式"
	}

	return mcp.NewToolResultText(response), nil
}
