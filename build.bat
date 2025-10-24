@echo off
REM 构建脚本 - Windows 版本

echo 🔨 开始编译 qwall2-mcp...

REM 清理旧的构建文件
if exist qwall2-mcp.exe (
    echo 🧹 清理旧的构建文件...
    del /f qwall2-mcp.exe
)

REM 下载依赖
echo 📦 下载依赖...
go mod download

REM 编译
echo ⚙️  编译中...
go build -o qwall2-mcp.exe -ldflags="-s -w" main.go

REM 检查编译结果
if exist qwall2-mcp.exe (
    echo ✅ 编译成功！
    echo 📍 可执行文件：%CD%\qwall2-mcp.exe
    echo.
    echo 运行方式：
    echo   qwall2-mcp.exe
    echo.
    echo 或配置到 Claude Desktop：
    echo   {"command": "%CD%\qwall2-mcp.exe"}
) else (
    echo ❌ 编译失败
    exit /b 1
)
