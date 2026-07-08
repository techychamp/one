import SwiftUI
import MarkdownUI

struct ConversationView: View {
    @Bindable var vm: GenerationViewModel
    @Environment(\.omlxTheme) private var theme

    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(spacing: 16) {
                    if vm.messages.isEmpty && vm.streamingDelta.isEmpty {
                        emptyState
                    } else {
                        ForEach(Array(vm.messages.enumerated()), id: \.offset) { index, msg in
                            MessageRow(message: msg)
                                .id(index)
                                .accessibilityElement(children: .contain)
                                .accessibilityLabel("\(msg.role == "user" ? "Your message" : "Assistant response"): \(msg.content)")
                        }

                        if !vm.streamingDelta.isEmpty {
                            MessageRow(message: ChatMessage(role: "assistant", content: vm.streamingDelta), isStreaming: true)
                                .id("streaming")
                                .accessibilityElement(children: .contain)
                                .accessibilityLabel("Assistant is generating response...")
                        }

                        if let error = vm.error {
                            ErrorRow(error: error)
                                .accessibilityElement(children: .combine)
                                .accessibilityLabel("Error: \(error.localizedDescription)")
                        }
                    }
                }
                .padding()
            }
            .accessibilityIdentifier("ConversationScrollView")
            .onChange(of: vm.messages.count) { _, _ in
                if let last = vm.messages.indices.last {
                    withAnimation { proxy.scrollTo(last, anchor: .bottom) }
                }
            }
            .onChange(of: vm.streamingDelta) { _, _ in
                withAnimation { proxy.scrollTo("streaming", anchor: .bottom) }
            }
        }
    }

    private var emptyState: some View {
        VStack(spacing: 12) {
            Spacer().frame(height: 100)
            Image(systemName: "bubble.left.and.bubble.right")
                .font(.system(size: 48, weight: .light))
                .foregroundColor(theme.textTertiary)
                .accessibilityHidden(true)
            Text("No messages yet")
                .font(.omlxText(16, weight: .medium))
                .foregroundColor(theme.text)
            Text("Start a conversation by typing a message below.")
                .font(.omlxText(13))
                .foregroundColor(theme.textSecondary)
        }
        .frame(maxWidth: .infinity, alignment: .center)
        .accessibilityElement(children: .combine)
        .accessibilityLabel("Empty conversation. Start a conversation by typing a message below.")
    }
}

private struct MessageRow: View {
    let message: ChatMessage
    var isStreaming: Bool = false
    @Environment(\.omlxTheme) private var theme

    var isUser: Bool {
        message.role == "user"
    }

    var body: some View {
        HStack {
            if isUser { Spacer(minLength: 40) }

            VStack(alignment: isUser ? .trailing : .leading, spacing: 4) {
                Text(isUser ? "You" : "Assistant")
                    .font(.omlxText(11, weight: .semibold))
                    .foregroundColor(theme.textSecondary)
                    .accessibilityHidden(true)

                Markdown(message.content)
                    .markdownTheme(.omlx)
                    .padding(12)
                    .background(isUser ? theme.accent.opacity(0.1) : theme.groupBg)
                    .cornerRadius(8)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(isUser ? theme.accent.opacity(0.3) : theme.groupBorder, lineWidth: 1)
                    )
            }

            if !isUser {
                if isStreaming {
                    ProgressView()
                        .controlSize(.small)
                        .padding(.leading, 8)
                        .accessibilityLabel("Loading indicator")
                }
                Spacer(minLength: 40)
            }
        }
    }
}

private struct ErrorRow: View {
    let error: Error
    @Environment(\.omlxTheme) private var theme

    var body: some View {
        HStack {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundColor(.red)
                .accessibilityHidden(true)
            Text(error.localizedDescription)
                .font(.omlxText(13))
                .foregroundColor(theme.text)
            Spacer()
        }
        .padding()
        .background(Color.red.opacity(0.1))
        .cornerRadius(8)
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(Color.red.opacity(0.3), lineWidth: 1)
        )
    }
}
