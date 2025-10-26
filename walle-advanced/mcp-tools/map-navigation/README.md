# Map Navigation MCP Server

地图导航 MCP Server,为 WALL-E 提供地图导航相关工具。

## 功能特性

### 工具列表

1. **navigate** - 路线导航
   - 打开地图应用进行路线规划
   - 支持多种出行方式(驾车、公交、步行)
   - 支持多个地图服务(百度地图、高德地图、Google Maps)

2. **search_location** - 地点搜索
   - 搜索指定地点
   - 支持城市限定
   - 可选返回详细位置信息(需配置 API Key)

3. **get_current_location** - 获取当前位置
   - 基于 IP 地址获取当前位置
   - 返回城市、省份、国家、坐标信息

### 支持的地图服务

- **百度地图** (Baidu Maps) - 国内推荐,默认选项
- **高德地图** (Amap) - 国内推荐
- **Google Maps** - 海外推荐

## 安装

```bash
npm install
```

## 配置

1. 复制环境变量配置文件:
```bash
cp .env.example .env
```

2. (可选)编辑 `.env` 文件,配置 API Key:
```env
DEFAULT_MAP_SERVICE=baidu
BAIDU_MAP_API_KEY=your_baidu_api_key
AMAP_API_KEY=your_amap_api_key
GOOGLE_MAPS_API_KEY=your_google_api_key
```

> **注意**: API Key 仅在需要获取详细位置信息时使用,基本的导航和搜索功能无需 API Key。

## 使用

### 构建

```bash
npm run build
```

### 运行

```bash
npm start
```

### 开发模式

```bash
npm run dev
```

### 测试

```bash
# 运行所有测试
npm test

# 监听模式
npm run test:watch
```

## 工具使用示例

### 1. navigate - 路线导航

从上海到北京的公交导航:

```json
{
  "name": "navigate",
  "arguments": {
    "origin": "上海",
    "destination": "北京",
    "mode": "transit",
    "mapService": "baidu"
  }
}
```

响应:
```json
{
  "success": true,
  "message": "✅ 成功打开 百度地图\n\n📍 起点：上海\n📍 终点：北京\n🚗 方式：公交\n🔗 导航链接：https://map.baidu.com/direction?...",
  "url": "https://map.baidu.com/direction?..."
}
```

### 2. search_location - 地点搜索

搜索上海的东方明珠:

```json
{
  "name": "search_location",
  "arguments": {
    "query": "东方明珠",
    "city": "上海",
    "mapService": "baidu"
  }
}
```

响应:
```json
{
  "success": true,
  "message": "✅ 已在百度地图搜索: 东方明珠\n🔗 https://map.baidu.com/?query=...\n\n📍 搜索结果:\n1. 东方明珠广播电视塔 - 上海市浦东新区世纪大道1号",
  "url": "https://map.baidu.com/?query=...",
  "results": [...]
}
```

### 3. get_current_location - 获取当前位置

```json
{
  "name": "get_current_location",
  "arguments": {}
}
```

响应:
```json
{
  "success": true,
  "message": "📍 当前位置: China Shanghai Shanghai\n🌐 坐标: 31.2304, 121.4737\n🔍 IP: 123.45.67.89",
  "location": {
    "city": "Shanghai",
    "province": "Shanghai",
    "country": "China",
    "location": {
      "lat": 31.2304,
      "lng": 121.4737
    },
    "ip": "123.45.67.89"
  }
}
```

## 项目结构

```
map-navigation/
├── src/
│   ├── index.ts              # MCP Server 入口
│   ├── config.ts             # 配置管理
│   ├── tools/
│   │   ├── navigate.ts       # 路线导航工具
│   │   ├── search_location.ts  # 地点搜索工具
│   │   └── get_current_location.ts  # 获取位置工具
│   ├── services/
│   │   ├── baidu_map.ts      # 百度地图服务
│   │   ├── amap.ts           # 高德地图服务
│   │   └── google_maps.ts    # Google Maps 服务
│   └── utils/
│       ├── browser.ts        # 浏览器工具
│       └── logger.ts         # 日志工具
├── tests/                    # 测试文件
├── package.json
├── tsconfig.json
└── README.md
```

## MCP 协议接口

本 MCP Server 实现了以下接口:

- `list_tools` - 返回可用工具列表
- `call_tool` - 执行工具调用

## 依赖

- `@modelcontextprotocol/sdk` - MCP SDK
- `open` - 打开浏览器
- `axios` - HTTP 客户端

## 开发

### 添加新工具

1. 在 `src/tools/` 创建新工具文件
2. 实现工具逻辑
3. 在 `src/index.ts` 中注册工具
4. 添加测试文件

### 添加新地图服务

1. 在 `src/services/` 创建新服务文件
2. 实现 URL 生成和 API 调用逻辑
3. 在相关工具中集成新服务

## API Key 申请

### 百度地图 API

1. 访问 [百度地图开放平台](https://lbsyun.baidu.com/)
2. 注册开发者账号
3. 创建应用,获取 AK(API Key)

### 高德地图 API

1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册开发者账号
3. 创建应用,获取 Key

### Google Maps API

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 启用 Maps JavaScript API 和 Places API
3. 创建凭据,获取 API Key

## 许可证

MIT

---

**让 AI 成为你的桌面助手!** ✨
