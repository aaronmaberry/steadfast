import Foundation

@MainActor
final class DevotionService: ObservableObject {
    @Published var today: Devotion
    @Published var source: String = "bundled"
    @Published var lastError: String?

    private let defaults = UserDefaults.standard

    init() {
        today = Self.bundledToday()
    }

    func load() async {
        do {
            var req = URLRequest(url: Config.dailyFeed)
            req.cachePolicy = .reloadIgnoringLocalCacheData
            req.timeoutInterval = 8
            let (data, _) = try await URLSession.shared.data(for: req)
            let feed = try JSONDecoder().decode(DailyFeed.self, from: data)
            if let match = Self.pick(from: feed.items) {
                today = match
                source = "live"
                lastError = nil
                return
            }
        } catch {
            lastError = error.localizedDescription
        }
        today = Self.bundledToday()
        source = "bundled"
    }

    var streak: Int {
        get { defaults.integer(forKey: "sm.streak") }
        set { defaults.set(newValue, forKey: "sm.streak") }
    }

    func markWalked() {
        let key = "sm.walked." + today.date
        let last = defaults.string(forKey: "sm.lastWalk")
        if defaults.bool(forKey: key) { return }
        defaults.set(true, forKey: key)
        if last == yesterdayString() {
            streak += 1
        } else {
            streak = max(1, streak == 0 ? 1 : 1)
            if last != today.date { streak = 1 }
        }
        defaults.set(today.date, forKey: "sm.lastWalk")
        objectWillChange.send()
    }

    var hasWalkedToday: Bool {
        defaults.bool(forKey: "sm.walked." + today.date)
    }

    var pairName: String {
        get { defaults.string(forKey: "sm.pairName") ?? "" }
        set { defaults.set(newValue, forKey: "sm.pairName"); objectWillChange.send() }
    }

    var pairPinged: String {
        get { defaults.string(forKey: "sm.pairPing") ?? "" }
        set { defaults.set(newValue, forKey: "sm.pairPing"); objectWillChange.send() }
    }

    func pingPair() {
        let f = DateFormatter()
        f.dateStyle = .short
        f.timeStyle = .short
        pairPinged = f.string(from: Date())
    }

    private func yesterdayString() -> String {
        let d = Calendar.current.date(byAdding: .day, value: -1, to: Date()) ?? Date()
        return Self.dayFormatter.string(from: d)
    }

    static let dayFormatter: DateFormatter = {
        let f = DateFormatter()
        f.calendar = Calendar(identifier: .gregorian)
        f.locale = Locale(identifier: "en_US_POSIX")
        f.dateFormat = "yyyy-MM-dd"
        return f
    }()

    static func pick(from items: [Devotion]) -> Devotion? {
        let key = dayFormatter.string(from: Date())
        if let exact = items.first(where: { $0.date == key }) { return exact }
        return items.sorted { $0.date > $1.date }.first
    }

    static func bundledToday() -> Devotion {
        if let url = Bundle.main.url(forResource: "daily", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let feed = try? JSONDecoder().decode(DailyFeed.self, from: data),
           let match = pick(from: feed.items) {
            return match
        }
        return Devotion(
            date: dayFormatter.string(from: Date()),
            title: "Stand still before you stride",
            verse: "“Be watchful, stand firm in the faith, act like men, be strong. Let all that you do be done in love.” — 1 Corinthians 16:13–14",
            body: "A steadfast man does not confuse motion with obedience. Before the meeting — stand. Watch. Then walk.",
            videoURL: nil,
            imageURL: nil
        )
    }
}
