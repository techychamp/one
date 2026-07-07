import SwiftUI
import Combine

@MainActor
@Observable
final class KeyboardShortcutManager {
    enum Action {
        case toggleSidebar
        case openSearch
        case newChat
        case cancelGeneration
        case navigateTo(AppSection)
    }

    var lastAction: Action?
    private let actionSubject = PassthroughSubject<Action, Never>()

    var actionPublisher: AnyPublisher<Action, Never> {
        actionSubject.eraseToAnyPublisher()
    }

    func perform(_ action: Action) {
        lastAction = action
        actionSubject.send(action)
    }
}

// SwiftUI Environment Key
struct KeyboardShortcutManagerKey: EnvironmentKey {
    static let defaultValue: KeyboardShortcutManager = KeyboardShortcutManager()
}

extension EnvironmentValues {
    var keyboardShortcutManager: KeyboardShortcutManager {
        get { self[KeyboardShortcutManagerKey.self] }
        set { self[KeyboardShortcutManagerKey.self] = newValue }
    }
}
