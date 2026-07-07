import Foundation

protocol PlatformServiceProtocol: Sendable {
    func getStatus() async throws -> RuntimeStatus
    func getCapabilities() async throws -> CapabilityReport
    func getServerInfo() async throws -> ServerInfo
}

actor PlatformService: PlatformServiceProtocol {
    private let client: OMLXClient
    
    init(client: OMLXClient) {
        self.client = client
    }
    
    func getStatus() async throws -> RuntimeStatus {
        return try await client.get(RuntimeAPI.v1Runtime)
    }
    
    func getCapabilities() async throws -> CapabilityReport {
        return try await client.get("\(RuntimeAPI.v1Runtime)/capabilities")
    }
    
    func getServerInfo() async throws -> ServerInfo {
        return try await client.get("\(RuntimeAPI.v1Runtime)/info")
    }
}
