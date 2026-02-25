#!/bin/bash

# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

set -x
set -e

# Get the current directory of this script (the bin directory)
BIN="$(cd "`dirname "$BASH_SOURCE"`"; pwd)"

# Get the project root directory (the directory at bin/ is inside)
ROOT="$(dirname "$BIN")"

# Specicy the directory to copy the hook scripts into (the .git/hooks directory)
HOOKS=$ROOT/.git/hooks

# Create the hooks directory if it doesn't already exist
if [ ! -e $HOOKS ]
then
  mkdir $HOOKS
fi

# Create a symlink from .git/hooks/pre-commit to bin/git-pre-commit.sh
if [ ! -e $HOOKS/pre-commit ]
then
  ln -fs $BIN/git-pre-commit.sh $HOOKS/pre-commit
fi

set +e
set +x