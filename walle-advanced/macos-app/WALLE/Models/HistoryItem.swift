import Foundation

struct HistoryItem: Identifiable {
    let id: UUID
    var input: String
    var type: InputType
    var status: ProcessStatus
    var result: String?
    var intent: String?
    var timestamp: Date
    
    init(input: String, type: InputType, status: ProcessStatus, result: String? = nil, intent: String? = nil) {
        self.id = UUID()
        self.input = input
        self.type = type
        self.status = status
        self.result = result
        self.intent = intent
        self.timestamp = Date()
    }
}

enum InputType {
    case text
    case voice
}

enum ProcessStatus {
    case processing
    case success
    case failed
}
