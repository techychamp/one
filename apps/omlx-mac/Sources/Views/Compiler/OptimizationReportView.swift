import SwiftUI

struct OptimizationReportView: View {
    var body: some View {
        VStack(alignment: .leading) {
            Text("Optimization Reports")
                .font(.headline)

            Text("Limitation: Optimization reports are unavailable in the frozen v1 GUI-002 API.")
                .font(.caption)
                .foregroundColor(.secondary)

            List {
                Text("No reports available.")
                    .foregroundColor(.secondary)
            }
            .listStyle(.plain)
            .frame(height: 150)
            .background(Color.gray.opacity(0.1))
            .cornerRadius(8)
        }
    }
}
