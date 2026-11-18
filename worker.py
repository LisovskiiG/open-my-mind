"""Send due reminders via SMTP. Run periodically with a service timer."""

from email.message import EmailMessage
import logging
import os
import smtplib
import ssl
import time

from . import storage

log = logging.getLogger(__name__)


def send(item):
    url = os.environ["OPENMYMIND_MCP_URL"].removesuffix("/mcp")
    message = EmailMessage()
    message["Subject"] = "Time for a short OpenMyMind exercise"
    message["From"] = os.environ["OPENMYMIND_FROM"]
    message["To"] = item["email"]
    message.set_content(
        "Pick a question and try a quiz or an independent hypothesis in OpenMyMind.\n\n"
        f"Open ChatGPT: https://chatgpt.com/\n"
        f"Turn off reminders: {url}/unsubscribe/{item['unsubscribe_token']}\n"
    )
    host = os.environ["OPENMYMIND_SMTP_HOST"]
    port = int(os.environ.get("OPENMYMIND_SMTP_PORT", "465"))
    context = ssl.create_default_context()
    mode = os.environ.get("OPENMYMIND_SMTP_TLS", "implicit")
    if mode not in ("implicit", "starttls"):
        raise ValueError("OPENMYMIND_SMTP_TLS must be implicit or starttls.")
    transport = (smtplib.SMTP_SSL(host, port, timeout=15, context=context)
                 if mode == "implicit" else smtplib.SMTP(host, port, timeout=15))
    try:
        if mode == "starttls":
            transport.starttls(context=context)
        username = os.environ.get("OPENMYMIND_SMTP_USERNAME")
        if username:
            transport.login(username, os.environ["OPENMYMIND_SMTP_PASSWORD"])
        if storage.claim_is_current(item["account"], item["claim"]):
            transport.send_message(message)
    finally:
        transport.close()


def run_once(deliver=send):
    storage.initialize()
    cutoff = int(time.time())
    after = None
    while item := storage.claim_due(cutoff, after):
        after = item["account"]
        try:
            deliver(item)
        except (smtplib.SMTPException, OSError, ValueError, KeyError) as error:
            log.warning("Reminder delivery failed (%s).", type(error).__name__)
            storage.finish_delivery(item, False, int(time.time()))
        else:
            storage.finish_delivery(item, True, int(time.time()))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_once()
