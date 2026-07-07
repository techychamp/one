import Foundation

actor PreviewGenerationService: GenerationServiceProtocol {
    init() {}
    
    func generate(request: GenerateRequest) async throws -> GenerateResponse {
        return GenerateResponse(
            apiVersion: "v1",
            id: "chatcmpl-preview",
            choices: [Choice(message: ChatMessage(role: "assistant", content: "This is a preview response."), finishReason: "stop")]
        )
    }
    
    nonisolated func stream(request: GenerateRequest) async throws -> AsyncThrowingStream<GenerationChunk, Error> {
        return AsyncThrowingStream { continuation in
            continuation.yield(GenerationChunk(
                apiVersion: "v1",
                id: "chatcmpl-preview",
                choices: [ChunkChoice(delta: MessageDelta(role: "assistant", content: "This "), finishReason: nil)]
            ))
            continuation.yield(GenerationChunk(
                apiVersion: "v1",
                id: "chatcmpl-preview",
                choices: [ChunkChoice(delta: MessageDelta(role: nil, content: "is a "), finishReason: nil)]
            ))
            continuation.yield(GenerationChunk(
                apiVersion: "v1",
                id: "chatcmpl-preview",
                choices: [ChunkChoice(delta: MessageDelta(role: nil, content: "preview."), finishReason: "stop")]
            ))
            continuation.finish()
        }
    }
}

actor PreviewPlatformService: PlatformServiceProtocol {
    init() {}
    
    func getStatus() async throws -> RuntimeStatus {
        return RuntimeStatus(apiVersion: "v1", status: "ok", uptime: 3600, version: "0.1.0-preview")
    }
    
    func getCapabilities() async throws -> CapabilityReport {
        return CapabilityReport(apiVersion: "v1", supportsMoe: true, supportsSpeculation: true, supportsDiffusion: false)
    }
    
    func getServerInfo() async throws -> ServerInfo {
        return ServerInfo(apiVersion: "v1", host: "127.0.0.1", port: 8000, backend: "mlx")
    }
}
