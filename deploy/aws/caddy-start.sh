#!/bin/sh
# Start Caddy, after writing what the Caddyfile imports for a site behind a
# name and a password. With SWISSTIP_MCP_USERNAME and SWISSTIP_MCP_PASSWORD
# the MCP site asks for basic credentials on every path, /health included;
# without them nothing is written and the site is open. Caddy keeps a hash,
# not the password; the cost is low because every request is checked against
# it, and the password is as long as its owner makes it.
set -eu

auth=/etc/caddy/auth
mkdir -p "$auth"
rm -f "$auth"/*.caddy

# The name goes into the Caddyfile as it is, where a space or a brace would be syntax.
case "${SWISSTIP_MCP_USERNAME:-}" in
    *[!A-Za-z0-9._-]*)
        echo "caddy-start: SWISSTIP_MCP_USERNAME may hold letters, digits, dots, underscores and hyphens only" >&2
        exit 64 ;;
esac

if [ -n "${SWISSTIP_MCP_USERNAME:-}" ] && [ -n "${SWISSTIP_MCP_PASSWORD:-}" ]; then
    hash=$(caddy hash-password --algorithm bcrypt --bcrypt-cost 8 --plaintext "$SWISSTIP_MCP_PASSWORD")
    printf 'basic_auth {\n\t%s %s\n}\n' "$SWISSTIP_MCP_USERNAME" "$hash" > "$auth/mcp.caddy"
    echo "caddy-start: the MCP site asks for the password of $SWISSTIP_MCP_USERNAME" >&2
elif [ -n "${SWISSTIP_MCP_USERNAME:-}${SWISSTIP_MCP_PASSWORD:-}" ]; then
    echo "caddy-start: SWISSTIP_MCP_USERNAME and SWISSTIP_MCP_PASSWORD go together; one of them is empty" >&2
    exit 64
else
    echo "caddy-start: the MCP site is open" >&2
fi

exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
