package main

import (
	"fmt"
	"log"
	"net/http"
	"regexp"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"wall-e.qiniu.com/server/fast"
)

func main() {
	router := gin.Default()

	// 配置CORS中间件
	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	// 定义/get-text接口
	router.GET("/get-text", func(c *gin.Context) {
		text := c.Query("text")

		// 参数校验
		if text == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "缺少必要参数'text'"})
			return
		}

		//调用AI服务生成导航URL
		data, url, err := fast.ChatCompletion(text)
		if err != nil {
			log.Printf("导航生成失败: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "导航服务暂时不可用"})
			return
		}
		log.Println("-------------------------------------")
		if url == "" {
			// 使用正则表达式提取URL
			re := regexp.MustCompile(`\[点击这里\]\((.*?)\)`)
			matches := re.FindStringSubmatch(data)
			if len(matches) < 2 {
				fmt.Println("未找到URL")
			} else {
				url = matches[1]
				fmt.Println("提取的URL:", url)
			}
		}

		// 返回标准JSON响应
		c.JSON(http.StatusOK, gin.H{
			"data": data,
			"url":  fmt.Sprint(url),
		})
	})

	// 启动服务
	router.Run(":9004")
}
