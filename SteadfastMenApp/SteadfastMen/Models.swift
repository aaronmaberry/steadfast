import Foundation

struct DailyFeed: Codable {
    var updated: String?
    var items: [Devotion]
}

struct Devotion: Codable, Identifiable, Hashable {
    var date: String
    var title: String
    var verse: String
    var body: String
    var videoURL: String?
    var imageURL: String?

    var id: String { date }
}

struct Product: Identifiable {
    let id: String
    let eyebrow: String
    let title: String
    let price: String
    let blurb: String
    let url: URL
}

struct Social: Identifiable {
    let id: String
    let name: String
    let urlString: String
}
