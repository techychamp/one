# GUI-008 Navigation

## Unified Navigation
Navigation is centered around the `NavigationSplitView` defined in `AppView.swift` and driven by the `AppSection` enumeration.

## Key Changes
- Addition of `.chat`, `.compiler`, and `.developer` modules.
- Refactored `SettingsSidebar` to include these as a new "Workspaces" group.
- `KeyboardShortcutManager` integration for triggering sidebar toggle and search.
- Global Search integration allowing seamless jumping to any module or loaded model.
