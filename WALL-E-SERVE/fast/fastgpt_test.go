package fast

import (
	"fmt"
	"log"
	"testing"
)

func TestCreateChatCompletion(t *testing.T) {
	request := AIReqData{
		Messages: []ChatCompletionMessage{
			{
				Role:    ChatMessageRoleUser,
				Content: "导航，从长泰广场去七牛云",
			},
		},
	}

	result, err := ChatFromGPT(request)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	if result.Parsed[0].IsJSONContent {
		// JSON 模式：包含结构化数据
		fmt.Printf("JSON 模式结果:\n")
		fmt.Printf("Data: %s\n", result.Parsed[0].ContentData.Data)
		fmt.Printf("URL: %s\n", result.Parsed[0].ContentData.URL)
	} else {
		// 纯文本模式
		fmt.Printf("纯文本结果: %s\n", result.Parsed[0].TextContent)
	}

}
