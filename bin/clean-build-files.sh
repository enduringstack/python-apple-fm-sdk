#!/bin/bash

# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.


# Clean script to remove build artifacts

# Remove foundation-models-c/.build folder if it exists
if [ -d "foundation-models-c/.build" ]; then
    echo "Removing foundation-models-c/.build folder..."
    rm -rf foundation-models-c/.build
    echo "✓ foundation-models-c/.build folder removed"
else
    echo "✓ No foundation-models-c/.build folder found"
fi

# Remove generated Python bindings
if [ -f "src/apple_fm_sdk/_ctypes_bindings.py" ]; then
    echo "Removing generated _ctypes_bindings.py..."
    rm "src/apple_fm_sdk/_ctypes_bindings.py"
    echo "✓ _ctypes_bindings.py removed"
else
    echo "✓ No _ctypes_bindings.py found"
fi

# Remove compiled libraries
if [ -d "src/apple_fm_sdk/lib" ]; then
    echo "Removing compiled lib/ directory..."
    rm -rf "src/apple_fm_sdk/lib"
    echo "✓ lib/ directory removed"
else
    echo "✓ No lib/ directory found"
fi

# Remove Python build artifacts
if [ -d "build" ]; then
    echo "Removing build/ directory..."
    rm -rf "build"
    echo "✓ build/ directory removed"
else
    echo "✓ No build/ directory found"
fi

if [ -d "dist" ]; then
    echo "Removing dist/ directory..."
    rm -rf "dist"
    echo "✓ dist/ directory removed"
else
    echo "✓ No dist/ directory found"
fi

if [ -d "src/apple_fm_sdk.egg-info" ]; then
    echo "Removing .egg-info directory..."
    rm -rf "src/apple_fm_sdk.egg-info"
    echo "✓ .egg-info directory removed"
else
    echo "✓ No .egg-info directory found"
fi

echo "Build cleanup completed!"
