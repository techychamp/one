import SwiftUI

enum AppAppearance: String, CaseIterable, Identifiable {
    case system = "System"
    case light = "Light"
    case dark = "Dark"

    var id: String { rawValue }

    var colorScheme: ColorScheme? {
        switch self {
        case .system: return nil
        case .light: return .light
        case .dark: return .dark
        }
    }
}

@MainActor
@Observable
final class AppearanceManager {
    var currentAppearance: AppAppearance {
        get {
            guard let rawValue = UserDefaults.standard.string(forKey: "Appearance.current"),
                  let appearance = AppAppearance(rawValue: rawValue) else { return .system }
            return appearance
        }
        set {
            UserDefaults.standard.set(newValue.rawValue, forKey: "Appearance.current")
        }
    }
}
