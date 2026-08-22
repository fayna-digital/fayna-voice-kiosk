#!/bin/bash
# Installation script for AI Kiosk systemd service
set -e

echo "📦 Installing AI Kiosk systemd service..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Copy service file
cp /tmp/ai-kiosk.service /etc/systemd/system/
echo "✅ Service file copied"

# Reload systemd
systemctl daemon-reload
echo "✅ Systemd reloaded"

# Enable service
systemctl enable ai-kiosk
echo "✅ Service enabled for auto-start"

# Start service
systemctl start ai-kiosk
echo "✅ Service started"

# Check status
sleep 2
systemctl status ai-kiosk --no-pager

echo ""
echo "📊 To check logs:"
echo "  sudo journalctl -u ai-kiosk -f"
echo "  tail -f /home/ubuntu/ai-kiosk/logs/systemd.log"
echo ""
echo "🎯 To stop: sudo systemctl stop ai-kiosk"
echo "🎯 To disable: sudo systemctl disable ai-kiosk"
