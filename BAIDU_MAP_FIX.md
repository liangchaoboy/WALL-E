# 百度地图 URL 修复说明

## 问题描述

用户反馈："从 Claude 输入 '从北京到上海'，浏览器会跳转到错误的页面"

**症状：**
- 浏览器打开的初始 URL 会自动跳转到 `https://map.baidu.com/@12968049,4834747,13z`
- 无法显示路线规划结果

## 根本原因

百度地图的路线规划 API 需要 `region`（搜索区域）参数，否则无法正确处理地名查询。

## 修复方案

### 修改内容

**文件：** [`pkg/mapprovider/provider.go`](file:///Users/sanmu/eva/qwall2/pkg/mapprovider/provider.go)

1. **添加 `region` 参数**：从终点地址中提取城市名称
2. **新增 `extractCityName` 函数**：智能提取地址中的城市名称

### URL 对比

**修复前（缺少 region）：**
```
http://api.map.baidu.com/direction?destination=上海&mode=transit&origin=北京&output=html&src=webapp.qwall2.navigation
```

**修复后（包含 region）：**
```
http://api.map.baidu.com/direction?destination=上海&mode=transit&origin=北京&output=html&region=上海&src=webapp.qwall2.navigation
```

## 应用更新

### 第 1 步：确认编译时间

```bash
ls -lh /Users/sanmu/eva/qwall2/qwall2-mcp
```

应该看到最新的编译时间（刚才编译的）。

### 第 2 步：重启 Claude Desktop

**重要：必须完全退出 Claude Desktop！**

1. 点击菜单栏的 Claude 图标
2. 选择 "Quit Claude"（或按 `Cmd + Q`）
3. 确保 Claude 完全退出（不是最小化）
4. 重新打开 Claude Desktop

### 第 3 步：测试导航

在 Claude Desktop 中输入：

```
从北京到上海
```

**预期结果：**
- ✅ 浏览器打开百度地图
- ✅ 显示从北京到上海的公交路线规划
- ✅ 不再跳转到错误页面

## 技术细节

### extractCityName 函数

这个函数负责从地址中智能提取城市名称：

```go
func extractCityName(address string) string {
    // 1. 检查是否以常见城市名开头
    cities := []string{
        "北京", "上海", "天津", "重庆",
        "广州", "深圳", "杭州", "成都", "西安", "南京",
        // ... 更多城市
    }
    
    for _, city := range cities {
        if strings.HasPrefix(address, city) {
            return city  // 返回匹配的城市名
        }
    }
    
    // 2. 如果地址很短（≤12字节），可能本身就是城市名
    if len(address) <= 12 {
        return address
    }
    
    // 3. 默认返回"全国"
    return "全国"
}
```

### 测试示例

| 输入地址 | 提取的城市 | 说明 |
|---------|-----------|------|
| 北京 | 北京 | 直接匹配 |
| 上海东方明珠 | 上海 | 前缀匹配 |
| 深圳南山区 | 深圳 | 前缀匹配 |
| 小城市 | 小城市 | 短地址，直接返回 |
| 某个不知名的地方 | 全国 | 长地址且无匹配，返回全国 |

## 测试结果

所有单元测试通过：

```
✅ TestGenerateBaiduMapURL - PASS
✅ TestGenerateAmapURL - PASS
✅ TestGenerateNavigationURL - PASS
✅ TestGetMapProviderName - PASS
✅ TestIsValidMapProvider - PASS
✅ TestExtractCityName - PASS (7 个测试用例)
```

## URL 参数说明

根据[百度地图官方文档](https://lbsyun.baidu.com/index.php?title=模板:uriapi的web端)：

| 参数 | 必需 | 说明 | 示例值 |
|------|------|------|--------|
| `origin` | ✅ | 起点（支持地名或坐标） | 北京 |
| `destination` | ✅ | 终点（支持地名或坐标） | 上海 |
| `mode` | ✅ | 路线模式 | transit (公交) |
| `region` | ✅ | 搜索区域（城市名） | 上海 |
| `output` | ✅ | 输出格式 | html |
| `src` | ✅ | 应用标识 | webapp.qwall2.navigation |

**关键发现：** `region` 参数虽然在文档中标记为"可选"，但实际上对于地名查询是**必需的**，否则会导致跳转错误。

## 故障排除

### 问题：仍然跳转到错误页面

**可能原因 1：** Claude Desktop 没有完全重启

**解决方法：**
```bash
# 检查是否有 Claude 进程仍在运行
ps aux | grep -i claude | grep -v grep

# 如果有进程，手动结束
killall Claude

# 重新启动 Claude Desktop
open -a Claude
```

**可能原因 2：** 使用了旧版本的程序

**解决方法：**
```bash
# 检查编译时间
ls -lh /Users/sanmu/eva/qwall2/qwall2-mcp

# 如果不是最新的，重新编译
cd /Users/sanmu/eva/qwall2
make build

# 重启 Claude Desktop
```

### 问题：找不到路线

这可能是正常的，因为：
- 某些小城市之间可能没有公交路线
- 可以尝试切换到高德地图

在 Claude 中说：
```
使用高德地图从北京到上海
```

## 完成

**现在百度地图导航应该能正常工作了！** 🎉

如果还有问题，请提供：
1. 您在 Claude 中输入的完整指令
2. 浏览器打开的完整 URL
3. 浏览器最终跳转到的 URL

---

**更新时间：** 2025-10-24  
**修复版本：** v1.1  
**相关文件：**
- [`pkg/mapprovider/provider.go`](file:///Users/sanmu/eva/qwall2/pkg/mapprovider/provider.go)
- [`pkg/mapprovider/provider_test.go`](file:///Users/sanmu/eva/qwall2/pkg/mapprovider/provider_test.go)
