#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
command -v qemu-system-i386 >/dev/null 2>&1 || { echo 'Install QEMU first'; exit 1; }
make run
