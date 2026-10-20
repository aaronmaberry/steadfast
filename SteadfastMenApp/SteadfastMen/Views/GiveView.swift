import SwiftUI

struct GiveView: View {
    @Environment(\.openURL) private var openURL

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    Text("Support")
                        .font(.system(size: 34, weight: .semibold))
                        .foregroundStyle(SM.text)
                    Text("Help us expand the mission and make steadfast men.")
                        .font(.system(size: 22, weight: .regular))
                        .foregroundStyle(SM.text)
                    Text("Visit the website to see ways to help contribute. Your support helps us reach more men who need this content.")
                        .font(.system(size: 16))
                        .foregroundStyle(SM.muted)
                    Button("See ways to contribute") { openURL(Config.giveURL) }
                        .buttonStyle(.borderedProminent)
                    Text("Opens walksteadfast.com/give in Safari.")
                        .font(.system(size: 13))
                        .foregroundStyle(SM.muted)
                }
                .padding(24)
                .frame(maxWidth: 640, alignment: .leading)
                .frame(maxWidth: .infinity)
            }
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("Support")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}
