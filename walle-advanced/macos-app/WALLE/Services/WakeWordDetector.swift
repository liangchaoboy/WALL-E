import Foundation
import AVFoundation

class WakeWordDetector {
    var onWakeWordDetected: (() -> Void)?
    private var audioEngine: AVAudioEngine?
    private var isListening = false
    
    private var sensitivity: Float = 0.5
    
    init() {
        setupAudioEngine()
    }
    
    private func setupAudioEngine() {
        audioEngine = AVAudioEngine()
        
        guard let inputNode = audioEngine?.inputNode else {
            print("Failed to get audio input node")
            return
        }
        
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, time in
            self?.processAudioBuffer(buffer)
        }
    }
    
    func startListening() {
        guard !isListening else { return }
        
        do {
            try audioEngine?.start()
            isListening = true
            print("Wake word detector started")
        } catch {
            print("Failed to start audio engine: \(error)")
        }
    }
    
    func stopListening() {
        guard isListening else { return }
        
        audioEngine?.stop()
        audioEngine?.inputNode.removeTap(onBus: 0)
        isListening = false
        print("Wake word detector stopped")
    }
    
    func updateSensitivity(_ newSensitivity: Float) {
        sensitivity = max(0.0, min(1.0, newSensitivity))
    }
    
    private func processAudioBuffer(_ buffer: AVAudioPCMBuffer) {
        guard let channelData = buffer.floatChannelData else { return }
        
        let channelDataValue = channelData.pointee
        let channelDataValueArray = stride(from: 0, to: Int(buffer.frameLength), by: buffer.stride)
            .map { channelDataValue[$0] }
        
        if detectWakeWord(in: channelDataValueArray) {
            DispatchQueue.main.async { [weak self] in
                self?.onWakeWordDetected?()
            }
        }
    }
    
    private func detectWakeWord(in audioData: [Float]) -> Bool {
        let averageAmplitude = audioData.reduce(0, { $0 + abs($1) }) / Float(audioData.count)
        let threshold = 0.1 * sensitivity
        
        if averageAmplitude > threshold {
            return true
        }
        
        return false
    }
}
