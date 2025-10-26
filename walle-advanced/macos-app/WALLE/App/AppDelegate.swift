import Cocoa
import SwiftUI
import Carbon

class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem?
    private var inputWindowController: NSWindowController?
    private var globalHotKeyManager: GlobalHotKeyManager?
    private var voiceInputCoordinator: VoiceInputCoordinator?
    private var grpcClient: GRPCClient?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        setupStatusBar()
        setupGlobalHotKey()
        setupServices()
        requestPermissions()
    }
    
    private func setupStatusBar() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        
        if let button = statusItem?.button {
            button.image = NSImage(systemSymbolName: "mic.circle.fill", accessibilityDescription: "WALL-E")
            button.action = #selector(toggleInputWindow)
            button.target = self
        }
        
        let menu = NSMenu()
        menu.addItem(NSMenuItem(title: "打开输入面板", action: #selector(showInputWindow), keyEquivalent: "o"))
        menu.addItem(NSMenuItem(title: "设置", action: #selector(openSettings), keyEquivalent: ","))
        menu.addItem(NSMenuItem.separator())
        menu.addItem(NSMenuItem(title: "退出", action: #selector(quitApp), keyEquivalent: "q"))
        
        statusItem?.menu = menu
    }
    
    private func setupGlobalHotKey() {
        globalHotKeyManager = GlobalHotKeyManager()
        globalHotKeyManager?.registerHotKey(keyCode: kVK_Space, modifiers: .command) { [weak self] in
            self?.showInputWindow()
        }
    }
    
    private func setupServices() {
        grpcClient = GRPCClient(host: "localhost", port: 50051)
        voiceInputCoordinator = VoiceInputCoordinator(grpcClient: grpcClient)
        
        voiceInputCoordinator?.onVoiceInput = { [weak self] audioData in
            self?.handleVoiceInput(audioData)
        }
    }
    
    private func requestPermissions() {
        PermissionManager.shared.requestMicrophoneAccess()
        PermissionManager.shared.requestAccessibilityAccess()
    }
    
    @objc private func toggleInputWindow() {
        if inputWindowController?.window?.isVisible == true {
            inputWindowController?.close()
        } else {
            showInputWindow()
        }
    }
    
    @objc private func showInputWindow() {
        if inputWindowController == nil {
            let window = NSWindow(
                contentRect: NSRect(x: 0, y: 0, width: 500, height: 400),
                styleMask: [.titled, .closable, .miniaturizable, .resizable],
                backing: .buffered,
                defer: false
            )
            window.title = "WALL-E 助手"
            window.contentView = NSHostingView(rootView: InputWindow(
                voiceCoordinator: voiceInputCoordinator,
                grpcClient: grpcClient
            ))
            window.center()
            window.isMovableByWindowBackground = true
            window.level = .floating
            
            inputWindowController = NSWindowController(window: window)
        }
        
        inputWindowController?.showWindow(nil)
        NSApp.activate(ignoringOtherApps: true)
    }
    
    @objc private func openSettings() {
        NSApp.sendAction(Selector(("showSettingsWindow:")), to: nil, from: nil)
    }
    
    @objc private func quitApp() {
        voiceInputCoordinator?.stopListening()
        grpcClient?.disconnect()
        NSApplication.shared.terminate(self)
    }
    
    private func handleVoiceInput(_ audioData: Data) {
        grpcClient?.processVoiceInput(audioData: audioData) { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let response):
                    self.showFeedback(response.feedbackText)
                case .failure(let error):
                    self.showError(error.localizedDescription)
                }
            }
        }
    }
    
    private func showFeedback(_ text: String) {
        let notification = NSUserNotification()
        notification.title = "WALL-E"
        notification.informativeText = text
        notification.soundName = NSUserNotificationDefaultSoundName
        NSUserNotificationCenter.default.deliver(notification)
    }
    
    private func showError(_ text: String) {
        let alert = NSAlert()
        alert.messageText = "错误"
        alert.informativeText = text
        alert.alertStyle = .warning
        alert.addButton(withTitle: "确定")
        alert.runModal()
    }
}
