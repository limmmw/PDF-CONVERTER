#!/usr/bin/env bash
# ══════════════════════════════════════════════════════
#   install_deps.sh — Instalasi dependensi konverter PDF
#   Jalankan: bash install_deps.sh
# ══════════════════════════════════════════════════════

set -e

CYAN="\033[96m"
HIJAU="\033[92m"
KUNING="\033[93m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${CYAN}${BOLD}"
echo "╔══════════════════════════════════════════════════╗"
echo "║     Instalasi Dependensi Konverter PDF           ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${RESET}"

# ── Deteksi distro ─────────────────────────────────────
if command -v apt-get &>/dev/null; then
    PKG="apt"
elif command -v dnf &>/dev/null; then
    PKG="dnf"
elif command -v pacman &>/dev/null; then
    PKG="pacman"
else
    echo -e "${KUNING}⚠  Distro tidak dikenali. Install manual:${RESET}"
    echo "   - libreoffice"
    echo "   - imagemagick"
    echo "   - python3-pip"
    echo "   - pip install Pillow reportlab"
    exit 1
fi

echo -e "${BOLD}[1/3] Update package list...${RESET}"
if [ "$PKG" = "apt" ]; then
    sudo apt-get update -qq
elif [ "$PKG" = "dnf" ]; then
    sudo dnf check-update -q || true
fi

echo -e "\n${BOLD}[2/3] Install sistem tools...${RESET}"

install_pkg() {
    local pkg="$1"
    echo -ne "  ➜  $pkg ... "
    if [ "$PKG" = "apt" ]; then
        sudo apt-get install -y -qq "$pkg" > /dev/null 2>&1 && echo -e "${HIJAU}✔ terpasang${RESET}" || echo -e "${KUNING}⚠ gagal${RESET}"
    elif [ "$PKG" = "dnf" ]; then
        sudo dnf install -y -q "$pkg" > /dev/null 2>&1 && echo -e "${HIJAU}✔ terpasang${RESET}" || echo -e "${KUNING}⚠ gagal${RESET}"
    elif [ "$PKG" = "pacman" ]; then
        sudo pacman -S --noconfirm --quiet "$pkg" > /dev/null 2>&1 && echo -e "${HIJAU}✔ terpasang${RESET}" || echo -e "${KUNING}⚠ gagal${RESET}"
    fi
}

install_pkg "libreoffice"
install_pkg "imagemagick"
install_pkg "python3-pip"

echo -e "\n${BOLD}[3/3] Install Python packages...${RESET}"
pip3 install --quiet Pillow reportlab 2>/dev/null && \
    echo -e "  ${HIJAU}✔  Pillow & reportlab terpasang${RESET}" || \
    echo -e "  ${KUNING}⚠  Gagal install Python packages${RESET}"

echo -e "\n${HIJAU}${BOLD}✔  Instalasi selesai!${RESET}"
echo -e "   Jalankan: ${CYAN}python3 convert_to_pdf.py --cek-deps${RESET} untuk verifikasi.\n"