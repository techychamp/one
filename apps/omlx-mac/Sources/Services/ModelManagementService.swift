import Foundation

protocol ModelManagementServiceProtocol: Sendable {
    func getModels() async throws -> [ModelInfo]
}

actor ModelManagementService: ModelManagementServiceProtocol {
    private let client: OMLXClient
    
    init(client: OMLXClient) {
        self.client = client
    }
    
    func getModels() async throws -> [ModelInfo] {
        return try await client.get(RuntimeAPI.v1Models)
    }
}

struct ModelInfo: Decodable, Sendable {
    let apiVersion: String?
    let id: String
    let ready: Bool
}
