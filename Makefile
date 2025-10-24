# Makefile for qwall2 Web Server

.PHONY: all build test clean run install help server

# 默认目标
all: build

# 构建项目（Web 服务器）
build:
	@echo "🔨 构建 qwall2 Web 服务器..."
	@go build -o qwall2-server -ldflags="-s -w" main.go
	@echo "✅ 构建完成！"

# 运行测试
test:
	@echo "🧪 运行测试..."
	@go test -v ./...

# 测试覆盖率
coverage:
	@echo "📊 生成测试覆盖率报告..."
	@go test -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html
	@echo "✅ 覆盖率报告已生成: coverage.html"

# 运行 Web 服务器
run: build
	@echo "🚀 启动 Web 服务器..."
	@./qwall2-server

# 使用启动脚本运行（推荐）
server:
	@echo "🚀 使用启动脚本运行..."
	@./start.sh

# 清理构建文件
clean:
	@echo "🧹 清理构建文件..."
	@rm -f qwall2-server qwall2-mcp
	@rm -f coverage.out coverage.html
	@echo "✅ 清理完成！"

# 安装依赖
deps:
	@echo "📦 安装依赖..."
	@go mod download
	@go mod tidy
	@echo "✅ 依赖安装完成！"

# 代码格式化
fmt:
	@echo "🎨 格式化代码..."
	@go fmt ./...
	@echo "✅ 格式化完成！"

# 代码检查
vet:
	@echo "🔍 代码检查..."
	@go vet ./...
	@echo "✅ 检查完成！"

# 安装到系统
install: build
	@echo "📥 安装到系统..."
	@cp qwall2-server $(GOPATH)/bin/
	@echo "✅ 安装完成！可以使用 'qwall2-server' 命令运行"

# 帮助信息
help:
	@echo "QWall2 AI 地图导航系统 - Makefile 命令"
	@echo ""
	@echo "使用方法: make [target]"
	@echo ""
	@echo "可用命令:"
	@echo "  build      - 编译项目（生成 qwall2-server）"
	@echo "  test       - 运行测试"
	@echo "  coverage   - 生成测试覆盖率报告"
	@echo "  run        - 直接运行服务器"
	@echo "  server     - 使用启动脚本运行（推荐）"
	@echo "  clean      - 清理构建文件"
	@echo "  deps       - 安装依赖"
	@echo "  fmt        - 格式化代码"
	@echo "  vet        - 代码检查"
	@echo "  install    - 安装到系统"
	@echo "  help       - 显示此帮助信息"
