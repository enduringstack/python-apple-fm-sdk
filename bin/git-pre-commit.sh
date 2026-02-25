#!/bin/bash

# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

echo "Formatting Python code with ruff..."
ruff format
echo "Formatting Swift code with swiftformat"
swift format . --recursive --in-place