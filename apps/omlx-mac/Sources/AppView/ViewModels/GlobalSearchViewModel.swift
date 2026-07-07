import SwiftUI

struct SearchResult: Identifiable, Hashable {
    let id = UUID()
    let title: String
    let subtitle: String
    let section: AppSection
    let systemImage: String
}

@MainActor
@Observable
final class GlobalSearchViewModel {
    var query: String = ""
    var results: [SearchResult] = []
    var isSearching: Bool = false

    @ObservationIgnored
    private var modelService: ModelManagementServiceProtocol?
    @ObservationIgnored
    private var sessionService: SessionServiceProtocol?
    @ObservationIgnored
    private var searchTask: Task<Void, Never>?

    func configure(modelService: ModelManagementServiceProtocol, sessionService: SessionServiceProtocol) {
        self.modelService = modelService
        self.sessionService = sessionService
    }

    func performSearch() {
        searchTask?.cancel()
        guard !query.isEmpty else {
            results = []
            isSearching = false
            return
        }

        isSearching = true
        searchTask = Task { [weak self] in
            guard let self else { return }
            do {
                try await Task.sleep(nanoseconds: 300_000_000) // Debounce
                if Task.isCancelled { return }

                var newResults: [SearchResult] = []
                let lowerQuery = self.query.lowercased()

                // Static section searches
                for section in AppSection.allCases {
                    if section.title.lowercased().contains(lowerQuery) {
                        newResults.append(SearchResult(title: section.title, subtitle: "Navigation", section: section, systemImage: section.symbol))
                    }
                }

                // Real service-backed searches (mocked if service missing/failed)
                if let modelService = self.modelService {
                    let models = (try? await modelService.getModels()) ?? []
                    for model in models {
                        if model.id.lowercased().contains(lowerQuery) {
                            newResults.append(SearchResult(title: model.id, subtitle: "Model", section: .models, systemImage: "cube.transparent"))
                        }
                    }
                }

                if let sessionService = self.sessionService {
                    let sessions = (try? await sessionService.listSessions()) ?? []
                    for session in sessions {
                        if session.title.lowercased().contains(lowerQuery) {
                            newResults.append(SearchResult(title: session.title, subtitle: "Chat Session", section: .chat, systemImage: "bubble.left.and.bubble.right"))
                        }
                    }
                }

                if !Task.isCancelled {
                    self.results = newResults
                    self.isSearching = false
                }

            } catch {
                if !Task.isCancelled {
                    self.isSearching = false
                }
            }
        }
    }
}
