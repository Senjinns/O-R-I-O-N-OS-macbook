#!/usr/bin/env bash
RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLIST_PATH="$HOME/Library/LaunchAgents/com.orion.assistant.plist"

cat << EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.orion.assistant</string>
    <key>ProgramArguments</key>
    <array>
        <string>$RACINE/scripts/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$RACINE/logs/launchagent_out.log</string>
    <key>StandardErrorPath</key>
    <string>$RACINE/logs/launchagent_err.log</string>
</dict>
</plist>
EOF

launchctl load "$PLIST_PATH"
echo "✅ Service LaunchAgent macOS configuré pour démarrer automatiquement."
