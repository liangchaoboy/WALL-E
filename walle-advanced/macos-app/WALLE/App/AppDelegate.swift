import Cocoa
import SwiftUI
import Carbon.HIToolbox

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusBarItem: NSStatusItem?
    var inputWindow: NSWindow?
    var wakeWordDetector: WakeWordDetector?
    var audioRecorder: AudioRecorder?
    var vadDetector: VADDetector?
    var grpcClient: GRPCClient?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        setupStatusBar()
        setupServices()
        setupGlobalShortcut()
        checkPermissions()
    }
    
    func setupStatusBar() {
        statusBarItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusBarItem?.button {
            button.image = NSImage(systemSymbolName: "mic.fill", accessibilityDescription: "WALL-E")
            button.action = #selector(toggleInputWindow)
            button.target = self
        }
        
        let menu = NSMenu()
        menu.addItem(NSMenuItem(title: "打开输入面板", action: #selector(showInputWindow), keyEquivalent: ""))
        menu.addItem(NSMenuItem(title: "设置", action: #selector(showSettings), keyEquivalent: ","))
        menu.addItem(NSMenuItem.separator())
        menu.addItem(NSMenuItem(title: "退出", action: #selector(quitApp), keyEquivalent: "q"))
        
        statusBarItem?.menu = menu
    }
    
    func setupServices() {
        wakeWordDetector = WakeWordDetector()
        audioRecorder = AudioRecorder()
        vadDetector = VADDetector()
        grpcClient = GRPCClient()
        
        wakeWordDetector?.onWakeWordDetected = { [weak self] in
            DispatchQueue.main.async {
                self?.handleWakeWord()
            }
        }
        
        audioRecorder?.onRecordingComplete = { [weak self] audioData in
            self?.handleRecordingComplete(audioData: audioData)
        }
        
        vadDetector?.onSpeechEnd = { [weak self] in
            self?.audioRecorder?.stopRecording()
        }
        
        wakeWordDetector?.startListening()
    }
    
    func setupGlobalShortcut() {
        NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { [weak self] event in
            if event.modifierFlags.contains(.command) && event.keyCode == kVK_Space {
                self?.showInputWindow()
            }
        }
        
        NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            if event.modifierFlags.contains(.command) && event.keyCode == kVK_Space {
                self?.showInputWindow()
                return nil
            }
            return event
        }
    }
    
    func checkPermissions() {
        checkMicrophonePermission()
        checkAccessibilityPermission()
    }
    
    func checkMicrophonePermission() {
        switch AVCaptureDevice.authorizationStatus(for: .audio) {
        case .authorized:
            break
        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .audio) { granted in
                if !granted {
                    DispatchQueue.main.async {
                        self.showPermissionAlert(type: "麦克风")
                    }
                }
            }
        case .denied, .restricted:
            showPermissionAlert(type: "麦克风")
        @unknown default:
            break
        }
    }
    
    func checkAccessibilityPermission() {
        let options: NSDictionary = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true]
        let accessEnabled = AXIsProcessTrustedWithOptions(options)
        
        if !accessEnabled {
            showPermissionAlert(type: "辅助功能")
        }
    }
    
    func showPermissionAlert(type: String) {
        let alert = NSAlert()
        alert.messageText = "需要\(type)权限"
        alert.informativeText = "WALL-E 需要\(type)权限才能正常工作。请在系统设置中授予权限。"
        alert.alertStyle = .warning
        alert.addButton(withTitle: "打开系统设置")
        alert.addButton(withTitle: "稍后")
        
        if alert.runModal() == .alertFirstButtonReturn {
            if type == "麦克风" {
                NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone")!)
            } else if type == "辅助功能" {
                NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility")!)
            }
        }
    }
    
    @objc func toggleInputWindow() {
        if inputWindow?.isVisible == true {
            inputWindow?.close()
        } else {
            showInputWindow()
        }
    }
    
    @objc func showInputWindow() {
        if inputWindow == nil {
            let contentView = InputWindowView(
                onVoiceStart: { [weak self] in
                    self?.startVoiceRecording()
                },
                onTextSubmit: { [weak self] text in
                    self?.handleTextInput(text: text)
                }
            )
            
            inputWindow = NSWindow(
                contentRect: NSRect(x: 0, y: 0, width: 400, height: 300),
                styleMask: [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView],
                backing: .buffered,
                defer: false
            )
            inputWindow?.contentView = NSHostingView(rootView: contentView)
            inputWindow?.title = "WALL-E 输入面板"
            inputWindow?.center()
            inputWindow?.level = .floating
            inputWindow?.isOpaque = false
            inputWindow?.backgroundColor = .clear
        }
        
        inputWindow?.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }
    
    @objc func showSettings() {
        NSApp.sendAction(Selector(("showPreferencesWindow:")), to: nil, from: nil)
        NSApp.activate(ignoringOtherApps: true)
    }
    
    @objc func quitApp() {
        wakeWordDetector?.stopListening()
        audioRecorder?.stopRecording()
        NSApplication.shared.terminate(nil)
    }
    
    func handleWakeWord() {
        showInputWindow()
        startVoiceRecording()
    }
    
    func startVoiceRecording() {
        audioRecorder?.startRecording()
        vadDetector?.startDetecting(audioStream: audioRecorder?.audioStream)
    }
    
    func handleRecordingComplete(audioData: Data) {
        grpcClient?.sendAudioForSTT(audioData: audioData) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let text):
                    self?.handleRecognizedText(text: text)
                case .failure(let error):
                    self?.showError(message: "语音识别失败: \(error.localizedDescription)")
                }
            }
        }
    }
    
    func handleTextInput(text: String) {
        grpcClient?.sendTextCommand(text: text) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let response):
                    self?.showResult(message: response)
                case .failure(let error):
                    self?.showError(message: "处理失败: \(error.localizedDescription)")
                }
            }
        }
    }
    
    func handleRecognizedText(text: String) {
        handleTextInput(text: text)
    }
    
    func showResult(message: String) {
        let alert = NSAlert()
        alert.messageText = "执行结果"
        alert.informativeText = message
        alert.alertStyle = .informational
        alert.runModal()
    }
    
    func showError(message: String) {
        let alert = NSAlert()
        alert.messageText = "错误"
        alert.informativeText = message
        alert.alertStyle = .warning
        alert.runModal()
    }
}
