import SwiftUI

@main
struct SteadfastMenApp: App {
    @StateObject private var store = DevotionService()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(store)
                .preferredColorScheme(.dark)
                .task { await store.load() }
        }
    }
}

struct RootView: View {
    var body: some View {
        TabView {
            TodayView()
                .tabItem { Label("Daily", systemImage: "sparkle") }
            PathView()
                .tabItem { Label("Library", systemImage: "square.stack") }
            RoomsView()
                .tabItem { Label("Socials", systemImage: "circle.grid.2x2") }
            YouView()
                .tabItem { Label("Profile", systemImage: "person.crop.circle") }
        }
        .tint(SM.text)
        .toolbarBackground(SM.surface, for: .tabBar)
    }
}
