import Foundation
import AVFoundation

class AudioRecorder: NSObject {
    private let audioEngine = AVAudioEngine()
    private var isRecording = false
    private var audioBuffer = Data()
    private var recordingStartTime: Date?
    
    private let audioFormat: AVAudioFormat = {
        return AVAudioFormat(
            commonFormat: .pcmFormatInt16,
            sampleRate: 16000,
            channels: 1,
            interleaved: false
        )!
    }()
    
    func startRecording() {
        guard !isRecording else { return }
        
        audioBuffer.removeAll()
        recordingStartTime = Date()
        isRecording = true
        
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, time in
            self?.processAudioBuffer(buffer)
        }
        
        do {
            try audioEngine.start()
            print("Recording started")
        } catch {
            print("Error starting audio engine: \(error.localizedDescription)")
            isRecording = false
        }
    }
    
    func stopRecording() -> Data {
        guard isRecording else { return Data() }
        
        audioEngine.inputNode.removeTap(onBus: 0)
        audioEngine.stop()
        isRecording = false
        
        let duration = Date().timeIntervalSince(recordingStartTime ?? Date())
        print("Recording stopped. Duration: \(duration)s, Size: \(audioBuffer.count) bytes")
        
        return audioBuffer
    }
    
    private func processAudioBuffer(_ buffer: AVAudioPCMBuffer) {
        guard let channelData = buffer.int16ChannelData else { return }
        
        let channelDataValue = channelData.pointee
        let channelDataArray = stride(from: 0, to: Int(buffer.frameLength), by: 1).map { channelDataValue[$0] }
        
        let data = Data(bytes: channelDataArray, count: channelDataArray.count * MemoryLayout<Int16>.size)
        audioBuffer.append(data)
    }
    
    func getRecordingLevel() -> Float {
        guard isRecording else { return 0.0 }
        
        let inputNode = audioEngine.inputNode
        return inputNode.volume
    }
}
