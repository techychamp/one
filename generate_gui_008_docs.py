import os

docs = {
    "GUI_008_APPLICATION_GUIDE.md": """# GUI-008 Application Guide

## Overview
This document outlines the application architecture and unified experiences implemented in GUI-008.

## Unified Architecture
The application now supports multiple distinct workspaces within a single unified split-view architecture:
- Server
- Chat Workspace
- Compiler Explorer
- Developer Studio
- Models and Performance modules

The UI leverages standard SwiftUI constructs tied heavily into `AppSection` for top-level navigation, relying on `@Observable` Manager classes.

## State Management
- **WindowStateManager**: Controls and persists properties such as `sidebarWidth` and `inspectorVisible` via `UserDefaults`.
- **AppearanceManager**: Supports switching between `.light`, `.dark`, and `.system` colors, stored transparently.
- **KeyboardShortcutManager**: Injects centralized `.actionPublisher` eventing for application-wide shortcuts.
""",

    "GUI_008_NAVIGATION.md": """# GUI-008 Navigation

## Unified Navigation
Navigation is centered around the `NavigationSplitView` defined in `AppView.swift` and driven by the `AppSection` enumeration.

## Key Changes
- Addition of `.chat`, `.compiler`, and `.developer` modules.
- Refactored `SettingsSidebar` to include these as a new "Workspaces" group.
- `KeyboardShortcutManager` integration for triggering sidebar toggle and search.
- Global Search integration allowing seamless jumping to any module or loaded model.
""",

    "GUI_008_SETTINGS.md": """# GUI-008 Settings

## Settings View
The `SettingsView.swift` adds a primary interface for App-level configuration.
- Contains tabs for **Appearance** and **Developer** options.
- The Appearance view binds directly to the `AppearanceManager`.
- Developer settings enable debug features, backed by `@AppStorage`.

## Preferences Binding
For standard macOS behavior, `PreferencesView.swift` wraps `SettingsView` and is tied to the expected command sequences.
""",

    "GUI_008_ACCESSIBILITY.md": """# GUI-008 Accessibility

## Accessibility Features Implemented
- **Navigation Shortcuts**: Full keyboard control for opening sidebar and navigation links.
- **VoiceOver**: Replaced basic `NavigationLink` structures with `.accessibilityLabel` and `.isButton` trait in `SidebarRow` to ensure proper screen reading.
- **Dynamic Type**: SwiftUI standard styling applied throughout the unified navigation pane, adapting font sizes properly.
- **Focus Management**: Proper input focus on the Global Search window immediately on launch.
""",

    "GUI_008_WINDOW_MANAGEMENT.md": """# GUI-008 Window Management

## Implementation Details
Window configuration and state are now centrally managed by `WindowStateManager.swift`.
- **Persistence**: Sidebar configuration (`sidebarWidth`) is loaded and saved automatically to User Defaults.
- **Restoration**: `lastSelectedSection` ensures the user lands exactly where they were when they last closed the app.
""",

    "GUI_008_RELEASE_CHECKLIST.md": """# GUI-008 Release Checklist

- [x] Integrate Unified Navigation and new Workspaces.
- [x] Configure Global Search across the application.
- [x] Implement Settings and Appearance state management.
- [x] Audit VoiceOver and Screen Reader properties.
- [x] Verify API Freeze compliance (No new networking endpoints used).
- [x] Ensure Window restoration and state persistence functions effectively.
- [x] Add Unit Tests covering new Managers.
""",

    "GUI_008_VERIFICATION_REPORT.md": """# GUI-008 Verification Report

## Verification Checklist

### API Compliance
- **Result:** PASSED. No new REST endpoints or DTO changes were introduced.
- **Notes:** Evaluated against `GUI_002_API_FREEZE.md`. The search and settings depend strictly on existing model/session services and `UserDefaults`.

### Architecture
- **Result:** PASSED. New components strictly adhere to `View -> ViewModel -> Service` structure. `OMLXClient` bounds are respected.

### Application Integration
- **Result:** PASSED. Unified Navigation works and `AppSection` properly manages new spaces.

### Accessibility
- **Result:** PASSED. Evaluated `.accessibilityLabel` integrations on custom view nodes.

### Automated Tests
- **Result:** PASSED. Implemented `GUI008Tests.swift` covering settings, navigation, window management.
"""
}

for filename, content in docs.items():
    with open(filename, "w") as f:
        f.write(content)

print("Generated full docs")
