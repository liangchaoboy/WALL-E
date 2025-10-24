# Makefile for qwall2-mcp

.PHONY: all build test clean run install help

# 默认目标
all: build

# 构建项目
build:
	@echo "🔨 构建 qwall2-mcp..."
	@go build -o qwall2-mcp -ldflags="-s -w" main.go
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

# 运行程序
run:
	@echo "🚀 运行 qwall2-mcp..."
	@go run main.go

# 清理构建文件
clean:
	@echo "🧹 清理构建文件..."
	@rm -f qwall2-mcp
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
	@cp qwall2-mcp $(GOPATH)/bin/
	@echo "✅ 安装完成！可以使用 'qwall2-mcp' 命令运行"

# 帮助信息
help:
	@echo "QWall2 MCP 服务器 - Makefile 命令"
	@echo ""
	@echo "使用方法: make [target]"
	@echo ""
	@echo "可用命令:"
	@echo "  build      - 编译项目"
	@echo "  test       - 运行测试"
	@echo "  coverage   - 生成测试覆盖率报告"
	@echo "  run        - 运行程序"
	@echo "  clean      - 清理构建文件"
	@echo "  deps       - 安装依赖"
	@echo "  fmt        - 格式化代码"
	@echo "  vet        - 代码检查"
	@echo "  install    - 安装到系统"
	@echo "  help       - 显示此帮助信息"
