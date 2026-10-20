import SwiftUI
import WebKit

struct PathWeek: Identifiable {
    let id: String
    let title: String
}

struct InAppWebView: UIViewRepresentable {
    let url: URL
    func makeUIView(context: Context) -> WKWebView { WKWebView() }
    func updateUIView(_ webView: WKWebView, context: Context) {
        if webView.url != url { webView.load(URLRequest(url: url)) }
    }
}

struct PathView: View {
    @Environment(\.openURL) private var openURL
    @AppStorage("sm.member") private var isMember = false
    @State private var webURL: URL? = nil

    private let weeks: [PathWeek] = [
        .init(id: "01", title: "Name the drift in your own house."),
        .init(id: "02", title: "Stop waiting for someone else to captain the room."),
        .init(id: "03", title: "Put the phone down at the table."),
        .init(id: "04", title: "Tell the truth about the quiet sins."),
        .init(id: "05", title: "Show up to church as a man, not a guest."),
        .init(id: "06", title: "Close the first mark."),
        .init(id: "07", title: "Write what is yours."),
        .init(id: "08", title: "Provide without theater."),
        .init(id: "09", title: "Confess what you have left half-done."),
        .init(id: "10", title: "Carry the calendar of your house."),
        .init(id: "11", title: "Make a plan a boy can see."),
        .init(id: "12", title: "Close the second mark."),
        .init(id: "13", title: "Go first in the hard conversation."),
        .init(id: "14", title: "Pray out loud where your people can hear it."),
        .init(id: "15", title: "Protect what you will not joke about."),
        .init(id: "16", title: "Discipline without rage."),
        .init(id: "17", title: "Lead when it costs you the easy room."),
        .init(id: "18", title: "Close the third mark."),
        .init(id: "19", title: "Lift your eyes past payday."),
        .init(id: "20", title: "Work as worship, not as a brand."),
        .init(id: "21", title: "Stay when leaving would be simpler."),
        .init(id: "22", title: "Bless your son with a future, not a mood."),
        .init(id: "23", title: "Hold the greater city in view."),
        .init(id: "24", title: "Finish. Begin again as a different man.")
    ]

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    Text("The path")
                        .font(.system(size: 34, weight: .semibold))
                        .foregroundStyle(SM.text)
                    Text("Sign in if you bought the 24 lessons. An ebook or audiobook on its own does not use this door. Those files go to the email on the receipt. The daily walk is free.")
                        .font(.system(size: 15))
                        .foregroundStyle(SM.muted)

                    if !isMember {
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Training login only. Bought just the ebook or the audiobook? Check the inbox on the Stripe receipt.")
                                .foregroundStyle(SM.muted)
                            Button("I bought the 24 lessons") { isMember = true }
                                .buttonStyle(.borderedProminent)
                            Button("Sign in") { webURL = Config.login }
                        }
                        .padding(16)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(SM.surface)
                        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                    } else {
                        libraryRow
                        ForEach(weeks) { week in
                            Button {
                                webURL = Config.week(week.id)
                            } label: {
                                VStack(alignment: .leading, spacing: 6) {
                                    Text("LESSON \(week.id)")
                                        .font(.system(size: 11, weight: .medium))
                                        .tracking(0.8)
                                        .foregroundStyle(SM.accent)
                                    Text(week.title)
                                        .font(.system(size: 18, weight: .semibold))
                                        .foregroundStyle(SM.text)
                                        .multilineTextAlignment(.leading)
                                    Text("Lecture · this lesson’s pages · the act")
                                        .font(.system(size: 13))
                                        .foregroundStyle(SM.muted)
                                }
                                .padding(16)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(SM.surface)
                                .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
                .padding(24)
                .frame(maxWidth: 720, alignment: .leading)
                .frame(maxWidth: .infinity)
            }
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("Library")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(item: Binding(get: { webURL.map { IdentifiableURL(url: $0) } }, set: { webURL = $0?.url })) { item in
                InAppWebView(url: item.url)
                    .ignoresSafeArea()
            }
        }
    }

    private var libraryRow: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("IN THE PLAN")
                .font(.system(size: 11, weight: .medium))
                .foregroundStyle(SM.accent)
            Text("Audiobook")
                .font(.system(size: 20, weight: .semibold))
                .foregroundStyle(SM.text)
            Text("Player slot. File drops here when Wes locks the chapters. Until then the same file is on /program after login.")
                .font(.system(size: 14))
                .foregroundStyle(SM.muted)
            Button("Play") { webURL = Config.program }
            Text("Ebook is not read in this app. Training members open it on the path. Solo ebook buyers use the receipt email.")
                .font(.system(size: 14))
                .foregroundStyle(SM.muted)
            Button("Daily podcast (free)") { openURL(URL(string: Config.podcast) ?? Config.site) }
            Button("Lead a room · scripts and bulk paper") { openURL(Config.groupKit) }
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(SM.surface)
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
    }
}

struct IdentifiableURL: Identifiable {
    let id = UUID()
    let url: URL
}
        .init(id: "01", title: "Name the drift in your own house."),
        .init(id: "02", title: "Stop waiting for someone else to captain the room."),
        .init(id: "03", title: "Put the phone down at the table."),
        .init(id: "04", title: "Tell the truth about the quiet sins."),
        .init(id: "05", title: "Show up to church as a man, not a guest."),
        .init(id: "06", title: "Close the first mark."),
        .init(id: "07", title: "Write what is yours."),
        .init(id: "08", title: "Provide without theater."),
        .init(id: "09", title: "Confess what you have left half-done."),
        .init(id: "10", title: "Carry the calendar of your house."),
        .init(id: "11", title: "Make a plan a boy can see."),
        .init(id: "12", title: "Close the second mark."),
        .init(id: "13", title: "Go first in the hard conversation."),
        .init(id: "14", title: "Pray out loud where your people can hear it."),
        .init(id: "15", title: "Protect what you will not joke about."),
        .init(id: "16", title: "Discipline without rage."),
        .init(id: "17", title: "Lead when it costs you the easy room."),
        .init(id: "18", title: "Close the third mark."),
        .init(id: "19", title: "Lift your eyes past payday."),
        .init(id: "20", title: "Work as worship, not as a brand."),
        .init(id: "21", title: "Stay when leaving would be simpler."),
        .init(id: "22", title: "Bless your son with a future, not a mood."),
        .init(id: "23", title: "Hold the greater city in view."),
        .init(id: "24", title: "Finish. Begin again as a different man.")
    ]

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    Text("The path")
                        .font(.system(size: 34, weight: .semibold))
                        .foregroundStyle(SM.text)
                    Text("Sign in if you bought the 24 lessons. An ebook or audiobook on its own does not use this door. Those files go to the email on the receipt. The daily walk is free.")
                        .font(.system(size: 15))
                        .foregroundStyle(SM.muted)

                    if !isMember {
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Training login only. Bought just the ebook or the audiobook? Check the inbox on the Stripe receipt.")
                                .foregroundStyle(SM.muted)
                            Button("I bought the 24 lessons") { isMember = true }
                                .buttonStyle(.borderedProminent)
                            Button("Sign in on the site") { openURL(Config.login) }
                        }
                        .padding(16)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(SM.surface)
                        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                    } else {
                        libraryRow
                        ForEach(weeks) { week in
                            Button {
                                openURL(Config.week(week.id))
                            } label: {
                                VStack(alignment: .leading, spacing: 6) {
                                    Text("LESSON \(week.id)")
                                        .font(.system(size: 11, weight: .medium))
                                        .tracking(0.8)
                                        .foregroundStyle(SM.accent)
                                    Text(week.title)
                                        .font(.system(size: 18, weight: .semibold))
                                        .foregroundStyle(SM.text)
                                        .multilineTextAlignment(.leading)
                                    Text("Lecture · this lesson’s pages · the act")
                                        .font(.system(size: 13))
                                        .foregroundStyle(SM.muted)
                                }
                                .padding(16)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(SM.surface)
                                .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
                .padding(24)
                .frame(maxWidth: 720, alignment: .leading)
                .frame(maxWidth: .infinity)
            }
            .background(SM.bg.ignoresSafeArea())
            .navigationTitle("Library")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private var libraryRow: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("IN THE PLAN")
                .font(.system(size: 11, weight: .medium))
                .foregroundStyle(SM.accent)
            Text("Audiobook")
                .font(.system(size: 20, weight: .semibold))
                .foregroundStyle(SM.text)
            Text("Player slot. File drops here when Wes locks the chapters. Until then the same file is on /program after login.")
                .font(.system(size: 14))
                .foregroundStyle(SM.muted)
            Button("Play on the site") { openURL(Config.program) }
            Text("Ebook is not read in this app. Training members open it on the path. Solo ebook buyers use the receipt email.")
                .font(.system(size: 14))
                .foregroundStyle(SM.muted)
            Button("Daily podcast (free)") { openURL(URL(string: Config.podcast) ?? Config.site) }
            Button("Lead a room · scripts and bulk paper") { openURL(Config.groupKit) }
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(SM.surface)
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
    }
}
