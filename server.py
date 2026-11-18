"""OpenMyMind Streamable HTTP MCP server."""

import base64
from datetime import date
from email.headerregistry import Address
from io import BytesIO
import os
from typing import Any, Literal
from urllib.parse import urlsplit

import anyio
import jwt
from matplotlib.figure import Figure
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult, ImageContent, TextContent, ToolAnnotations
from starlette.responses import HTMLResponse, PlainTextResponse

from . import storage

SCOPE = "openmymind"
Cadence = Literal["daily", "every_three_days", "off"]


def settings_url(name):
    value = os.environ[name]
    url = urlsplit(value)
    if url.scheme != "https" or not url.hostname or url.username or url.query or url.fragment:
        raise ValueError(f"{name} must be an HTTPS URL without credentials, query, or fragment.")
    return value


class OAuthVerifier(TokenVerifier):
    def __init__(self, issuer, audience, jwks_url, allowed_client):
        self.issuer = issuer
        self.audience = audience
        self.jwks = jwt.PyJWKClient(jwks_url, timeout=5)
        self.allowed_client = allowed_client

    async def verify_token(self, token):
        return await anyio.to_thread.run_sync(self.decode, token)

    def decode(self, token):
        try:
            key = self.jwks.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token, key.key, algorithms=["RS256"], audience=self.audience, issuer=self.issuer,
                options={"require": ["exp", "sub", "iss", "aud"]},
            )
        except (jwt.PyJWTError, ValueError):
            return None
        scopes = claims.get("scope", "")
        client = claims.get("client_id") or claims.get("azp")
        if not isinstance(scopes, str) or SCOPE not in scopes.split() or client != self.allowed_client:
            return None
        return AccessToken(
            token=token, client_id=client, scopes=scopes.split(), subject=claims["sub"],
            expires_at=claims["exp"], resource=self.audience, claims=claims,
        )


def plot(series, monthly):
    figure = Figure(figsize=(8, 3.6), layout="constrained")
    axes = figure.subplots()
    dates = [date.fromisoformat(point["bucket"] + ("-01" if monthly else "")) for point in series]
    values = [point["independence_percent"] for point in series]
    axes.plot(dates, values, color="#176D5B", marker="o", linewidth=2)
    axes.set(ylim=(-4, 104), ylabel="Independent answers (%)", title="OpenMyMind progress")
    axes.grid(axis="y", color="#D2DDD9", alpha=0.8)
    figure.autofmt_xdate()
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=120)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def create_server():
    public_url = settings_url("OPENMYMIND_MCP_URL")
    if urlsplit(public_url).path != "/mcp":
        raise ValueError("OPENMYMIND_MCP_URL must end with /mcp.")
    issuer = settings_url("OPENMYMIND_ISSUER")
    verifier = OAuthVerifier(
        issuer, public_url, settings_url("OPENMYMIND_JWKS_URL"), os.environ["OPENMYMIND_CLIENT_ID"],
    )
    storage.initialize()
    origin = urlsplit(public_url)
    server = FastMCP(
        "OpenMyMind", stateless_http=True, json_response=True, max_request_body_size=64 * 1024,
        auth=AuthSettings(issuer_url=issuer, resource_server_url=public_url, required_scopes=[SCOPE]),
        token_verifier=verifier,
        transport_security=TransportSecuritySettings(
            allowed_hosts=[origin.netloc], allowed_origins=[f"{origin.scheme}://{origin.netloc}"],
        ),
    )
    email_claim = os.environ.get("OPENMYMIND_EMAIL_CLAIM", "email")
    verified_claim = os.environ.get("OPENMYMIND_EMAIL_VERIFIED_CLAIM", "email_verified")
    oauth_meta = {
        "securitySchemes": [{"type": "oauth2", "scopes": [SCOPE]}],
        "openai/toolInvocation/invoking": "Updating OpenMyMind",
        "openai/toolInvocation/invoked": "OpenMyMind",
    }

    def account():
        token = get_access_token()
        if not token or not token.subject:
            raise ValueError("Connect your OpenMyMind account.")
        return token

    def tool(read_only=False, destructive=False, sends_email=False, idempotent=True, structured=True):
        return server.tool(structured_output=structured, meta=oauth_meta, annotations=ToolAnnotations(
            readOnlyHint=read_only, destructiveHint=destructive,
            openWorldHint=sends_email, idempotentHint=idempotent,
        ))

    @tool(read_only=True)
    def analytics_status() -> dict[str, Any]:
        """Read whether this account has enabled OpenMyMind progress tracking."""
        with storage.database() as db:
            return {"enabled": storage.analytics_enabled(db, account().subject)}

    @tool()
    def set_analytics(enabled: bool) -> dict[str, Any]:
        """Enable or stop progress tracking after the user's explicit choice."""
        storage.set_analytics(account().subject, enabled)
        return {"enabled": enabled}

    @tool(idempotent=False)
    def start_exercise() -> dict[str, Any]:
        """Create an exercise ID for the current question when tracking is enabled."""
        exercise = storage.start_exercise(account().subject)
        return {"exercise_id": exercise, "tracking_enabled": exercise is not None}

    @tool()
    def record_outcome(exercise_id: str, outcome: storage.Outcome) -> dict[str, Any]:
        """Save one completed practice outcome for an existing exercise ID."""
        return {"status": storage.record(account().subject, exercise_id, outcome)}

    @tool(read_only=True, structured=False)
    def progress_report(period: storage.Period = "week") -> CallToolResult:
        """Read personal practice totals and show the independence trend for 7 days, 30 days or all time."""
        report = storage.progress(account().subject, period)
        counts = ", ".join(f"{label}: {count}" for label, count in report["counts"].items())
        percent = report["independence_percent"]
        summary = "No scored exercises in this period." if percent is None else f"Independence: {percent}%."
        content = [TextContent(type="text", text=f"{summary} Counts: {counts}.")]
        if percent is not None:
            content.append(ImageContent(type="image", mimeType="image/png",
                                        data=plot(report["series"], period == "all_time")))
        return CallToolResult(content=content, structuredContent=report)

    @tool(read_only=True)
    def reminder_status() -> dict[str, Any]:
        """Read whether email reminders are enabled and when the next one is due."""
        return storage.reminder(account().subject)

    @tool(destructive=True, sends_email=True)
    def set_email_reminder(cadence: Cadence) -> dict[str, Any]:
        """Schedule or disable practice emails after the user explicitly chooses a cadence."""
        token = account()
        if cadence == "off":
            storage.disable(token.subject)
            return {"enabled": False}
        if not os.environ.get("OPENMYMIND_SMTP_HOST") or not os.environ.get("OPENMYMIND_FROM"):
            return {"status": "email_service_unavailable"}
        claims = token.claims or {}
        email = claims.get(email_claim)
        if claims.get(verified_claim) is not True or not isinstance(email, str):
            return {"status": "verified_email_required"}
        try:
            address = Address(addr_spec=email)
        except ValueError:
            return {"status": "verified_email_required"}
        if not address.domain or not address.username or len(email) > 254:
            return {"status": "verified_email_required"}
        storage.schedule(token.subject, address.addr_spec, 1 if cadence == "daily" else 3)
        return storage.reminder(token.subject)

    @server.custom_route("/unsubscribe/{token}", methods=["GET", "POST"], include_in_schema=False)
    async def unsubscribe(request):
        token = request.path_params["token"]
        if len(token) != 43 or not all(ch.isascii() and (ch.isalnum() or ch in "-_") for ch in token):
            return PlainTextResponse("Invalid link.", status_code=404)
        headers = {"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"}
        if request.method == "POST":
            await anyio.to_thread.run_sync(storage.unsubscribe, token)
            return HTMLResponse("<h1>OpenMyMind reminders turned off</h1>", headers=headers)
        return HTMLResponse(
            '<h1>OpenMyMind email reminders</h1><form method="post">'
            '<button type="submit">Turn off reminders</button></form>', headers=headers,
        )

    return server


def app():
    return create_server().streamable_http_app()
