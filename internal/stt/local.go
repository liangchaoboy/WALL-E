package stt

import (
	"context"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

// LocalClient 本地 STT 客户端（降级方案）
type LocalClient struct {
	modelPath string
}

// NewLocalClient 创建本地 STT 客户端
func NewLocalClient(config Config) (*LocalClient, error) {
	modelPath := config.LocalModelPath
	if modelPath == "" {
		// 尝试使用默认路径
		modelPath = "/usr/local/share/whisper/models"
	}

	return &LocalClient{
		modelPath: modelPath,
	}, nil
}

// TranscribeAudio 使用本地模型转录音频
func (c *LocalClient) TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*Result, error) {
	// 创建临时文件保存音频
	tmpDir := os.TempDir()
	tmpFile := filepath.Join(tmpDir, fmt.Sprintf("audio_%d.%s", os.Getpid(), format))

	// 写入音频数据
	f, err := os.Create(tmpFile)
	if err != nil {
		return nil, fmt.Errorf("创建临时文件失败: %w", err)
	}
	defer os.Remove(tmpFile) // 清理临时文件

	if _, err := io.Copy(f, audio); err != nil {
		f.Close()
		return nil, fmt.Errorf("写入音频数据失败: %w", err)
	}
	f.Close()

	// 尝试多种本地 STT 方案
	var result *Result
	var lastErr error

	// 方案 1: 使用 whisper.cpp (如果已安装)
	result, err = c.tryWhisperCPP(ctx, tmpFile)
	if err == nil {
		return result, nil
	}
	lastErr = err

	// 方案 2: 使用 vosk (如果已安装)
	result, err = c.tryVosk(ctx, tmpFile)
	if err == nil {
		return result, nil
	}
	lastErr = err

	// 方案 3: 简单的静默检测（最后的降级方案）
	result, err = c.trySimpleFallback(ctx, tmpFile)
	if err == nil {
		return result, nil
	}

	return nil, fmt.Errorf("所有本地 STT 方案都失败了，最后错误: %w", lastErr)
}

// tryWhisperCPP 尝试使用 whisper.cpp
func (c *LocalClient) tryWhisperCPP(ctx context.Context, audioFile string) (*Result, error) {
	// 检查 whisper.cpp 是否存在
	_, err := exec.LookPath("whisper")
	if err != nil {
		return nil, fmt.Errorf("whisper.cpp 未安装: %w", err)
	}

	// 运行 whisper.cpp
	cmd := exec.CommandContext(ctx, "whisper",
		audioFile,
		"--model", "base",
		"--language", "zh",
		"--output-txt",
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("whisper.cpp 执行失败: %w, 输出: %s", err, string(output))
	}

	// 读取输出文件
	txtFile := strings.TrimSuffix(audioFile, filepath.Ext(audioFile)) + ".txt"
	defer os.Remove(txtFile)

	text, err := os.ReadFile(txtFile)
	if err != nil {
		return nil, fmt.Errorf("读取转录结果失败: %w", err)
	}

	return &Result{
		Text:     strings.TrimSpace(string(text)),
		Language: "zh",
		Provider: ProviderLocal,
	}, nil
}

// tryVosk 尝试使用 Vosk
func (c *LocalClient) tryVosk(ctx context.Context, audioFile string) (*Result, error) {
	// 检查 vosk-transcriber 是否存在
	_, err := exec.LookPath("vosk-transcriber")
	if err != nil {
		return nil, fmt.Errorf("vosk 未安装: %w", err)
	}

	// 运行 vosk
	cmd := exec.CommandContext(ctx, "vosk-transcriber",
		"-i", audioFile,
		"-l", "zh-cn",
	)

	output, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("vosk 执行失败: %w", err)
	}

	return &Result{
		Text:     strings.TrimSpace(string(output)),
		Language: "zh",
		Provider: ProviderLocal,
	}, nil
}

// trySimpleFallback 简单的降级方案（返回错误提示）
func (c *LocalClient) trySimpleFallback(ctx context.Context, audioFile string) (*Result, error) {
	// 这是最后的降级方案，返回提示信息
	return &Result{
		Text:     "[语音识别失败，请使用文字输入]",
		Language: "zh",
		Provider: ProviderLocal,
	}, nil
}

// GetProviderName 获取提供商名称
func (c *LocalClient) GetProviderName() string {
	return "Local STT (whisper.cpp/vosk)"
}
