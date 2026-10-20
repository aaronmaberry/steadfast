import SwiftUI

struct WordView: View {
    @EnvironmentObject var store: DevotionService
    @Environment(\.openURL) private var openURL
    @State private var showArticle = false
    @State private var showPray = false

    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("TODAY’S TEXT")
                            .font(.system(size: 11, weight: .medium))
                            .foregroundStyle(SM.accent)
                        Text(store.today.verse)
                            .font(.system(size: 18))
                    }
                    .padding(.vertical, 8)
                    .listRowBackground(SM.indigoCard)
                }
                Section("Walk") {
                    Button("Today’s devotion") { showArticle = true }
                    Button("Prayer") { showPray = true }
                    Button("Open daily on the site") { openURL(Config.dailyWeb) }
                }
            }
            .scrollContentBackground(.hidden)
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("Word")
            .sheet(isPresented: $showArticle) { DevotionArticleView() }
            .sheet(isPresented: $showPray) { PrayerView() }
        }
    }
}

struct DevotionArticleView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var store: DevotionService
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Button("Close") { dismiss() }
                Text("DEVOTION").font(.system(size: 11, weight: .medium)).foregroundStyle(SM.accent)
                Text(store.today.title).font(.system(size: 28, weight: .medium))
                Text(store.today.body).foregroundStyle(SM.text.opacity(0.86)).lineSpacing(4)
            }
            .padding(24)
        }
        .background(Color(red: 0.23, green: 0.14, blue: 0.38).ignoresSafeArea())
        .foregroundStyle(SM.text)
    }
}

struct PrayerView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var store: DevotionService
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Button("Close") { dismiss() }
            Text("PRAYER").font(.system(size: 11, weight: .medium)).foregroundStyle(SM.accent)
            Text("Father, break up the hard ground in me. I pick up what You assigned. In Jesus’ name, Amen.")
                .font(.system(size: 22, weight: .regular))
            Button("I walked this morning") { store.markWalked(); dismiss() }
                .buttonStyle(SMButtonStyle(fill: SM.text, ink: SM.bg))
            Spacer()
        }
        .padding(24)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
        .background(Color(red: 0.23, green: 0.14, blue: 0.38).ignoresSafeArea())
        .foregroundStyle(SM.text)
    }
}
