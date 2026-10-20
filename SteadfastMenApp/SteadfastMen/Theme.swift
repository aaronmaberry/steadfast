import SwiftUI

enum SM {
    static let bg = Color(red: 0.027, green: 0.027, blue: 0.039)
    static let bg2 = Color(red: 0.047, green: 0.047, blue: 0.063)
    static let surface = Color(red: 0.071, green: 0.071, blue: 0.094)
    static let surface2 = Color(red: 0.094, green: 0.094, blue: 0.122)
    static let text = Color(red: 0.957, green: 0.957, blue: 0.961)
    static let muted = Color(red: 0.631, green: 0.631, blue: 0.667)
    static let faint = Color(red: 0.443, green: 0.443, blue: 0.478)
    static let accent = Color(red: 0.545, green: 0.612, blue: 1.0)
    static let accent2 = Color(red: 0.357, green: 0.431, blue: 0.961)
    static let indigoCard = Color(red: 0.102, green: 0.165, blue: 0.290)

    static let navy = bg
    static let navy2 = surface
    static let bone = text
    static let brass = accent
}

struct SMButtonStyle: ButtonStyle {
    var fill: Color = SM.accent2
    var ink: Color = SM.text

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 17, weight: .semibold))
            .foregroundStyle(ink)
            .frame(maxWidth: .infinity)
            .frame(minHeight: 48)
            .background(fill)
            .clipShape(Capsule())
            .opacity(configuration.isPressed ? 0.82 : 1)
    }
}
