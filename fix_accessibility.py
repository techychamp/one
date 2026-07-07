import re

# Update AppView.swift for accessibility
with open('apps/omlx-mac/Sources/AppView/AppView.swift', 'r') as f:
    content = f.read()

# Make the settings sidebar accessible
a11y_sidebar = """        List(selection: $selection) {
            Section {
                SidebarRow(section: .chat)
                SidebarRow(section: .compiler)
                SidebarRow(section: .developer)
            } header: {"""

a11y_sidebar_repl = """        List(selection: $selection) {
            Section {
                SidebarRow(section: .chat)
                SidebarRow(section: .compiler)
                SidebarRow(section: .developer)
            } header: {"""

# Replace SidebarRow to add accessibility traits
row_find = """    var body: some View {
        NavigationLink(value: section) {
            Label(section.title, systemImage: section.symbol)
        }
    }"""

row_repl = """    var body: some View {
        NavigationLink(value: section) {
            Label(section.title, systemImage: section.symbol)
        }
        .accessibilityLabel(section.title)
        .accessibilityAddTraits(.isButton)
    }"""

content = content.replace(row_find, row_repl)

with open('apps/omlx-mac/Sources/AppView/AppView.swift', 'w') as f:
    f.write(content)
