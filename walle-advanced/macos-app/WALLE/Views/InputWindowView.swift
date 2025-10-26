import SwiftUI

struct InputWindowView: View {
    @State private var inputText: String = ""
    @State private var recognizedText: String = ""
    @State private var isRecording: Bool = false
    @State private var audioLevel: CGFloat = 0.0
    
    var onVoiceStart: () -> Void
    var onTextSubmit: (String) -> Void
    
    var body: some View {
        ZStack {
            VisualEffectBlur(material: .hudWindow, blendingMode: .behindWindow)
            
            VStack(spacing: 20) {
                Text("WALL-E 语音助手")
                    .font(.title)
                    .fontWeight(.bold)
                
                VStack(spacing: 10) {
                    TextField("输入命令或点击麦克风说话...", text: $inputText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .onSubmit {
                            submitText()
                        }
                    
                    if !recognizedText.isEmpty {
                        Text("识别结果: \(recognizedText)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
                
                HStack(spacing: 20) {
                    Button(action: {
                        toggleRecording()
                    }) {
                        VStack {
                            Image(systemName: isRecording ? "stop.circle.fill" : "mic.circle.fill")
                                .font(.system(size: 48))
                                .foregroundColor(isRecording ? .red : .blue)
                            
                            Text(isRecording ? "停止录音" : "开始语音")
                                .font(.caption)
                        }
                    }
                    .buttonStyle(PlainButtonStyle())
                    
                    Button(action: {
                        submitText()
                    }) {
                        VStack {
                            Image(systemName: "paperplane.circle.fill")
                                .font(.system(size: 48))
                                .foregroundColor(.green)
                            
                            Text("发送")
                                .font(.caption)
                        }
                    }
                    .buttonStyle(PlainButtonStyle())
                    .disabled(inputText.isEmpty)
                }
                
                if isRecording {
                    WaveformView(audioLevel: audioLevel)
                        .frame(height: 50)
                }
                
                Spacer()
            }
            .padding(30)
        }
        .frame(width: 400, height: 300)
    }
    
    func toggleRecording() {
        isRecording.toggle()
        if isRecording {
            onVoiceStart()
        }
    }
    
    func submitText() {
        guard !inputText.isEmpty else { return }
        onTextSubmit(inputText)
        inputText = ""
    }
}

struct VisualEffectBlur: NSViewRepresentable {
    var material: NSVisualEffectView.Material
    var blendingMode: NSVisualEffectView.BlendingMode
    
    func makeNSView(context: Context) -> NSVisualEffectView {
        let view = NSVisualEffectView()
        view.material = material
        view.blendingMode = blendingMode
        view.state = .active
        return view
    }
    
    func updateNSView(_ nsView: NSVisualEffectView, context: Context) {
        nsView.material = material
        nsView.blendingMode = blendingMode
    }
}

struct WaveformView: View {
    var audioLevel: CGFloat
    
    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<20) { index in
                RoundedRectangle(cornerRadius: 2)
                    .fill(Color.blue)
                    .frame(width: 4, height: randomHeight(for: index))
                    .animation(.easeInOut(duration: 0.3), value: audioLevel)
            }
        }
    }
    
    func randomHeight(for index: Int) -> CGFloat {
        let base: CGFloat = 10
        let variation: CGFloat = audioLevel * 30
        return base + CGFloat.random(in: 0...variation)
    }
}
