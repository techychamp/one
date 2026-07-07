import SwiftUI

@MainActor
@Observable
final class WindowStateManager {
    var sidebarWidth: CGFloat {
        get { UserDefaults.standard.double(forKey: "WindowState.sidebarWidth") > 0 ? UserDefaults.standard.double(forKey: "WindowState.sidebarWidth") : 220 }
        set { UserDefaults.standard.set(newValue, forKey: "WindowState.sidebarWidth") }
    }

    var inspectorVisible: Bool {
        get { UserDefaults.standard.bool(forKey: "WindowState.inspectorVisible") }
        set { UserDefaults.standard.set(newValue, forKey: "WindowState.inspectorVisible") }
    }

    var lastSelectedSection: AppSection? {
        get {
            guard let rawValue = UserDefaults.standard.string(forKey: "WindowState.lastSection"),
                  let section = AppSection(rawValue: rawValue) else { return .chat }
            return section
        }
        set {
            UserDefaults.standard.set(newValue?.rawValue, forKey: "WindowState.lastSection")
        }
    }
}
