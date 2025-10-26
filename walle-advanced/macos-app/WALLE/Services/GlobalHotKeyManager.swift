import Foundation
import Carbon
import AppKit

class GlobalHotKeyManager {
    private var hotKeyRef: EventHotKeyRef?
    private var eventHandler: EventHandlerRef?
    private var callback: (() -> Void)?
    
    func registerHotKey(keyCode: UInt32, modifiers: NSEvent.ModifierFlags, handler: @escaping () -> Void) {
        self.callback = handler
        
        var eventType = EventTypeSpec()
        eventType.eventClass = OSType(kEventClassKeyboard)
        eventType.eventKind = OSType(kEventHotKeyPressed)
        
        InstallEventHandler(
            GetApplicationEventTarget(),
            { (_, inEvent, _) -> OSStatus in
                GlobalHotKeyManager.handleHotKeyEvent(inEvent)
                return noErr
            },
            1,
            &eventType,
            UnsafeMutableRawPointer(Unmanaged.passUnretained(self).toOpaque()),
            &eventHandler
        )
        
        var hotKeyID = EventHotKeyID()
        hotKeyID.signature = OSType(0x4B455921)
        hotKeyID.id = 1
        
        let carbonModifiers = modifiers.carbonFlags
        
        RegisterEventHotKey(
            keyCode,
            carbonModifiers,
            hotKeyID,
            GetApplicationEventTarget(),
            0,
            &hotKeyRef
        )
    }
    
    func unregisterHotKey() {
        if let ref = hotKeyRef {
            UnregisterEventHotKey(ref)
            hotKeyRef = nil
        }
        
        if let handler = eventHandler {
            RemoveEventHandler(handler)
            eventHandler = nil
        }
    }
    
    private static func handleHotKeyEvent(_ event: EventRef?) -> OSStatus {
        return noErr
    }
    
    deinit {
        unregisterHotKey()
    }
}

extension NSEvent.ModifierFlags {
    var carbonFlags: UInt32 {
        var carbon: UInt32 = 0
        
        if contains(.command) {
            carbon |= UInt32(cmdKey)
        }
        if contains(.option) {
            carbon |= UInt32(optionKey)
        }
        if contains(.control) {
            carbon |= UInt32(controlKey)
        }
        if contains(.shift) {
            carbon |= UInt32(shiftKey)
        }
        
        return carbon
    }
}
