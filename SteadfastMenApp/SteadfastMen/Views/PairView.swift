import SwiftUI

struct PairView: View {
    @EnvironmentObject var store: DevotionService
    @Environment(\.dismiss) private var dismiss
    @Environment(\.openURL) private var openURL
    @State private var name: String = ""

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    Text("THE PAIR · SIX LESSONS")
                        .font(.system(size: 11, weight: .medium))
                        .tracking(0.8)
                        .foregroundStyle(SM.accent)
                    Text("One brother. No board.")
                        .font(.system(size: 28, weight: .semibold))
                        .foregroundStyle(SM.text)
                    Text("Name one man for this mark. Midweek you ask: did you do the act? He asks you. The table only hears done. Shame stays off the stage.")
                        .font(.system(size: 16))
                        .foregroundStyle(SM.muted)
                    TextField("His first name", text: $name)
                        .textFieldStyle(.plain)
                        .padding(14)
                        .background(SM.surface)
                        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                        .foregroundStyle(SM.text)
                    Text("This lesson’s act")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(SM.accent)
                    Text("Phone down at the table.")
                        .font(.system(size: 17, weight: .semibold))
                    Button("Save the pair") {
                        store.pairName = name.trimmingCharacters(in: .whitespaces)
                    }
                    .buttonStyle(PairFill())
                    Button("Ask him: did you do the act?") {
                        store.pingPair()
                        let body = "Did you do the act from this lesson? Phone down at the table. — Steadfast"
                        let q = body.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? body
                        if let url = URL(string: "sms:&body=\(q)") {
                            openURL(url)
                        }
                    }
                    .buttonStyle(PairGhost())
                    .disabled(store.pairName.isEmpty && name.trimmingCharacters(in: .whitespaces).isEmpty)
                    if !store.pairPinged.isEmpty {
                        Text("Last ping \(store.pairPinged). Still just you two.")
                            .font(.system(size: 13))
                            .foregroundStyle(SM.muted)
                    }
                }
                .padding(24)
            }
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("Pair")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
            .onAppear { name = store.pairName }
        }
    }
}

private struct PairFill: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity)
            .padding(14)
            .background(SM.text)
            .foregroundStyle(SM.bg)
            .clipShape(RoundedRectangle(cornerRadius: 24, style: .continuous))
            .opacity(configuration.isPressed ? 0.85 : 1)
    }
}

private struct PairGhost: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity)
            .padding(14)
            .background(SM.surface)
            .foregroundStyle(SM.text)
            .clipShape(RoundedRectangle(cornerRadius: 24, style: .continuous))
            .opacity(configuration.isPressed ? 0.85 : 1)
    }
}
