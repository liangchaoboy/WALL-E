package main

import (
	"context"
	"fmt"
	"log"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
)

func main() {
	log.Println("mcp server init start")
	// Create a new MCP server
	mcpServer := server.NewMCPServer(
		"ssetest",
		"1.0.0",
		server.WithToolCapabilities(false),
	)

	// Add tool
	tool := mcp.NewTool("check_iphone_number",
		mcp.WithDescription("获取指定好友的手机联系方式"),
		mcp.WithString("name",
			mcp.Required(),
			mcp.Description("还有的名称"),
		),
	)

	// Add tool handler
	mcpServer.AddTool(tool, phoneHandler)

	log.Println("mcp server init done")

	sseServer := server.NewSSEServer(mcpServer, server.WithBaseURL(""))
	err := sseServer.Start(fmt.Sprintf(":%d", 10087))
	if err != nil {
		log.Fatal(err)
	}
}

func phoneHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	num := "我不知道"
	name, err := request.RequireString("name")
	log.Printf("开始调用%s \n", name)
	if err != nil {
		return mcp.NewToolResultError(err.Error()), nil
	}
	if name == "" {
		return mcp.NewToolResultError("必须先知道好友姓名"), nil
	}
	if name == "刘洋" {
		num = "1390258889009"
	}

	if name == "lucy" {
		num = "0528905"
	}

	text := fmt.Sprintf("hi, %s 的手机号 m ,%s", name, num)
	return mcp.NewToolResultText(text), nil
}
