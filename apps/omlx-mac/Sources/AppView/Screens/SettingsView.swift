import SwiftUI

struct SettingsView: View {
    @Environment(\.omlxTheme) private var theme
    @State private var appearanceManager = AppearanceManager()

    @AppStorage("Settings.developerMode") private var developerMode: Bool = false
    @AppStorage("Settings.experimentalUI") private var experimentalUI: Bool = false

    var body: some View {
        TabView {
            AppearanceSettingsView(appearanceManager: appearanceManager)
                .tabItem {
                    Label("Appearance", systemImage: "paintpalette")
                }

            DeveloperSettingsView(developerMode: $developerMode, experimentalUI: $experimentalUI)
                .tabItem {
                    Label("Developer", systemImage: "hammer")
                }
        }
        .frame(width: 450, height: 250)
        .padding()
        .background(theme.windowBg)
    }
}

struct AppearanceSettingsView: View {
    @Bindable var appearanceManager: AppearanceManager
    @Environment(\.omlxTheme) private var theme

    var body: some View {
        Form {
            Picker("Appearance:", selection: $appearanceManager.currentAppearance) {
                ForEach(AppAppearance.allCases) { appearance in
                    Text(appearance.rawValue).tag(appearance)
                }
            }
            .pickerStyle(.radioGroup)
            .padding()
        }
    }
}

struct DeveloperSettingsView: View {
    @Binding var developerMode: Bool
    @Binding var experimentalUI: Bool
    @Environment(\.omlxTheme) private var theme

    var body: some View {
        Form {
            Toggle("Enable Developer Mode", isOn: $developerMode)
            Toggle("Enable Experimental UI", isOn: $experimentalUI)
                .disabled(!developerMode)
        }
        .padding()
    }
}
