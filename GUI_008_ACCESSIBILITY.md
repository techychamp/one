# GUI-008 Accessibility

## Accessibility Features Implemented
- **Navigation Shortcuts**: Full keyboard control for opening sidebar and navigation links.
- **VoiceOver**: Replaced basic `NavigationLink` structures with `.accessibilityLabel` and `.isButton` trait in `SidebarRow` to ensure proper screen reading.
- **Dynamic Type**: SwiftUI standard styling applied throughout the unified navigation pane, adapting font sizes properly.
- **Focus Management**: Proper input focus on the Global Search window immediately on launch.
