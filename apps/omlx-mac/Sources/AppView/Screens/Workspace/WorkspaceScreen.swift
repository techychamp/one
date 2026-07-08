import SwiftUI

struct WorkspaceScreen: View {
    @Environment(AppServices.self) private var services
    @Environment(\.omlxTheme) private var theme

    @State private var generationVM: GenerationViewModel?
    @State private var sessionVM: SessionViewModel?

    var body: some View {
        Group {
            if let generationVM, let sessionVM {
                HStack(spacing: 0) {
                    SessionSidebar(vm: sessionVM)
                        .frame(width: 250)
                        .background(theme.windowBg.opacity(0.8))

                    Divider()
                        .background(theme.groupBorder)

                    VStack(spacing: 0) {
                        RuntimeStatusView()
                            .padding(.horizontal)
                            .padding(.vertical, 8)
                            .background(theme.groupBg)
                            .border(width: 1, edges: [.bottom], color: theme.groupBorder)

                        ConversationView(vm: generationVM)
                            .frame(maxWidth: .infinity, maxHeight: .infinity)

                        PromptComposer(vm: generationVM)
                            .padding()
                            .background(theme.groupBg)
                            .border(width: 1, edges: [.top], color: theme.groupBorder)
                    }
                    .frame(maxWidth: .infinity)
                }
                .background(theme.windowBg)
                .onChange(of: sessionVM.activeSessionId) { _, _ in
                    generationVM.clear()
                }
            } else {
                ProgressView()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .onAppear {
            self.generationVM = GenerationViewModel(service: services.generationService)
            self.sessionVM = SessionViewModel(service: services.sessionService)
            Task { await self.sessionVM?.fetchSessions() }
        }
    }
}

extension View {
    func border(width: CGFloat, edges: [Edge], color: Color) -> some View {
        overlay(EdgeBorder(width: width, edges: edges).foregroundColor(color))
    }
}

private struct EdgeBorder: Shape {
    var width: CGFloat
    var edges: [Edge]

    func path(in rect: CGRect) -> Path {
        var path = Path()
        for edge in edges {
            var x: CGFloat {
                switch edge {
                case .top, .bottom, .leading: return rect.minX
                case .trailing: return rect.maxX - width
                }
            }
            var y: CGFloat {
                switch edge {
                case .top, .leading, .trailing: return rect.minY
                case .bottom: return rect.maxY - width
                }
            }
            var w: CGFloat {
                switch edge {
                case .top, .bottom: return rect.width
                case .leading, .trailing: return width
                }
            }
            var h: CGFloat {
                switch edge {
                case .top, .bottom: return width
                case .leading, .trailing: return rect.height
                }
            }
            path.addRect(CGRect(x: x, y: y, width: w, height: h))
        }
        return path
    }
}
