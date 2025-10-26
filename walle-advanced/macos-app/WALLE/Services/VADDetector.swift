import Foundation
import AVFoundation

class VADDetector {
    private let silenceThreshold: Float = 0.02
    private let silenceDuration: TimeInterval = 1.5
    private var lastVoiceTime: Date?
    private var isSpeaking = false
    
    func processSample(_ buffer: AVAudioPCMBuffer) -> VoiceActivityState {
        let energy = calculateEnergy(buffer)
        let hasVoice = energy > silenceThreshold
        
        if hasVoice {
            lastVoiceTime = Date()
            if !isSpeaking {
                isSpeaking = true
                return .speechStarted
            }
            return .speaking
        } else {
            if isSpeaking {
                if let lastVoice = lastVoiceTime,
                   Date().timeIntervalSince(lastVoice) > silenceDuration {
                    isSpeaking = false
                    return .speechEnded
                }
            }
            return .silence
        }
    }
    
    func reset() {
        isSpeaking = false
        lastVoiceTime = nil
    }
    
    private func calculateEnergy(_ buffer: AVAudioPCMBuffer) -> Float {
        guard let channelData = buffer.floatChannelData else { return 0.0 }
        
        let channelDataValue = channelData.pointee
        let frameLength = Int(buffer.frameLength)
        
        var sum: Float = 0.0
        for i in 0..<frameLength {
            let sample = channelDataValue[i]
            sum += sample * sample
        }
        
        let rms = sqrt(sum / Float(frameLength))
        return rms
    }
}

enum VoiceActivityState {
    case silence
    case speechStarted
    case speaking
    case speechEnded
}
