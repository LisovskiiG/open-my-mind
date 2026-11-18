"""Build the installable OpenMyMind plugin ZIP for a deployed MCP server."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--url", required=True, help="Public HTTPS URL of the /mcp endpoint")
parser.add_argument("--client-id", required=True, help="Public OAuth client identifier")
parser.add_argument("--token-auth", default="client_secret_basic",
                    choices=("client_secret_basic", "client_secret_post", "none"))
parser.add_argument("--output", type=Path, default=Path("OpenMyMind-v2-plugin.zip"))
args = parser.parse_args()
url = urlsplit(args.url)
if url.scheme != "https" or not url.hostname or url.path != "/mcp" or url.username or url.query or url.fragment:
    parser.error("--url must be a public HTTPS URL ending in /mcp.")

config = {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
    "mcpServers": {"openmymind": {
        "type": "streamable-http", "url": args.url,
        "extensions": {"com.openai": {"auth": {
            "type": "oauth",
            "client": {"mode": "provided", "clientId": args.client_id,
                       "tokenEndpointAuthMethod": args.token_auth},
            "baseScopes": ["openmymind"],
            "resource": args.url,
        }}},
    }},
}
root = Path(__file__).resolve().parent
with ZipFile(args.output, "w", ZIP_DEFLATED) as package:
    package.write(root / "plugin.json", "plugin.json")
    skill = "skills/think-first/SKILL.md"
    package.write(root / skill, skill)
    package.writestr("mcp.json", json.dumps(config, indent=2) + "\n")
print(args.output)
