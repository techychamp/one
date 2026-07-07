# GUI-008 Window Management

## Implementation Details
Window configuration and state are now centrally managed by `WindowStateManager.swift`.
- **Persistence**: Sidebar configuration (`sidebarWidth`) is loaded and saved automatically to User Defaults.
- **Restoration**: `lastSelectedSection` ensures the user lands exactly where they were when they last closed the app.
