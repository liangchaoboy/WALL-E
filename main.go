package main

import (
	"flag"
	"log"
	"os"

	"github.com/sanmu/qwall2/internal/config"
	"github.com/sanmu/qwall2/internal/server"
)

func main() {
	// 命令行参数
	configPath := flag.String("config", "config.yaml", "配置文件路径")
	flag.Parse()

	// 加载配置
	cfg, err := loadConfig(*configPath)
	if err != nil {
		log.Fatalf("⚠️  加载配置失败: %v", err)
	}

	log.Println("🎉 AI 地图导航系统启动")
	log.Println("📍 项目：qwall2 - AI Map Navigation")
	log.Println("────────────────────")

	// 创建服务器
	srv, err := server.New(cfg)
	if err != nil {
		log.Fatalf("❌ 创建服务器失败: %v", err)
	}

	// 启动服务器
	if err := srv.Start(); err != nil {
		log.Fatalf("❌ 启动服务器失败: %v", err)
	}
}

// loadConfig 加载配置
func loadConfig(path string) (*config.Config, error) {
	// 检查配置文件是否存在
	if _, err := os.Stat(path); os.IsNotExist(err) {
		log.Printf("⚠️  配置文件不存在: %s，使用默认配置", path)
		return config.Default(), nil
	}

	return config.Load(path)
}
