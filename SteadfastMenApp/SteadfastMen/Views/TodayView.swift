import SwiftUI

struct TodayView: View {
    @EnvironmentObject var store: DevotionService
    @Environment(\.openURL) private var openURL
    @State private var showWalk = false
    @State private var showTeach = false
    @State private var showVerse = false
    @State private var showPair = false

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 14) {
                    header
                    verseCard
                    guidedCard
                    teachCard
                    pairCard
                    Text("More for you")
                        .font(.system(size: 20, weight: .semibold))
                        .padding(.top, 8)
                    planCard
                }
                .padding(.horizontal, 18)
                .padding(.bottom, 28)
            }
            .background(SM.bg.ignoresSafeArea())
            .toolbar(.hidden, for: .navigationBar)
            .sheet(isPresented: $showWalk) { GuidedWalkView().presentationDragIndicator(.visible) }
            .sheet(isPresented: $showTeach) { TeachingView().presentationDragIndicator(.visible) }
            .sheet(isPresented: $showVerse) { VerseFullView(text: store.today.verse).presentationDragIndicator(.visible) }
            .sheet(isPresented: $showPair) { PairView().environmentObject(store).presentationDragIndicator(.visible) }
        }
    }

    private var header: some View {
        HStack(alignment: .center) {
            VStack(alignment: .leading, spacing: 4) {
                Text("Today")
                    .font(.system(size: 13, weight: .medium))
                    .foregroundStyle(SM.muted)
                Text(greeting)
                    .font(.system(size: 24, weight: .semibold))
                    .foregroundStyle(SM.text)
            }
            Spacer()
            HStack(spacing: 14) {
                Label("\(max(store.streak, store.hasWalkedToday ? 1 : 0))", systemImage: "bolt.fill")
                Image(systemName: "bell")
            }
            .font(.system(size: 14, weight: .semibold))
            .foregroundStyle(SM.muted)
        }
        .padding(.top, 8)
    }

    private var verseCard: some View {
        Button { showVerse = true } label: {
            VStack(alignment: .leading, spacing: 10) {
                Text("VERSE OF THE DAY")
                    .font(.system(size: 11, weight: .medium))
                    .tracking(0.8)
                    .foregroundStyle(SM.accent)
                Text(versePlain(store.today.verse))
                    .font(.system(size: 18, weight: .regular))
                    .foregroundStyle(SM.text)
                    .multilineTextAlignment(.leading)
                    .lineSpacing(3)
                if !verseRef(store.today.verse).isEmpty {
                    Text(verseRef(store.today.verse))
                        .font(.system(size: 12, weight: .medium))
                        .foregroundStyle(SM.muted)
                }
                HStack {
                    spacerAction("heart", "Walk")
                    spacerAction("bubble.right", "Notes")
                    spacerAction("square.and.arrow.up", "Share")
                    spacerAction("ellipsis", "More")
                }
                .padding(.top, 8)
                .foregroundStyle(SM.accent.opacity(0.85))
            }
            .padding(18)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(LinearGradient(colors: [SM.indigoCard, SM.bg2], startPoint: .top, endPoint: .bottom))
            .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
        }
        .buttonStyle(.plain)
    }

    private func versePlain(_ raw: String) -> String {
        var s = raw.replacingOccurrences(of: "“", with: "\"").replacingOccurrences(of: "”", with: "\"")
        if let r = s.range(of: " — ") { s = String(s[..<r.lowerBound]) }
        s = s.trimmingCharacters(in: CharacterSet(charactersIn: "\""))
        return s.trimmingCharacters(in: .whitespacesAndNewlines)
    }
    private func verseRef(_ raw: String) -> String {
        if let r = raw.range(of: " — ") {
            var tail = String(raw[r.upperBound...]).trimmingCharacters(in: .whitespacesAndNewlines)
            if !tail.uppercased().contains("NIV") { tail += " NIV" }
            return tail
        }
        return ""
    }

    private func spacerAction(_ icon: String, _ label: String) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
            Text(label).font(.system(size: 10))
        }
        .frame(maxWidth: .infinity)
    }

    private var guidedCard: some View {
        Button { showWalk = true } label: {
            HStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("DAILY SILENT TOUCH · 4–6 MIN")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(SM.accent)
                    Text("What’s on the table this morning?")
                        .font(.system(size: 17, weight: .semibold))
                        .foregroundStyle(SM.text)
                        .multilineTextAlignment(.leading)
                    Text("Stand. Watch. Then walk.")
                        .font(.system(size: 13))
                        .foregroundStyle(SM.muted)
                }
                Spacer()
                RoundedRectangle(cornerRadius: 12).fill(SM.surface2).frame(width: 84, height: 68)
            }
            .padding(14)
            .background(SM.surface)
            .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        }
        .buttonStyle(.plain)
    }

    private var teachCard: some View {
        Button { showTeach = true } label: {
            HStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("TEACHING")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(SM.accent)
                    Text(store.today.title)
                        .font(.system(size: 17, weight: .semibold))
                        .foregroundStyle(SM.text)
                        .multilineTextAlignment(.leading)
                    Text("Wes & Jonathan · table")
                        .font(.system(size: 13))
                        .foregroundStyle(SM.muted)
                }
                Spacer()
                Circle().fill(SM.surface2).frame(width: 64, height: 64)
            }
            .padding(14)
            .background(SM.surface)
            .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        }
        .buttonStyle(.plain)
    }

    private var pairCard: some View {
        Button { showPair = true } label: {
            HStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("THIS LESSON’S ACT · PAIR")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(SM.accent)
                    Text("Phone down at the table")
                        .font(.system(size: 17, weight: .semibold))
                        .foregroundStyle(SM.text)
                    Text(store.pairName.isEmpty
                         ? "Name one brother for these six lessons."
                         : "Brother: \(store.pairName). Midweek he asks. Shame stays off the stage.")
                        .font(.system(size: 13))
                        .foregroundStyle(SM.muted)
                        .multilineTextAlignment(.leading)
                }
                Spacer()
            }
            .padding(14)
            .background(SM.surface)
            .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        }
        .buttonStyle(.plain)
    }

    private var planCard: some View {
        Button { openURL(Config.training) } label: {
            HStack {
                VStack(alignment: .leading, spacing: 6) {
                    Text("24 LESSONS")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(SM.accent)
                    Text("The path")
                        .font(.system(size: 18, weight: .semibold))
                        .foregroundStyle(SM.text)
                    Text("Four marks. One act, at your pace.")
                        .font(.system(size: 13))
                        .foregroundStyle(SM.muted)
                }
                Spacer()
            }
            .padding(16)
            .background(SM.surface)
            .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        }
        .buttonStyle(.plain)
    }

    private var greeting: String {
        let h = Calendar.current.component(.hour, from: Date())
        let w = h < 12 ? "morning" : h < 17 ? "afternoon" : "evening"
        return "Good \(w)"
    }
}

struct GuidedWalkView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var store: DevotionService
    @State private var step = 0
    private let steps: [(String, String, String)] = [
        ("Welcome", "Come as you are.", "Take a few deep breaths. Prepare for this time with God."),
        ("Honor God", "Be watchful. Stand firm. Act like men.", "The God over the day is the God in this minute."),
        ("My house", "Cast your cares on the Lord.", "Name the place you have gone passive. Hand it over."),
        ("His will", "Your kingdom come.", "Ask for one act of obedience you can finish before noon."),
        ("Closing", "Two intentional breaths.", "Inhale the assignment. Exhale the drift. Then walk.")
    ]

    var body: some View {
        ZStack(alignment: .bottom) {
            SM.bg.ignoresSafeArea()
            VStack(alignment: .leading, spacing: 16) {
                HStack {
                    Button("Close") { dismiss() }.foregroundStyle(SM.text)
                    Spacer()
                }
                Spacer()
                Text(steps[step].0.uppercased())
                    .font(.system(size: 11, weight: .medium))
                    .tracking(1.4)
                    .foregroundStyle(SM.muted)
                Text(steps[step].1)
                    .font(.system(size: 28, weight: .medium))
                    .foregroundStyle(SM.text)
                Text(steps[step].2)
                    .font(.system(size: 17))
                    .foregroundStyle(SM.muted)
                Spacer()
                Button(step == steps.count - 1 ? "I walked this morning" : "Continue") {
                    if step < steps.count - 1 { step += 1 }
                    else { store.markWalked(); dismiss() }
                }
                .buttonStyle(SMButtonStyle(fill: SM.text, ink: SM.bg))
            }
            .padding(24)
        }
    }
}

struct TeachingView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var store: DevotionService
    @Environment(\.openURL) private var openURL

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Button("Close") { dismiss() }
                Spacer()
            }
            Text("TEACHING")
                .font(.system(size: 11, weight: .medium))
                .foregroundStyle(SM.accent)
            Text(store.today.title)
                .font(.system(size: 28, weight: .medium))
            Text("Wes & Jonathan at the locked table. Drop the film URL into daily.json → videoURL.")
                .foregroundStyle(SM.muted)
            if let raw = store.today.videoURL, let url = URL(string: raw), !raw.isEmpty {
                Button("Watch today’s film") { openURL(url) }
                    .buttonStyle(SMButtonStyle())
            }
            Spacer()
        }
        .padding(24)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
        .background(SM.bg.ignoresSafeArea())
        .foregroundStyle(SM.text)
    }
}

struct VerseFullView: View {
    @Environment(\.dismiss) private var dismiss
    let text: String
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Button("Close") { dismiss() }
            Spacer()
            Text("SCRIPTURE")
                .font(.system(size: 11, weight: .medium))
                .tracking(1.4)
                .foregroundStyle(SM.muted)
            Text(text)
                .font(.system(size: 26, weight: .regular))
            Spacer()
        }
        .padding(24)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
        .background(SM.bg.ignoresSafeArea())
        .foregroundStyle(SM.text)
    }
}
