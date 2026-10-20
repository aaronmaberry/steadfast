import SwiftUI

struct MoreView: View {
    @Environment(\.openURL) private var openURL

    private var socials: [Social] {
        [
            Social(id: "yt", name: "YouTube", urlString: Config.youtube),
            Social(id: "ig", name: "Instagram", urlString: Config.instagram),
            Social(id: "x", name: "X", urlString: Config.x),
            Social(id: "fb", name: "Facebook", urlString: Config.facebook),
            Social(id: "tt", name: "TikTok", urlString: Config.tiktok),
            Social(id: "pod", name: "Podcast", urlString: Config.podcast)
        ]
    }

    var body: some View {
        NavigationStack {
            List {
                Section("The house") {
                    linkRow("Website", url: Config.site)
                    linkRow("Daily on the web", url: Config.dailyWeb)
                    linkRow("Training", url: Config.training)
                    linkRow("The book", url: Config.book)
                }

                Section("Social") {
                    ForEach(socials) { item in
                        Button {
                            openSocial(item)
                        } label: {
                            HStack {
                                Text(item.name)
                                Spacer()
                                Text(item.urlString.isEmpty ? "Add URL" : "Open")
                                    .font(.system(size: 13))
                                    .foregroundStyle(SM.brass)
                            }
                        }
                    }
                }

                Section("About") {
                    Text("Steadfast Men is a 24-lesson path for Christian husbands and fathers. The app is the daily walk. The site is the shop and the training.")
                        .font(.system(size: 15))
                        .foregroundStyle(.secondary)
                        .listRowBackground(SM.navy2)
                }
            }
            .scrollContentBackground(.hidden)
            .background(SM.navy.ignoresSafeArea())
            .navigationTitle("More")
        }
    }

    private func linkRow(_ title: String, url: URL) -> some View {
        Button(title) { openURL(url) }
    }

    private func openSocial(_ item: Social) {
        if let url = URL(string: item.urlString), !item.urlString.isEmpty {
            openURL(url)
        } else {
            openURL(Config.site)
        }
    }
}
