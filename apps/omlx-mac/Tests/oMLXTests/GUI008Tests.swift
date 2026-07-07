import XCTest
import SwiftUI
@testable import oMLX

@MainActor
final class GUI008Tests: XCTestCase {

    func testWindowStateManagerPersistence() {
        let manager = WindowStateManager()
        manager.sidebarWidth = 250
        XCTAssertEqual(manager.sidebarWidth, 250)
        XCTAssertEqual(UserDefaults.standard.double(forKey: "WindowState.sidebarWidth"), 250)

        manager.lastSelectedSection = .chat
        XCTAssertEqual(manager.lastSelectedSection, .chat)
    }

    func testAppearanceManagerPersistence() {
        let manager = AppearanceManager()
        manager.currentAppearance = .dark
        XCTAssertEqual(manager.currentAppearance, .dark)
        XCTAssertEqual(UserDefaults.standard.string(forKey: "Appearance.current"), "Dark")

        XCTAssertEqual(AppAppearance.dark.colorScheme, .dark)
        XCTAssertEqual(AppAppearance.light.colorScheme, .light)
        XCTAssertNil(AppAppearance.system.colorScheme)
    }

    func testKeyboardShortcutManager() {
        let manager = KeyboardShortcutManager()
        let expectation = XCTestExpectation(description: "Action published")

        let cancellable = manager.actionPublisher.sink { action in
            if case .toggleSidebar = action {
                expectation.fulfill()
            }
        }

        manager.perform(.toggleSidebar)
        wait(for: [expectation], timeout: 1.0)
        cancellable.cancel()
    }

    func testAppSectionNavigationProperties() {
        XCTAssertEqual(AppSection.chat.title, "Chat Workspace")
        XCTAssertEqual(AppSection.compiler.title, "Compiler Explorer")
        XCTAssertEqual(AppSection.developer.title, "Developer Studio")

        XCTAssertEqual(AppSection.chat.symbol, "bubble.left.and.bubble.right")
        XCTAssertEqual(AppSection.compiler.symbol, "cpu")
        XCTAssertEqual(AppSection.developer.symbol, "hammer")
    }
}
