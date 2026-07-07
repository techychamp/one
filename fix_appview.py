import re

with open('apps/omlx-mac/Sources/AppView/AppView.swift', 'r') as f:
    content = f.read()

# Add new sections to SettingsSidebar
sidebar_repl = """            Section {
                SidebarRow(section: .chat)
                SidebarRow(section: .compiler)
                SidebarRow(section: .developer)
            } header: {
                Text(String(localized: "sidebar.group.workspace",
                            defaultValue: "Workspaces",
                            comment: "Sidebar group heading for workspaces"))
            }
            Section {"""

content = content.replace("            Section {", sidebar_repl, 1) # Only first occurrence

# Add screen stubs to screen(for:)
# Need to find the screen(for:) method, which might be in an extension
with open('apps/omlx-mac/Sources/AppView/AppView.swift', 'w') as f:
    f.write(content)
