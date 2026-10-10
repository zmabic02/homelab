#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

K3S_CONFIG_SOURCE="${REPO_ROOT}/cluster/k3s/config.yaml"
K3S_CONFIG_DEST="/etc/rancher/k3s/config.yaml"

INSTALL_SCRIPT="$(mktemp)"

cleanup() {
    rm -f "$INSTALL_SCRIPT"
}

trap cleanup EXIT

sudo install -D -m 0600 \
    "$K3S_CONFIG_SOURCE" \
    "$K3S_CONFIG_DEST"

curl -sfL https://get.k3s.io -o "$INSTALL_SCRIPT"

sudo sh "$INSTALL_SCRIPT"