import Foundation

enum Config {
    static let site = URL(string: "https://www.walksteadfast.com")!
    static let training = URL(string: "https://www.walksteadfast.com/training")!
    static let book = URL(string: "https://www.walksteadfast.com/book")!
    static let shop = URL(string: "https://www.walksteadfast.com/shop")!
    static let dailyWeb = URL(string: "https://www.walksteadfast.com/daily")!
    static let groups = URL(string: "https://www.walksteadfast.com/groups")!
    static let merch = URL(string: "https://www.walksteadfast.com/merch")!
    static let privacy = URL(string: "https://www.walksteadfast.com/privacy")!
    static let login = URL(string: "https://www.walksteadfast.com/login")!
    static let program = URL(string: "https://www.walksteadfast.com/program")!
    static let groupKit = URL(string: "https://www.walksteadfast.com/group-kit")!

    static func week(_ n: String) -> URL {
        URL(string: "https://www.walksteadfast.com/program#week-\(n)")!
    }

    /// Host this file on the site. Edit it each morning. The app pulls it first.
    static let dailyFeed = URL(string: "https://www.walksteadfast.com/app/daily.json")!

    /// Support page on the site. No in-app checkout — store rules for a for-profit.
    static let giveURL = URL(string: "https://www.walksteadfast.com/give")!

    /// Leave empty until the channel is live. Empty links open the website instead.
    static let youtube = ""
    static let instagram = ""
    static let x = ""
    static let facebook = ""
    static let tiktok = ""
    static let podcast = "https://www.walksteadfast.com/listen"
}
