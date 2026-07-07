# GUI-008 Application Guide

## Overview
This document outlines the application architecture and unified experiences implemented in GUI-008.

## Unified Architecture
The application now supports multiple distinct workspaces within a single unified split-view architecture:
- Server
- Chat Workspace
- Compiler Explorer
- Developer Studio
- Models and Performance modules

The UI leverages standard SwiftUI constructs tied heavily into `AppSection` for top-level navigation, relying on `@Observable` Manager classes.

## State Management
- **WindowStateManager**: Controls and persists properties such as `sidebarWidth` and `inspectorVisible` via `UserDefaults`.
- **AppearanceManager**: Supports switching between `.light`, `.dark`, and `.system` colors, stored transparently.
- **KeyboardShortcutManager**: Injects centralized `.actionPublisher` eventing for application-wide shortcuts.
