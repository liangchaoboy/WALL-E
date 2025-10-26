import SwiftUI

struct InputWindow: View {
    @State private var inputText: String = ""
    @State private var recognizedText: String = ""
    @State private var isRecording: Bool = false
    @State private var history: [HistoryItem] = []
    
    var voiceCoordinator: VoiceInputCoordinator?
    var grpcClient: GRPCClient?
    
    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Text("WALL-E 助手")
                    .font(.title)
                    .fontWeight(.bold)
                Spacer()
                Button(action: clearHistory) {
                    Image(systemName: "trash")
                }
                .buttonStyle(.plain)
            }
            .padding()
            
            HStack {
                TextField("输入指令或点击麦克风说话...", text: $inputText)
                    .textFieldStyle(.roundedBorder)
                    .onSubmit {
                        submitTextInput()
                    }
                
                Button(action: toggleVoiceRecording) {
                    Image(systemName: isRecording ? "mic.fill" : "mic")
                        .foregroundColor(isRecording ? .red : .blue)
                }
                .buttonStyle(.plain)
                .font(.title2)
                .help(isRecording ? "停止录音" : "开始语音输入")
                
                Button(action: submitTextInput) {
                    Image(systemName: "arrow.right.circle.fill")
                        .foregroundColor(.blue)
                }
                .buttonStyle(.plain)
                .font(.title2)
                .disabled(inputText.isEmpty)
            }
            .padding(.horizontal)
            
            if !recognizedText.isEmpty {
                HStack {
                    Text("识别结果:")
                        .foregroundColor(.secondary)
                    Text(recognizedText)
                        .foregroundColor(.primary)
                    Spacer()
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                .background(Color.blue.opacity(0.1))
                .cornerRadius(8)
                .padding(.horizontal)
            }
            
            Divider()
            
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 12) {
                    ForEach(history) { item in
                        HistoryItemView(item: item)
                    }
                }
                .padding()
            }
            .frame(maxHeight: .infinity)
        }
        .frame(width: 500, height: 400)
        .background(Color(NSColor.windowBackgroundColor))
    }
    
    private func toggleVoiceRecording() {
        if isRecording {
            voiceCoordinator?.stopRecording()
            isRecording = false
        } else {
            voiceCoordinator?.startRecording { audioData in
                handleVoiceInput(audioData)
            }
            isRecording = true
        }
    }
    
    private func submitTextInput() {
        guard !inputText.isEmpty else { return }
        
        let item = HistoryItem(
            input: inputText,
            type: .text,
            status: .processing
        )
        history.insert(item, at: 0)
        
        grpcClient?.processTextInput(text: inputText) { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let response):
                    updateHistoryItem(id: item.id, response: response)
                case .failure(let error):
                    updateHistoryItemError(id: item.id, error: error.localizedDescription)
                }
            }
        }
        
        inputText = ""
    }
    
    private func handleVoiceInput(_ audioData: Data) {
        let item = HistoryItem(
            input: "语音输入...",
            type: .voice,
            status: .processing
        )
        history.insert(item, at: 0)
        
        grpcClient?.processVoiceInput(audioData: audioData) { result in
            DispatchQueue.main.async {
                isRecording = false
                
                switch result {
                case .success(let response):
                    recognizedText = response.recognizedText
                    updateHistoryItem(id: item.id, response: response)
                    
                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                        recognizedText = ""
                    }
                case .failure(let error):
                    updateHistoryItemError(id: item.id, error: error.localizedDescription)
                }
            }
        }
    }
    
    private func updateHistoryItem(id: UUID, response: ProcessResponse) {
        if let index = history.firstIndex(where: { $0.id == id }) {
            history[index].status = response.success ? .success : .failed
            history[index].result = response.feedbackText
            history[index].intent = response.intent
        }
    }
    
    private func updateHistoryItemError(id: UUID, error: String) {
        if let index = history.firstIndex(where: { $0.id == id }) {
            history[index].status = .failed
            history[index].result = error
        }
    }
    
    private func clearHistory() {
        history.removeAll()
    }
}

struct HistoryItemView: View {
    let item: HistoryItem
    
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Image(systemName: item.type == .voice ? "mic.fill" : "text.bubble.fill")
                    .foregroundColor(.blue)
                Text(item.input)
                    .font(.body)
                Spacer()
                statusIcon
            }
            
            if let intent = item.intent, !intent.isEmpty {
                Text("意图: \(intent)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            if let result = item.result, !result.isEmpty {
                Text(result)
                    .font(.caption)
                    .foregroundColor(item.status == .success ? .green : .red)
            }
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(8)
    }
    
    @ViewBuilder
    private var statusIcon: some View {
        switch item.status {
        case .processing:
            ProgressView()
                .scaleEffect(0.7)
        case .success:
            Image(systemName: "checkmark.circle.fill")
                .foregroundColor(.green)
        case .failed:
            Image(systemName: "exclamationmark.circle.fill")
                .foregroundColor(.red)
        }
    }
}
