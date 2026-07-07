import os
from pbxproj import XcodeProject
from pbxproj.pbxextensions.ProjectFiles import ProjectFiles

orig_filter = ProjectFiles._filter_targets_without_path

def patched_filter(self, path, target_name):
    try:
        return orig_filter(self, path, target_name)
    except AttributeError:
        return target_name

ProjectFiles._filter_targets_without_path = patched_filter

project_path = 'apps/omlx-mac/oMLX.xcodeproj/project.pbxproj'
project = XcodeProject.load(project_path)

files_to_add = [
    'Sources/AppView/ViewModels/GlobalSearchViewModel.swift',
    'Sources/AppView/Screens/SearchView.swift',
    'Sources/AppView/Screens/SettingsView.swift',
    'Sources/AppView/Screens/PreferencesView.swift',
    'Sources/AppView/Utils/KeyboardShortcutManager.swift',
    'Sources/AppView/Utils/WindowStateManager.swift',
    'Sources/AppView/Utils/AppearanceManager.swift'
]

for file in files_to_add:
    project.add_file(file, force=False, target_name='oMLX')

test_files = [
    'Tests/oMLXTests/GUI008Tests.swift'
]

for file in test_files:
    project.add_file(file, force=False, target_name='oMLXTests')

project.save()
print("Successfully added GUI-008 files to Xcode project.")
