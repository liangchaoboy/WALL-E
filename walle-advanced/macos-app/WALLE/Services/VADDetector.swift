import Foundation
import AVFoundation

class VADDetector {
    var onSpeechEnd: (() -> Void)?
    
    private var silenceThreshold: Float = 0.01
    private var silenceDuration: TimeInterval = 1.5
    private var lastSpeechTime: Date?
    private var isDetecting = false
    private var detectionTask: Task<Void, Never>?
    
    func startDetecting(audioStream: AsyncStream<AVAudioPCMBuffer>?) {
        guard !isDetecting, let stream = audioStream else { return }
        
        isDetecting = true
        lastSpeechTime = Date()
        
        detectionTask = Task {
            for await buffer in stream {
                await processBuffer(buffer)
            }
        }
    }
    
    func stopDetecting() {
        isDetecting = false
        detectionTask?.cancel()
        detectionTask = nil
    }
    
    func updateThreshold(_ threshold: Float) {
        silenceThreshold = max(0.0, min(1.0, threshold))
    }
    
    func updateSilenceDuration(_ duration: TimeInterval) {
        silenceDuration = max(0.5, min(5.0, duration))
    }
    
    private func processBuffer(_ buffer: AVAudioPCMBuffer) async {
        guard let channelData = buffer.floatChannelData else { return }
        
        let channelDataValue = channelData.pointee
        let frameLength = Int(buffer.frameLength)
        
        var sum: Float = 0
        for i in 0..<frameLength {
            sum += abs(channelDataValue[i])
        }
        let averageAmplitude = sum / Float(frameLength)
        
        if averageAmplitude > silenceThreshold {
            lastSpeechTime = Date()
        } else {
            if let lastSpeech = lastSpeechTime,
               Date().timeIntervalSince(lastSpeech) >= silenceDuration {
                await MainActor.run {
                    onSpeechEnd?()
                    stopDetecting()
                }
            }
        }
    }
}
