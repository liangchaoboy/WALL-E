import Foundation

class GRPCClient {
    private let host: String
    private let port: Int
    private var isConnected = false
    
    init(host: String, port: Int) {
        self.host = host
        self.port = port
        connect()
    }
    
    func connect() {
        print("Connecting to gRPC server at \(host):\(port)")
        isConnected = true
    }
    
    func disconnect() {
        print("Disconnecting from gRPC server")
        isConnected = false
    }
    
    func processTextInput(text: String, completion: @escaping (Result<ProcessResponse, Error>) -> Void) {
        guard isConnected else {
            completion(.failure(GRPCError.notConnected))
            return
        }
        
        DispatchQueue.global(qos: .userInitiated).async {
            Thread.sleep(forTimeInterval: 1.0)
            
            let response = ProcessResponse(
                intent: "navigate_map",
                parameters: ["destination": text],
                feedbackText: "已为您打开地图导航到: \(text)",
                success: true,
                recognizedText: text
            )
            
            DispatchQueue.main.async {
                completion(.success(response))
            }
        }
    }
    
    func processVoiceInput(audioData: Data, completion: @escaping (Result<ProcessResponse, Error>) -> Void) {
        guard isConnected else {
            completion(.failure(GRPCError.notConnected))
            return
        }
        
        DispatchQueue.global(qos: .userInitiated).async {
            Thread.sleep(forTimeInterval: 2.0)
            
            let response = ProcessResponse(
                intent: "query_weather",
                parameters: ["location": "上海", "date": "今天"],
                feedbackText: "上海今天天气晴朗,温度 18-25°C",
                success: true,
                recognizedText: "查询上海今天的天气"
            )
            
            DispatchQueue.main.async {
                completion(.success(response))
            }
        }
    }
}

enum GRPCError: Error {
    case notConnected
    case invalidResponse
    case serverError(String)
}

struct ProcessResponse {
    let intent: String
    let parameters: [String: String]
    let feedbackText: String
    let success: Bool
    let recognizedText: String
}
