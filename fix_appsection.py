import re

with open('apps/omlx-mac/Sources/AppView/AppSection.swift', 'r') as f:
    content = f.read()

# Add titles
title_repl = """        case .server:
            return String(localized: "sidebar.server",
                          defaultValue: "Server",
                          comment: "Sidebar row label / navigation title for the Server section")
        case .chat:
            return String(localized: "sidebar.chat",
                          defaultValue: "Chat Workspace",
                          comment: "Sidebar row label / navigation title for the Chat section")
        case .compiler:
            return String(localized: "sidebar.compiler",
                          defaultValue: "Compiler Explorer",
                          comment: "Sidebar row label / navigation title for the Compiler section")
        case .developer:
            return String(localized: "sidebar.developer",
                          defaultValue: "Developer Studio",
                          comment: "Sidebar row label / navigation title for the Developer section")"""

content = content.replace('        case .server:\n            return String(localized: "sidebar.server",\n                          defaultValue: "Server",\n                          comment: "Sidebar row label / navigation title for the Server section")', title_repl)

# Add symbols
symbol_repl = """        case .server:          return "server.rack"
        case .chat:            return "bubble.left.and.bubble.right"
        case .compiler:        return "cpu"
        case .developer:       return "hammer" """

content = content.replace('        case .server:          return "server.rack"', symbol_repl)

with open('apps/omlx-mac/Sources/AppView/AppSection.swift', 'w') as f:
    f.write(content)
