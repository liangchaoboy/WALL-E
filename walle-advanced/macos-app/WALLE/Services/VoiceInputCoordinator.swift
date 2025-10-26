import Foundation
import AVFoundation

class VoiceInputCoordinator {
    private let wakeWordDetector: WakeWordDetector
    private let audioRecorder: AudioRecorder
    private let vadDetector: VADDetector
    private var grpcClient: GRPCClient?
    
    var onVoiceInput: ((Data) -> Void)?
    private var isListeningForWakeWord = false
    private var isRecordingVoice = false
    
    init(grpcClient: GRPCClient?) {
        self.wakeWordDetector = WakeWordDetector()
        self.audioRecorder = AudioRecorder()
        self.vadDetector = VADDetector()
        self.grpcClient = grpcClient
    }
    
    func startListening() {
        guard !isListeningForWakeWord else { return }
        
        isListeningForWakeWord = true
        
        wakeWordDetector.start { [weak self] in
            self?.handleWakeWordDetected()
        }
    }
    
    func stopListening() {
        wakeWordDetector.stop()
        if isRecordingVoice {
            stopRecording()
        }
        isListeningForWakeWord = false
    }
    
    func startRecording(completion: @escaping (Data) -> Void) {
        guard !isRecordingVoice else { return }
        
        isRecordingVoice = true
        vadDetector.reset()
        audioRecorder.startRecording()
        
        monitorVAD { [weak self] in
            guard let self = self else { return }
            let audioData = self.audioRecorder.stopRecording()
            self.isRecordingVoice = false
            completion(audioData)
        }
    }
    
    func stopRecording() {
        guard isRecordingVoice else { return }
        
        let audioData = audioRecorder.stopRecording()
        isRecordingVoice = false
        onVoiceInput?(audioData)
    }
    
    private func handleWakeWordDetected() {
        print("Wake word detected! Starting recording...")
        
        startRecording { [weak self] audioData in
            self?.onVoiceInput?(audioData)
        }
    }
    
    private func monitorVAD(onSpeechEnd: @escaping () -> Void) {
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            guard let self = self else { return }
            
            while self.isRecordingVoice {
                Thread.sleep(forTimeInterval: 0.1)
            }
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 5.0) {
            if self.isRecordingVoice {
                onSpeechEnd()
            }
        }
    }
}
