import Foundation

// MARK: - Compiler DTOs for GUI-004

public struct PlanningBundleDTO: Decodable, Sendable, Identifiable {
    public var id: String {
        return UUID().uuidString
    }
    public let activeFamily: String
    public let domains: [String]
    public let status: String
}

public struct GraphNodeDTO: Decodable, Sendable, Identifiable {
    public let id: String
    public let name: String
    public let type: String
    public let dependencies: [String]
    public let metadata: [String: String]?
}

public struct ExecutionGraphDTO: Decodable, Sendable, Identifiable {
    public var id: String {
        return UUID().uuidString
    }
    public let nodes: [GraphNodeDTO]
    public let executionOrder: [String]
    public let phases: [String]
    public let barriers: [String]
}

public struct OptimizationReportDTO: Decodable, Sendable, Identifiable {
    public let id: String
    public let domain: String
    public let details: [String: String]
    public let status: String
}

public struct ArtifactInfoDTO: Decodable, Sendable, Identifiable {
    public let id: String
    public let type: String
    public let metadata: [String: String]
    public let dependencies: [String]
}

public struct TimelinePhaseDTO: Decodable, Sendable, Identifiable {
    public let id: String
    public let name: String
    public let status: String
    public let durationMs: Double?
}

public struct ExecutionTimelineDTO: Decodable, Sendable {
    public let phases: [TimelinePhaseDTO]
}
