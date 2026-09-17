# ====================================================================================
# Mailer — send an email via SMTP.

# Reads credentials from environment variables:
#     MAIL_USERNAME — SMTP username (e.g. your Gmail address)
#     MAIL_PASSWORD — SMTP password (e.g. a Gmail App Password)

# Configuration of host/port defaults to Gmail. Change SMTP_HOST and
# SMTP_PORT for other providers.
# ====================================================================================


import os
import smtplib
from email.message import EmailMessage


# Default SMTP settings (Gmail)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def _get_credentials() -> tuple[str, str]:
    # ============================================== 
    # Read credentials from the environment.

    # Raises:
    #     RuntimeError: if either MAIL_USERNAME or MAIL_PASSWORD is missing.
    # ==============================================
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "Missing MAIL_USERNAME and/or MAIL_PASSWORD environment variables. "
            "Locally: set them in a .env file. "
            "On GitHub Actions: set them as repository secrets."
        )

    return username, password


def send_email(to: str, subject: str, body: str) -> None:
    # ============================================================
    # Send a plain-text email.

    # Args:
    #     to: Recipient email address.
    #     subject: Email subject line.
    #     body: Plain-text body.

    # Raises:
    #     RuntimeError: if credentials are missing.
    #     smtplib.SMTPException: on delivery failure.
    # ============================================================
    
    username, password = _get_credentials()

    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()              # upgrade to encrypted connection
        server.login(username, password)
        server.send_message(msg)