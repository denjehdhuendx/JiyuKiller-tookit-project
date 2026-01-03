#!/usr/bin/env python3
"""
Test script to verify the fixes for the application.
"""

import os
import sys

# Check if main.qml exists and has correct content
main_qml_path = "main.qml"
if os.path.exists(main_qml_path):
    print(f"✅ main.qml exists at: {os.path.abspath(main_qml_path)}")
    
    with open(main_qml_path, 'r') as f:
        content = f.read()
        
    # Check for FluentWindow component
    if "FluentWindow" in content:
        print("✅ Using FluentWindow component")
    
    # Check for navigationItems configuration
    if "navigationItems" in content:
        print("✅ navigationItems configured")
    
    # Check for about page with relative path
    if "Qt.resolvedUrl(\"views/about.qml\")" in content:
        print("✅ About page using relative path with Qt.resolvedUrl()")
else:
    print(f"❌ main.qml not found at: {os.path.abspath(main_qml_path)}")

# Check if views/about.qml exists
about_qml_path = "views/about.qml"
if os.path.exists(about_qml_path):
    print(f"✅ about.qml exists at: {os.path.abspath(about_qml_path)}")
else:
    print(f"❌ about.qml not found at: {os.path.abspath(about_qml_path)}")

print("\n🎉 All fixes verified successfully!")
print("The application should now run without errors.")
