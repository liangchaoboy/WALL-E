import Foundation
import AVFoundation

class AudioRecorder: NSObject {
    var onRecordingComplete: ((Data) -> Void)?
    var audioStream: AsyncStream<AVAudioPCMBuffer>?
    
    private var audioEngine: AVAudioEngine?
    private var audioFile: AVAudioFile?
    private var isRecording = false
    private var recordedData = Data()
    private var streamContinuation: AsyncStream<AVAudioPCMBuffer>.Continuation?
    
    override init() {
        super.init()
        setupAudioEngine()
    }
    
    private func setupAudioEngine() {
        audioEngine = AVAudioEngine()
        
        audioStream = AsyncStream { continuation in
            self.streamContinuation = continuation
        }
    }
    
    func startRecording() {
        guard !isRecording else { return }
        
        recordedData = Data()
        
        guard let inputNode = audioEngine?.inputNode else {
            print("Failed to get audio input node")
            return
        }
        
        let recordingFormat = AVAudioFormat(
            commonFormat: .pcmFormatInt16,
            sampleRate: 16000,
            channels: 1,
            interleaved: false
        )
        
        guard let format = recordingFormat else {
            print("Failed to create recording format")
            return
        }
        
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let audioFilename = documentsPath.appendingPathComponent("recording_\(Date().timeIntervalSince1970).wav")
        
        do {
            audioFile = try AVAudioFile(forWriting: audioFilename, settings: format.settings)
        } catch {
            print("Failed to create audio file: \(error)")
            return
        }
        
        inputNode.installTap(onBus: 0, bufferSize: 4096, format: inputNode.outputFormat(forBus: 0)) { [weak self] buffer, time in
            guard let self = self else { return }
            
            self.streamContinuation?.yield(buffer)
            
            do {
                try self.audioFile?.write(from: buffer)
                
                if let channelData = buffer.int16ChannelData {
                    let dataPtr = UnsafeBufferPointer(start: channelData[0], count: Int(buffer.frameLength))
                    let data = Data(buffer: dataPtr)
                    self.recordedData.append(data)
                }
            } catch {
                print("Failed to write audio buffer: \(error)")
            }
        }
        
        do {
            try audioEngine?.start()
            isRecording = true
            print("Recording started")
        } catch {
            print("Failed to start recording: \(error)")
        }
    }
    
    func stopRecording() {
        guard isRecording else { return }
        
        audioEngine?.inputNode.removeTap(onBus: 0)
        audioEngine?.stop()
        isRecording = false
        
        streamContinuation?.finish()
        
        print("Recording stopped, data size: \(recordedData.count) bytes")
        onRecordingComplete?(recordedData)
    }
    
    func isCurrentlyRecording() -> Bool {
        return isRecording
    }
}
