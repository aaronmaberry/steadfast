import SwiftUI

struct YouView: View {
    @EnvironmentObject var store: DevotionService
    @Environment(\.openURL) private var openURL
    @State private var showPair = false

    var body: some View {
        NavigationStack {
            List {
                Section {
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Brother").font(.system(size: 26, weight: .semibold))
                            Text("Daily is free. The pair sits behind the path.").foregroundStyle(SM.muted)
                        }
                        Spacer()
                    }
                    .listRowBackground(SM.bg)
                }
                Section {
                    HStack {
                        VStack(alignment: .leading) {
                            Text("\(max(store.streak, store.hasWalkedToday ? 1 : 0))")
                                .font(.system(size: 28, weight: .medium))
                            Text("Walk streak").font(.system(size: 12)).foregroundStyle(SM.muted)
                        }
                        Spacer()
                        VStack(alignment: .leading) {
                            Text("—").font(.system(size: 28, weight: .medium))
                            Text("Days this year · slot").font(.system(size: 12)).foregroundStyle(SM.muted)
                        }
                    }
                    .listRowBackground(SM.surface)
                }
                Section("Account") {
                    Toggle("I bought the 24 lessons", isOn: Binding(
                        get: { UserDefaults.standard.bool(forKey: "sm.member") },
                        set: { UserDefaults.standard.set($0, forKey: "sm.member") }
                    ))
                    Button("Delete my data on this phone") {
                        ["sm.member", "sm.pairName", "sm.pairPing"].forEach {
                            UserDefaults.standard.removeObject(forKey: $0)
                        }
                        store.pairName = ""
                        store.pairPinged = ""
                    }
                    Text("To delete a paid login, write hello@walksteadfast.com.")
                        .font(.footnote)
                        .foregroundStyle(SM.muted)
                }
                Section("The pair") {
                    Button(store.pairName.isEmpty ? "Name a brother for this mark" : "Brother: \(store.pairName)") {
                        showPair = true
                    }
                }
                Section("Support") {
                    NavigationLink("Help expand the mission") { GiveView() }
                }
                Section("The house") {
                    Button("Privacy") { openURL(Config.privacy) }
                    Button("The path on the web") { openURL(Config.program) }
                    Button("Website") { openURL(Config.site) }
                }
                Section("Socials") {
                    ForEach(["YouTube", "Instagram", "X", "Facebook", "TikTok"], id: \.self) { name in
                        Button(name) { openURL(Config.site) }
                    }
                }
            }
            .scrollContentBackground(.hidden)
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("You")
            .sheet(isPresented: $showPair) { PairView().environmentObject(store) }
        }
    }
}
