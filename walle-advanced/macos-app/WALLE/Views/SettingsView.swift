import SwiftUI

struct SettingsView: View {
    @AppStorage("grpcServerURL") private var grpcServerURL = "localhost:50051"
    @AppStorage("wakeWordSensitivity") private var wakeWordSensitivity = 0.5
    @AppStorage("vadThreshold") private var vadThreshold = 0.6
    @AppStorage("autoStartRecording") private var autoStartRecording = true
    
    var body: some View {
        TabView {
            GeneralSettingsView(
                grpcServerURL: $grpcServerURL,
                autoStartRecording: $autoStartRecording
            )
            .tabItem {
                Label("通用", systemImage: "gear")
            }
            
            VoiceSettingsView(
                wakeWordSensitivity: $wakeWordSensitivity,
                vadThreshold: $vadThreshold
            )
            .tabItem {
                Label("语音", systemImage: "mic")
            }
            
            AboutView()
                .tabItem {
                    Label("关于", systemImage: "info.circle")
                }
        }
        .frame(width: 500, height: 400)
    }
}

struct GeneralSettingsView: View {
    @Binding var grpcServerURL: String
    @Binding var autoStartRecording: Bool
    
    var body: some View {
        Form {
            Section(header: Text("服务器设置")) {
                TextField("gRPC 服务器地址", text: $grpcServerURL)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
            }
            
            Section(header: Text("行为设置")) {
                Toggle("唤醒后自动开始录音", isOn: $autoStartRecording)
            }
        }
        .padding(20)
    }
}

struct VoiceSettingsView: View {
    @Binding var wakeWordSensitivity: Double
    @Binding var vadThreshold: Double
    
    var body: some View {
        Form {
            Section(header: Text("唤醒词设置")) {
                VStack(alignment: .leading) {
                    Text("唤醒词灵敏度: \(String(format: "%.2f", wakeWordSensitivity))")
                    Slider(value: $wakeWordSensitivity, in: 0...1)
                    Text("灵敏度越高,越容易被唤醒,但也可能增加误触发")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Section(header: Text("语音检测设置")) {
                VStack(alignment: .leading) {
                    Text("静音检测阈值: \(String(format: "%.2f", vadThreshold))")
                    Slider(value: $vadThreshold, in: 0...1)
                    Text("阈值越高,需要更长的静音时间才会停止录音")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(20)
    }
}

struct AboutView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "mic.fill")
                .font(.system(size: 60))
                .foregroundColor(.blue)
            
            Text("WALL-E")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("AI 驱动的桌面语音助手")
                .font(.headline)
                .foregroundColor(.secondary)
            
            Text("版本 1.0.0")
                .font(.caption)
                .foregroundColor(.secondary)
            
            Spacer()
            
            Link("GitHub 项目主页", destination: URL(string: "https://github.com/liangchaoboy/WALL-E")!)
                .font(.footnote)
        }
        .padding(40)
    }
}
