import SwiftUI

struct SearchView: View {
    @Bindable var viewModel: GlobalSearchViewModel
    @Binding var selection: AppSection?
    @Environment(\.dismiss) private var dismiss
    @Environment(\.omlxTheme) private var theme

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Image(systemName: "magnifyingglass")
                    .foregroundColor(theme.textTertiary)
                TextField("Search across oMLX...", text: $viewModel.query)
                    .textFieldStyle(.plain)
                    .font(.omlxText(16))
                    .onChange(of: viewModel.query) { _, _ in
                        viewModel.performSearch()
                    }

                if viewModel.isSearching {
                    ProgressView()
                        .controlSize(.small)
                } else if !viewModel.query.isEmpty {
                    Button(action: { viewModel.query = "" }) {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundColor(theme.textTertiary)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(16)
            .background(theme.windowBg)

            Divider()
                .background(theme.separator)

            if viewModel.results.isEmpty && !viewModel.query.isEmpty && !viewModel.isSearching {
                VStack(spacing: 12) {
                    Image(systemName: "magnifyingglass")
                        .font(.system(size: 32))
                        .foregroundColor(theme.textTertiary)
                    Text("No results for \"\(viewModel.query)\"")
                        .font(.omlxText(14))
                        .foregroundColor(theme.textSecondary)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .padding(.top, 40)
            } else {
                List(viewModel.results) { result in
                    Button(action: {
                        selection = result.section
                        dismiss()
                    }) {
                        HStack(spacing: 12) {
                            Image(systemName: result.systemImage)
                                .foregroundColor(theme.accent)
                                .frame(width: 24, height: 24)

                            VStack(alignment: .leading, spacing: 2) {
                                Text(result.title)
                                    .font(.omlxText(14, weight: .medium))
                                    .foregroundColor(theme.text)
                                Text(result.subtitle)
                                    .font(.omlxText(12))
                                    .foregroundColor(theme.textSecondary)
                            }
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundColor(theme.textTertiary)
                                .font(.system(size: 10, weight: .bold))
                        }
                        .padding(.vertical, 8)
                        .padding(.horizontal, 12)
                        .background(Color.clear)
                        .contentShape(Rectangle())
                    }
                    .buttonStyle(.plain)
                    .listRowInsets(EdgeInsets())
                    .listRowSeparator(.hidden)
                    .listRowBackground(Color.clear)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
                .background(theme.contentBg)
            }
        }
        .frame(width: 500, height: 400)
        .background(theme.windowBg)
        // Accessibility
        .accessibilityElement(children: .contain)
        .accessibilityLabel("Global Search")
    }
}
