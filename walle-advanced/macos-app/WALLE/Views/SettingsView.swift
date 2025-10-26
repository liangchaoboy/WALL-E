import SwiftUI

struct SettingsView: View {
    @AppStorage("wakeWord") private var wakeWord: String = "小七小七"
    @AppStorage("sttEngine") private var sttEngine: String = "aliyun"
    @AppStorage("llmProvider") private var llmProvider: String = "chatgpt"
    @AppStorage("hotKeyEnabled") private var hotKeyEnabled: Bool = true
    @AppStorage("launchAtLogin") private var launchAtLogin: Bool = false
    @AppStorage("apiKey") private var apiKey: String = ""
    
    var body: some View {
        TabView {
            GeneralSettingsView(
                wakeWord: $wakeWord,
                hotKeyEnabled: $hotKeyEnabled,
                launchAtLogin: $launchAtLogin
            )
            .tabItem {
                Label("通用", systemImage: "gearshape")
            }
            
            VoiceSettingsView(
                sttEngine: $sttEngine
            )
            .tabItem {
                Label("语音", systemImage: "mic")
            }
            
            AISettingsView(
                llmProvider: $llmProvider,
                apiKey: $apiKey
            )
            .tabItem {
                Label("AI", systemImage: "brain")
            }
        }
        .frame(width: 500, height: 400)
    }
}

struct GeneralSettingsView: View {
    @Binding var wakeWord: String
    @Binding var hotKeyEnabled: Bool
    @Binding var launchAtLogin: Bool
    
    var body: some View {
        Form {
            Section("基本设置") {
                TextField("唤醒词:", text: $wakeWord)
                Toggle("启用全局快捷键 (Cmd+Space)", isOn: $hotKeyEnabled)
                Toggle("开机自启动", isOn: $launchAtLogin)
            }
            
            Section("关于") {
                HStack {
                    Text("版本:")
                    Spacer()
                    Text("1.0.0")
                        .foregroundColor(.secondary)
                }
                
                Button("检查更新") {
                }
                
                Button("查看文档") {
                    if let url = URL(string: "https://github.com/liangchaoboy/WALL-E") {
                        NSWorkspace.shared.open(url)
                    }
                }
            }
        }
        .padding()
    }
}

struct VoiceSettingsView: View {
    @Binding var sttEngine: String
    
    var body: some View {
        Form {
            Section("语音识别") {
                Picker("STT 引擎:", selection: $sttEngine) {
                    Text("阿里云").tag("aliyun")
                    Text("OpenAI Whisper").tag("whisper")
                    Text("本地模型").tag("local")
                }
            }
            
            Section("音频设置") {
                HStack {
                    Text("麦克风:")
                    Spacer()
                    Text("系统默认")
                        .foregroundColor(.secondary)
                }
                
                Button("测试麦克风") {
                }
            }
        }
        .padding()
    }
}

struct AISettingsView: View {
    @Binding var llmProvider: String
    @Binding var apiKey: String
    
    var body: some View {
        Form {
            Section("AI 模型") {
                Picker("LLM 提供商:", selection: $llmProvider) {
                    Text("ChatGPT").tag("chatgpt")
                    Text("Claude").tag("claude")
                    Text("DeepSeek").tag("deepseek")
                }
                
                SecureField("API Key:", text: $apiKey)
                    .help("您的 API 密钥将安全存储在系统钥匙串中")
            }
            
            Section("模型参数") {
                HStack {
                    Text("温度:")
                    Spacer()
                    Text("0.7")
                        .foregroundColor(.secondary)
                }
                
                HStack {
                    Text("上下文长度:")
                    Spacer()
                    Text("10 轮")
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding()
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
    }
}
