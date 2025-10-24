package server

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/sanmu/qwall2/internal/ai"
	"github.com/sanmu/qwall2/internal/config"
	"github.com/sanmu/qwall2/internal/stt"
	"github.com/sanmu/qwall2/pkg/mapprovider"
)

// Server HTTP 服务器
type Server struct {
	config    *config.Config
	sttClient stt.Client
	aiClients map[string]ai.Client
	mux       *http.ServeMux
}

// New 创建服务器
func New(cfg *config.Config) (*Server, error) {
	s := &Server{
		config:    cfg,
		aiClients: make(map[string]ai.Client),
		mux:       http.NewServeMux(),
	}

	// 初始化 STT 客户端
	if err := s.initSTT(); err != nil {
		return nil, fmt.Errorf("初始化 STT 失败: %w", err)
	}

	// 初始化 AI 客户端
	if err := s.initAI(); err != nil {
		return nil, fmt.Errorf("初始化 AI 失败: %w", err)
	}

	// 注册路由
	s.registerRoutes()

	return s, nil
}

// initSTT 初始化 STT 客户端
func (s *Server) initSTT() error {
	// 优先使用阿里云语音识别
	if s.config.STT.AliyunAPIKey != "" {
		log.Printf("🎤 使用阿里云语音识别")
		sttConfig := stt.Config{
			Provider:     stt.ProviderAliyun,
			AliyunAPIKey: s.config.STT.AliyunAPIKey,
			AliyunModel:  s.config.STT.AliyunModel,
		}

		client, err := stt.NewClient(sttConfig)
		if err != nil {
			log.Printf("⚠️  阿里云 STT 初始化失败: %v", err)
			// 继续尝试其他方案
		} else {
			s.sttClient = client
			log.Printf("✅ 阿里云 STT 客户端初始化成功: %s", client.GetProviderName())
			return nil
		}
	}

	// 如果没有阿里云 Key，尝试 OpenAI
	if s.config.STT.OpenAIKey != "" {
		log.Printf("🎤 使用 OpenAI Whisper")
		sttConfig := stt.Config{
			Provider:  stt.ProviderOpenAI,
			OpenAIKey: s.config.STT.OpenAIKey,
			Model:     s.config.STT.Model,
		}

		client, err := stt.NewClient(sttConfig)
		if err != nil {
			log.Printf("⚠️  OpenAI STT 初始化失败: %v", err)
			// 继续尝试其他方案
		} else {
			s.sttClient = client
			log.Printf("✅ OpenAI STT 客户端初始化成功: %s", client.GetProviderName())
			return nil
		}
	}

	// 最后使用本地降级模式
	log.Printf("⚠️  没有可用的在线 STT 服务，使用本地 STT 模式")
	sttConfig := stt.Config{
		Provider:       stt.ProviderLocal,
		EnableFallback: false,
		LocalModelPath: s.config.STT.LocalModelPath,
	}

	client, err := stt.NewClient(sttConfig)
	if err != nil {
		log.Printf("⚠️  本地 STT 初始化失败: %v", err)
		return err
	}

	s.sttClient = client
	log.Printf("✅ 本地 STT 客户端初始化成功: %s", client.GetProviderName())
	return nil
}

// initAI 初始化 AI 客户端
func (s *Server) initAI() error {
	// ChatGPT
	if s.config.AI.ChatGPT.APIKey != "" {
		client, err := ai.NewClient(ai.Config{
			Provider: ai.ProviderChatGPT,
			APIKey:   s.config.AI.ChatGPT.APIKey,
			Model:    s.config.AI.ChatGPT.Model,
			BaseURL:  s.config.AI.ChatGPT.BaseURL,
		})
		if err != nil {
			log.Printf("⚠️  ChatGPT 客户端初始化失败: %v", err)
		} else {
			s.aiClients["chatgpt"] = client
			log.Printf("✅ ChatGPT 客户端初始化成功")
		}
	}

	// Claude
	if s.config.AI.Claude.APIKey != "" {
		client, err := ai.NewClient(ai.Config{
			Provider: ai.ProviderClaude,
			APIKey:   s.config.AI.Claude.APIKey,
			Model:    s.config.AI.Claude.Model,
			BaseURL:  s.config.AI.Claude.BaseURL,
		})
		if err != nil {
			log.Printf("⚠️  Claude 客户端初始化失败: %v", err)
		} else {
			s.aiClients["claude"] = client
			log.Printf("✅ Claude 客户端初始化成功")
		}
	}

	// DeepSeek
	if s.config.AI.DeepSeek.APIKey != "" {
		client, err := ai.NewClient(ai.Config{
			Provider: ai.ProviderDeepSeek,
			APIKey:   s.config.AI.DeepSeek.APIKey,
			Model:    s.config.AI.DeepSeek.Model,
			BaseURL:  s.config.AI.DeepSeek.BaseURL,
		})
		if err != nil {
			log.Printf("⚠️  DeepSeek 客户端初始化失败: %v", err)
		} else {
			s.aiClients["deepseek"] = client
			log.Printf("✅ DeepSeek 客户端初始化成功")
		}
	}

	if len(s.aiClients) == 0 {
		log.Printf("⚠️  没有可用的 AI 客户端，将使用模拟模式")
		// 创建一个模拟的 AI 客户端用于测试
		s.aiClients["mock"] = &mockAIClient{}
	}

	return nil
}

// registerRoutes 注册路由
func (s *Server) registerRoutes() {
	// 静态文件
	fs := http.FileServer(http.Dir("web/static"))
	s.mux.Handle("/static/", http.StripPrefix("/static/", fs))

	// 主页
	s.mux.HandleFunc("/", s.handleIndex)

	// API
	s.mux.HandleFunc("/api/navigate", s.handleNavigate)
	s.mux.HandleFunc("/api/health", s.handleHealth)
}

// Start 启动服务器
func (s *Server) Start() error {
	addr := fmt.Sprintf("%s:%d", s.config.Server.Host, s.config.Server.Port)
	log.Printf("🚀 服务器启动在 http://%s", addr)
	log.Printf("📍 支持的地图：百度地图、高德地图、Google Maps")
	log.Printf("🤖 支持的 AI：%v", s.getAvailableAI())

	return http.ListenAndServe(addr, s.corsMiddleware(s.mux))
}

// getAvailableAI 获取可用的 AI 列表
func (s *Server) getAvailableAI() []string {
	var available []string
	for name := range s.aiClients {
		available = append(available, name)
	}
	return available
}

// corsMiddleware CORS 中间件
func (s *Server) corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

// NavigateRequest 导航请求
type NavigateRequest struct {
	Type        string `json:"type"`         // text or audio
	Input       string `json:"input"`        // 文字输入
	Audio       string `json:"audio"`        // 音频数据（base64）
	Format      string `json:"format"`       // 音频格式
	AIProvider  string `json:"ai_provider"`  // AI 提供商
	MapProvider string `json:"map_provider"` // 地图提供商
}

// NavigateResponse 导航响应
type NavigateResponse struct {
	Success        bool   `json:"success"`
	URL            string `json:"url,omitempty"`
	Start          string `json:"start,omitempty"`
	End            string `json:"end,omitempty"`
	RecognizedText string `json:"recognized_text,omitempty"`
	STTProvider    string `json:"stt_provider,omitempty"`
	AIProvider     string `json:"ai_provider,omitempty"`
	MapProvider    string `json:"map_provider,omitempty"`
	Error          string `json:"error,omitempty"`
	ErrorType      string `json:"error_type,omitempty"`
}

// handleNavigate 处理导航请求
func (s *Server) handleNavigate(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// 解析请求
	var req NavigateRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.sendError(w, "invalid_request", "无效的请求格式: "+err.Error())
		return
	}

	ctx, cancel := context.WithTimeout(r.Context(), 30*time.Second)
	defer cancel()

	var text string
	var sttProvider string

	// 1. STT 处理（如果是语音）
	if req.Type == "audio" {
		result, err := s.transcribeAudio(ctx, req.Audio, req.Format)
		if err != nil {
			s.sendError(w, "stt_failed", "语音识别失败: "+err.Error())
			return
		}
		text = result.Text
		sttProvider = string(result.Provider)

		// 检查是否是语音识别服务不可用的提示
		if strings.Contains(text, "语音识别服务暂时不可用") {
			s.sendError(w, "stt_unavailable", "语音识别服务暂时不可用，请使用文字输入功能")
			return
		}

		log.Printf("🎤 STT 结果: %s (提供商: %s)", text, sttProvider)
	} else {
		text = req.Input
	}

	// 2. AI 提取起点终点
	aiProvider := req.AIProvider
	if aiProvider == "" {
		aiProvider = s.config.AI.DefaultProvider
	}

	aiClient, ok := s.aiClients[aiProvider]
	if !ok {
		s.sendError(w, "ai_not_available", fmt.Sprintf("AI 提供商 %s 不可用", aiProvider))
		return
	}

	intent, err := aiClient.ExtractNavigationIntent(ctx, text)
	if err != nil {
		s.sendError(w, "extraction_failed", "提取导航意图失败: "+err.Error())
		return
	}

	log.Printf("🧠 AI 提取结果: %s → %s (提供商: %s)", intent.Start, intent.End, aiProvider)

	// 验证起点终点
	if intent.Start == "" && intent.End == "" {
		s.sendError(w, "no_location", "未能识别起点和终点")
		return
	}

	// 3. 生成地图 URL
	mapProvider := req.MapProvider
	if mapProvider == "" {
		mapProvider = s.config.Map.DefaultProvider
	}

	mapURL, err := s.generateMapURL(intent.Start, intent.End, mapProvider)
	if err != nil {
		s.sendError(w, "map_generation_failed", "生成地图 URL 失败: "+err.Error())
		return
	}

	// 4. 返回成功响应
	resp := NavigateResponse{
		Success:        true,
		URL:            mapURL,
		Start:          intent.Start,
		End:            intent.End,
		RecognizedText: text,
		STTProvider:    sttProvider,
		AIProvider:     aiProvider,
		MapProvider:    mapProvider,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// transcribeAudio 转录音频
func (s *Server) transcribeAudio(ctx context.Context, audioBase64, format string) (*stt.Result, error) {
	// 解码 base64
	// 移除 data URL 前缀
	if strings.Contains(audioBase64, ",") {
		parts := strings.SplitN(audioBase64, ",", 2)
		audioBase64 = parts[1]
	}

	audioData, err := base64.StdEncoding.DecodeString(audioBase64)
	if err != nil {
		return nil, fmt.Errorf("解码音频数据失败: %w", err)
	}

	// 调用 STT
	reader := strings.NewReader(string(audioData))
	return s.sttClient.TranscribeAudio(ctx, reader, format)
}

// generateMapURL 生成地图 URL
func (s *Server) generateMapURL(start, end, provider string) (string, error) {
	params := mapprovider.NavigationParams{
		Start:       start,
		End:         end,
		MapProvider: mapprovider.MapProvider(provider),
	}

	return mapprovider.GenerateNavigationURL(params)
}

// sendError 发送错误响应
func (s *Server) sendError(w http.ResponseWriter, errorType, message string) {
	resp := NavigateResponse{
		Success:   false,
		Error:     message,
		ErrorType: errorType,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusBadRequest)
	json.NewEncoder(w).Encode(resp)
}

// handleHealth 健康检查
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	health := map[string]interface{}{
		"status": "ok",
		"ai":     s.getAvailableAI(),
		"stt":    s.sttClient.GetProviderName(),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(health)
}

// handleIndex 主页
func (s *Server) handleIndex(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}

	http.ServeFile(w, r, "web/index.html")
}

// emptySTTClient 空的 STT 客户端实现
type emptySTTClient struct{}

func (c *emptySTTClient) TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*stt.Result, error) {
	return nil, fmt.Errorf("STT 功能不可用：请配置 OpenAI API Key")
}

func (c *emptySTTClient) GetProviderName() string {
	return "Empty (需要配置 API Key)"
}

// mockAIClient 模拟 AI 客户端实现
type mockAIClient struct{}

func (c *mockAIClient) ExtractNavigationIntent(ctx context.Context, text string) (*ai.NavigationIntent, error) {
	// 简单的模拟逻辑，用于测试
	if strings.Contains(text, "到") || strings.Contains(text, "去") {
		parts := strings.Split(text, "到")
		if len(parts) == 2 {
			return &ai.NavigationIntent{
				Start: strings.TrimSpace(parts[0]),
				End:   strings.TrimSpace(parts[1]),
			}, nil
		}

		// 尝试 "去" 分割
		parts = strings.Split(text, "去")
		if len(parts) == 2 {
			return &ai.NavigationIntent{
				Start: "当前位置",
				End:   strings.TrimSpace(parts[1]),
			}, nil
		}
	}

	// 如果无法解析，返回默认值
	return &ai.NavigationIntent{
		Start: "当前位置",
		End:   text,
	}, nil
}

func (c *mockAIClient) GetProviderName() string {
	return "Mock (测试模式)"
}
