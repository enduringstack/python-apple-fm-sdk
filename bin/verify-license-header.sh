#!/bin/bash

# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

# This script verifies that all source files in the repository contain 
# the correct license header.
# It checks for the presence of the license header in all source files and 
# reports any files that are missing the header.

# ============================================================================
# LICENSE TEXT - Define once, use everywhere
# ============================================================================
LICENSE_LINE_1="For licensing see accompanying LICENSE file."
LICENSE_LINE_2="Copyright (C) 2026 Apple Inc. All Rights Reserved."

# ============================================================================
# LICENSE HEADER FORMATTERS - Generate headers with appropriate comment syntax
# ============================================================================

# Python files - hash comments
PYTHON_LICENSE_HEADER='# '"${LICENSE_LINE_1}"'
# '"${LICENSE_LINE_2}"'

'

# C, Swift, and CSS files - block comment
SWIFT_LICENSE_HEADER='/*
'"${LICENSE_LINE_1}"'
'"${LICENSE_LINE_2}"'
*/

'

# Bash scripts - hash comments with shebang
BASH_LICENSE_HEADER='#!/bin/bash

# '"${LICENSE_LINE_1}"'
# '"${LICENSE_LINE_2}"'
'

# Text files (requirements.txt, Makefile) - hash comments
TEXT_LICENSE_HEADER='# '"${LICENSE_LINE_1}"'
# '"${LICENSE_LINE_2}"'

'

# RST documentation files - RST comment block
RST_LICENSE_HEADER='..
    '"${LICENSE_LINE_1}"'
    '"${LICENSE_LINE_2}"'

'

# README.md files - footer with separator
READMEMD_LICENSE_FOOTER='
---
'"${LICENSE_LINE_1}"'
'"${LICENSE_LINE_2}"'
'

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
MISSING_COUNT=0
FIXED_COUNT=0
CHECKED_COUNT=0

# Function to check if a file has the correct license header
check_license_header() {
    local file="$1"
    local expected_header="$2"
    local is_footer="$3"
    local is_bash="${4:-false}"
    
    if [ "$is_footer" = "true" ]; then
        # For footers, check if the license text appears at the end of the file
        if tail -n 5 "$file" | grep -q "${LICENSE_LINE_1}" && \
           tail -n 5 "$file" | grep -q "${LICENSE_LINE_2}"; then
            return 0
        else
            return 1
        fi
    elif [ "$is_bash" = "true" ]; then
        # For bash files, check if license appears after shebang (lines 2-4)
        if head -n 5 "$file" | grep -q "${LICENSE_LINE_1}" && \
           head -n 5 "$file" | grep -q "${LICENSE_LINE_2}"; then
            return 0
        else
            return 1
        fi
    else
        # For all other headers, check if license text appears in first few lines
        if head -n 10 "$file" | grep -q "${LICENSE_LINE_1}" && \
           head -n 10 "$file" | grep -q "${LICENSE_LINE_2}"; then
            return 0
        else
            return 1
        fi
    fi
}

# Function to add license header to a file
add_license_header() {
    local file="$1"
    local header="$2"
    local is_footer="$3"
    local is_bash="${4:-false}"
    
    if [ "$is_footer" = "true" ]; then
        # Add footer to the end of the file
        echo "$header" >> "$file"
    elif [ "$is_bash" = "true" ]; then
        # For bash files, insert license after the shebang line
        local temp_file=$(mktemp)
        head -n 1 "$file" > "$temp_file"  # Keep the shebang
        echo "" >> "$temp_file"
        echo "# ${LICENSE_LINE_1}" >> "$temp_file"
        echo "# ${LICENSE_LINE_2}" >> "$temp_file"
        echo "" >> "$temp_file"
        tail -n +2 "$file" >> "$temp_file"  # Add rest of file
        mv "$temp_file" "$file"
    else
        # Add header to the beginning of the file
        local temp_file=$(mktemp)
        echo -n "$header" > "$temp_file"
        cat "$file" >> "$temp_file"
        mv "$temp_file" "$file"
    fi
}

# Function to process a file
process_file() {
    local file="$1"
    local header="$2"
    local is_footer="${3:-false}"
    local is_bash="${4:-false}"
    
    CHECKED_COUNT=$((CHECKED_COUNT + 1))
    
    if ! check_license_header "$file" "$header" "$is_footer" "$is_bash"; then
        echo -e "${YELLOW}Missing license in: $file${NC}"
        MISSING_COUNT=$((MISSING_COUNT + 1))
        
        # Add the license header
        add_license_header "$file" "$header" "$is_footer" "$is_bash"
        echo -e "${GREEN}Added license to: $file${NC}"
        FIXED_COUNT=$((FIXED_COUNT + 1))
    fi
}

echo "Checking license headers in the repository..."
echo ""

# Find and process Python files
while IFS= read -r -d '' file; do
    process_file "$file" "$PYTHON_LICENSE_HEADER"
done < <(find . -type f -name "*.py" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process Swift files
while IFS= read -r -d '' file; do
    process_file "$file" "$SWIFT_LICENSE_HEADER"
done < <(find . -type f -name "*.swift" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process C files
while IFS= read -r -d '' file; do
    process_file "$file" "$SWIFT_LICENSE_HEADER"
done < <(find . -type f -name "*.c" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process header files
while IFS= read -r -d '' file; do
    process_file "$file" "$SWIFT_LICENSE_HEADER"
done < <(find . -type f -name "*.h" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process CSS files
while IFS= read -r -d '' file; do
    process_file "$file" "$SWIFT_LICENSE_HEADER"
done < <(find . -type f -name "*.css" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process bash scripts (excluding this script itself)
while IFS= read -r -d '' file; do
    # Skip this script itself
    if [[ "$file" != "./bin/verify-license-header.sh" ]]; then
        # Check if file starts with shebang
        if head -n 1 "$file" | grep -q "^#!/bin/bash"; then
            process_file "$file" "$BASH_LICENSE_HEADER" "false" "true"
        fi
    fi
done < <(find . -type f -name "*.sh" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process RST files
while IFS= read -r -d '' file; do
    process_file "$file" "$RST_LICENSE_HEADER"
done < <(find . -type f -name "*.rst" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process requirements.txt files
while IFS= read -r -d '' file; do
    process_file "$file" "$TEXT_LICENSE_HEADER"
done < <(find . -type f -name "requirements.txt" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process Makefile
while IFS= read -r -d '' file; do
    process_file "$file" "$TEXT_LICENSE_HEADER"
done < <(find . -type f -name "Makefile" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

# Find and process README.md files (with footer instead of header)
while IFS= read -r -d '' file; do
    process_file "$file" "$READMEMD_LICENSE_FOOTER" "true"
done < <(find . -type f -name "README.md" ! -path "./.venv/*" ! -path "./build/*" ! -path "./.build/*" ! -path "*/.*" -print0)

echo ""
echo "======================================"
echo "License Header Verification Complete"
echo "======================================"
echo -e "Files checked: ${CHECKED_COUNT}"
echo -e "${YELLOW}Files missing license: ${MISSING_COUNT}${NC}"
echo -e "${GREEN}Files fixed: ${FIXED_COUNT}${NC}"
echo ""

if [ $MISSING_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ All source files have correct license headers!${NC}"
    exit 0
else
    echo -e "${GREEN}✓ All missing license headers have been added!${NC}"
    exit 0
fi
