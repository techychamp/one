import re

with open('apps/omlx-mac/Sources/AppView/AppView.swift', 'r') as f:
    content = f.read()

# Add missing screen cases
screen_repl = """    private func screen(for section: AppSection) -> some View {
        switch section {
        case .chat:         Text("Chat Workspace Placeholder")
        case .compiler:     Text("Compiler Explorer Placeholder")
        case .developer:    Text("Developer Studio Placeholder")
        case .server:       ServerScreen()"""

content = content.replace('    private func screen(for section: AppSection) -> some View {\n        switch section {\n        case .server:       ServerScreen()', screen_repl)

# Add properties for state managers
manager_props = """struct AppView: View {
    @State private var selection: AppSection? = .status
    @State private var presentedUpdate: AvailableUpdate?
    @State private var isSearchPresented = false
    @State private var searchViewModel = GlobalSearchViewModel()
    @Environment(\.keyboardShortcutManager) private var shortcuts
    @State private var windowState = WindowStateManager()"""

content = content.replace('struct AppView: View {\n    @State private var selection: AppSection? = .status\n    @State private var presentedUpdate: AvailableUpdate?', manager_props)

modifier_repl = """        .onChange(of: services.requestedSection) { _, requested in
            // A screen asked us to navigate elsewhere (e.g. "Edit on
            // Server →" from the per-model Profiles tab). Clear the
            // request after applying so the same section can be requested
            // again later.
            guard let requested else { return }
            selection = requested
            services.requestedSection = nil
        }
        .onReceive(shortcuts.actionPublisher) { action in
            switch action {
            case .toggleSidebar:
                windowState.sidebarWidth = windowState.sidebarWidth == 0 ? 220 : 0
            case .openSearch:
                isSearchPresented = true
            case .navigateTo(let section):
                selection = section
            default: break
            }
        }
        .sheet(isPresented: $isSearchPresented) {
            SearchView(viewModel: searchViewModel, selection: $selection)
        }
        .task {
            searchViewModel.configure(modelService: services.modelManagement, sessionService: services.sessions)
        }"""

content = content.replace('        .onChange(of: services.requestedSection) { _, requested in\n            // A screen asked us to navigate elsewhere (e.g. "Edit on\n            // Server →" from the per-model Profiles tab). Clear the\n            // request after applying so the same section can be requested\n            // again later.\n            guard let requested else { return }\n            selection = requested\n            services.requestedSection = nil\n        }', modifier_repl)


with open('apps/omlx-mac/Sources/AppView/AppView.swift', 'w') as f:
    f.write(content)
