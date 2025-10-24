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

	// 检查音频文件是否存在且不为空
	info, err := os.Stat(tmpFile)
	if err != nil {
		return nil, fmt.Errorf("音频文件不存在: %w", err)
	}

	if info.Size() == 0 {
		return nil, fmt.Errorf("音频文件为空")
	}

	// 尝试多种本地 STT 方案
	var result *Result

	// 方案 1: 使用 whisper.cpp (如果已安装)
	result, err = c.tryWhisperCPP(ctx, tmpFile)
	if err == nil {
		return result, nil
	}

	// 方案 2: 使用 vosk (如果已安装)
	result, err = c.tryVosk(ctx, tmpFile)
	if err == nil {
		return result, nil
	}

	// 方案 3: 使用 Qwen2-Audio (如果已安装)
	result, err = c.tryQwen2Audio(ctx, tmpFile)
	if err == nil {
		return result, nil
	}

	// 方案 4: 返回友好的提示信息
	return &Result{
		Text:     "语音识别服务暂时不可用，请使用文字输入功能",
		Language: "zh",
		Provider: ProviderLocal,
	}, nil
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

// tryQwen2Audio 尝试使用 Qwen2-Audio
func (c *LocalClient) tryQwen2Audio(ctx context.Context, audioFile string) (*Result, error) {
	// 检查 Python 是否存在
	_, err := exec.LookPath("python3")
	if err != nil {
		_, err = exec.LookPath("python")
		if err != nil {
			return nil, fmt.Errorf("Python 未安装: %w", err)
		}
	}

	// 创建临时的 Python 脚本
	tmpDir := os.TempDir()
	scriptFile := filepath.Join(tmpDir, fmt.Sprintf("qwen2_audio_%d.py", os.Getpid()))
	defer os.Remove(scriptFile)

	// 写入 Qwen2-Audio 脚本
	script := `#!/usr/bin/env python3
import sys
import os
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa
import soundfile as sf

def transcribe_audio(audio_file):
    try:
        # 使用较小的模型以提高性能
        model_id = "Qwen/Qwen2-Audio-1.5B"  # 使用 1.5B 模型，更轻量
        
        # 检查是否有 GPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        
        # 加载模型
        processor = AutoProcessor.from_pretrained(model_id)
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            device_map="auto" if device == "cuda" else None
        )
        
        if device == "cpu":
            model = model.to(device)
        
        # 加载音频
        audio, sr = librosa.load(audio_file, sr=16000)
        
        # 处理音频
        inputs = processor(
            audio=audio,
            sampling_rate=16000,
            return_tensors="pt"
        )
        
        # 将输入移到设备
        if device == "cuda":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # 转录
        with torch.no_grad():
            generated_ids = model.generate(
                inputs["input_features"],
                max_new_tokens=256,  # 减少生成长度
                do_sample=False,
                num_beams=1,
                pad_token_id=processor.tokenizer.eos_token_id
            )
        
        # 解码结果
        transcription = processor.batch_decode(
            generated_ids, 
            skip_special_tokens=True
        )[0]
        
        print(transcription)
        return True
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <audio_file>", file=sys.stderr)
        sys.exit(1)
    
    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"Audio file not found: {audio_file}", file=sys.stderr)
        sys.exit(1)
    
    success = transcribe_audio(audio_file)
    sys.exit(0 if success else 1)
`

	if err := os.WriteFile(scriptFile, []byte(script), 0755); err != nil {
		return nil, fmt.Errorf("创建脚本文件失败: %w", err)
	}

	// 运行脚本
	var cmd *exec.Cmd
	if _, err := exec.LookPath("python3"); err == nil {
		cmd = exec.CommandContext(ctx, "python3", scriptFile, audioFile)
	} else {
		cmd = exec.CommandContext(ctx, "python", scriptFile, audioFile)
	}

	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("Qwen2-Audio 执行失败: %w, 输出: %s", err, string(output))
	}

	// 解析输出
	transcription := strings.TrimSpace(string(output))
	if transcription == "" {
		return nil, fmt.Errorf("Qwen2-Audio 返回空结果")
	}

	return &Result{
		Text:     transcription,
		Language: "zh",
		Provider: ProviderLocal,
	}, nil
}

// GetProviderName 获取提供商名称
func (c *LocalClient) GetProviderName() string {
	return "Local STT (whisper.cpp/vosk/qwen2-audio)"
}
