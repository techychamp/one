import Foundation

protocol DiagnosticsServiceProtocol: Sendable {
    func getCompilerInspection() async throws -> CompilerInspection
    func getExecutionMetrics() async throws -> ExecutionMetrics
    func getAppleMetrics() async throws -> AppleMetrics
    func getBenchmarkReport() async throws -> BenchmarkReport
}

actor DiagnosticsService: DiagnosticsServiceProtocol {
    private let client: OMLXClient
    
    init(client: OMLXClient) {
        self.client = client
    }
    
    func getCompilerInspection() async throws -> CompilerInspection {
        return try await client.get("\(RuntimeAPI.v1Diagnostics)/compiler")
    }
    
    func getExecutionMetrics() async throws -> ExecutionMetrics {
        return try await client.get("\(RuntimeAPI.v1Diagnostics)/execution")
    }
    
    func getAppleMetrics() async throws -> AppleMetrics {
        return try await client.get("\(RuntimeAPI.v1Diagnostics)/apple")
    }
    
    func getBenchmarkReport() async throws -> BenchmarkReport {
        return try await client.get(RuntimeAPI.v1Benchmarks)
    }
}
