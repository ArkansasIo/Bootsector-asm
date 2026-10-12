#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
command -v nasm >/dev/null 2>&1 || { echo 'NASM is required'; exit 1; }
make components image verify
