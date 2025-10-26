import Foundation

struct AudioConfig {
    static let sampleRate: Double = 16000
    static let channels: UInt32 = 1
    static let bitDepth: Int = 16
    
    static let bufferSize: UInt32 = 4096
    
    static let wakeWord: String = "小七小七"
    static let defaultSensitivity: Float = 0.5
    
    static let vadThreshold: Float = 0.01
    static let silenceDuration: TimeInterval = 1.5
    
    static let maxRecordingDuration: TimeInterval = 60.0
}

struct GRPCConfig {
    static let defaultServerURL = "localhost:50051"
    static let connectionTimeout: TimeInterval = 10.0
    static let requestTimeout: TimeInterval = 30.0
}

struct AppConfig {
    static let appName = "WALL-E"
    static let appVersion = "1.0.0"
    static let bundleIdentifier = "com.walle.desktop"
    
    static let minSystemVersion = "13.0"
}
