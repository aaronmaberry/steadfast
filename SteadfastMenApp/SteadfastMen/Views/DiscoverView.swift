import SwiftUI

struct DiscoverView: View {
    @Environment(\.openURL) private var openURL

    private let tiles: [(String, URL)] = [
        ("Training", Config.training),
        ("Book", Config.book),
        ("Groups", Config.groups),
        ("Merch", Config.merch),
        ("Daily", Config.dailyWeb),
        ("The table", Config.site)
    ]

    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 10) {
                    ForEach(tiles, id: \.0) { tile in
                        Button {
                            openURL(tile.1)
                        } label: {
                            Text(tile.0)
                                .font(.system(size: 17, weight: .semibold))
                                .foregroundStyle(SM.text)
                                .frame(maxWidth: .infinity, minHeight: 96, alignment: .bottomLeading)
                                .padding(14)
                                .background(SM.surface)
                                .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(18)
            }
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("Discover")
        }
    }
}
