import Foundation

struct AudioConfig {
    static let sampleRate: Double = 16000
    static let channels: UInt32 = 1
    static let bitDepth: Int = 16
    
    static let vadSilenceThreshold: Float = 0.02
    static let vadSilenceDuration: TimeInterval = 1.5
    
    static let maxRecordingDuration: TimeInterval = 30.0
    static let minRecordingDuration: TimeInterval = 0.5
}

struct WakeWordConfig {
    static let defaultWakeWord = "小七小七"
    static let sensitivity: Float = 0.5
    static let modelPath = "Resources/Models/wakeword.ppn"
}

struct GRPCConfig {
    static let defaultHost = "localhost"
    static let defaultPort = 50051
    static let connectionTimeout: TimeInterval = 5.0
    static let requestTimeout: TimeInterval = 30.0
}
