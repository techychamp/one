import Foundation

public protocol CompilerServiceProtocol: Sendable {
    func getPlanningBundle() async throws -> PlanningBundleDTO
    func getExecutionGraph() async throws -> ExecutionGraphDTO
    func getOptimizationReports() async throws -> [OptimizationReportDTO]
    func getArtifact(id: String) async throws -> ArtifactInfoDTO
    func getTimeline() async throws -> ExecutionTimelineDTO
}

public actor CompilerService: CompilerServiceProtocol {
    private let client: OMLXClient

    public init(client: OMLXClient) {
        self.client = client
    }

    public func getPlanningBundle() async throws -> PlanningBundleDTO {
        try await client.get("\(RuntimeAPI.v1Compiler)/planning-bundle")
    }

    public func getExecutionGraph() async throws -> ExecutionGraphDTO {
        try await client.get("\(RuntimeAPI.v1Compiler)/execution-graph")
    }

    public func getOptimizationReports() async throws -> [OptimizationReportDTO] {
        struct ReportsResponse: Decodable {
            let reports: [OptimizationReportDTO]
        }
        let res: ReportsResponse = try await client.get("\(RuntimeAPI.v1Compiler)/optimization-reports")
        return res.reports
    }

    public func getArtifact(id: String) async throws -> ArtifactInfoDTO {
        try await client.get("\(RuntimeAPI.v1Compiler)/artifacts/\(id)")
    }

    public func getTimeline() async throws -> ExecutionTimelineDTO {
        try await client.get("\(RuntimeAPI.v1Compiler)/timeline")
    }
}
