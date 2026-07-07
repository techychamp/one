# GUI-008 Settings

## Settings View
The `SettingsView.swift` adds a primary interface for App-level configuration.
- Contains tabs for **Appearance** and **Developer** options.
- The Appearance view binds directly to the `AppearanceManager`.
- Developer settings enable debug features, backed by `@AppStorage`.

## Preferences Binding
For standard macOS behavior, `PreferencesView.swift` wraps `SettingsView` and is tied to the expected command sequences.
