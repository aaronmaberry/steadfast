import SwiftUI

struct RoomsView: View {
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
                Section {
                    Text("Every channel in one room. Paste live URLs in Config.swift — empty cards open the website.")
                        .font(.system(size: 15))
                        .foregroundStyle(SM.muted)
                        .listRowBackground(SM.bg)
                }
                Section("Channels") {
                    ForEach(socials) { item in
                        Button {
                            if let url = URL(string: item.urlString), !item.urlString.isEmpty {
                                openURL(url)
                            } else {
                                openURL(Config.site)
                            }
                        } label: {
                            HStack {
                                Text(item.name)
                                Spacer()
                                Text(item.urlString.isEmpty ? "Add URL" : "Open")
                                    .font(.system(size: 13))
                                    .foregroundStyle(SM.accent)
                            }
                        }
                    }
                }
                Section("The house") {
                    Button("Churches & crews") { openURL(Config.groups) }
                    Button("Website") { openURL(Config.site) }
                }
            }
            .scrollContentBackground(.hidden)
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("Rooms")
        }
    }
}
