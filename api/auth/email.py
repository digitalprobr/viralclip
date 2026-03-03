"""
Email service: sends magic link emails via SMTP.
Supports Gmail App Password, Resend, or any SMTP server.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.logger import get_logger

logger = get_logger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
FROM_NAME = os.getenv("FROM_NAME", "ViralClip")


def send_magic_link_email(to_email: str, magic_link_url: str, purpose: str = "login") -> bool:
    """Send a magic link email for login or registration."""
    subject = "🔗 Sign in to ViralClip" if purpose == "login" else "🎉 Welcome to ViralClip!"
    action_text = "Sign In" if purpose == "login" else "Verify & Create Account"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0;padding:0;background-color:#0f1117;font-family:'Inter',system-ui,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0f1117;padding:40px 20px;">
            <tr>
                <td align="center">
                    <table width="480" cellpadding="0" cellspacing="0" style="background-color:#1a1d27;border-radius:16px;border:1px solid #2a2d37;overflow:hidden;">
                        <!-- Header -->
                        <tr>
                            <td style="padding:32px 32px 0;text-align:center;">
                                <div style="font-size:24px;font-weight:800;color:#f0f0f0;">
                                    ✂️ Viral<span style="color:#34d399;">Clip</span>
                                </div>
                            </td>
                        </tr>
                        <!-- Body -->
                        <tr>
                            <td style="padding:24px 32px;">
                                <h1 style="color:#f0f0f0;font-size:22px;font-weight:700;margin:0 0 12px;">
                                    {"Welcome aboard! 🎬" if purpose == "register" else "Sign in to your account"}
                                </h1>
                                <p style="color:#9ca3af;font-size:14px;line-height:1.6;margin:0 0 24px;">
                                    {"Click the button below to verify your email and create your ViralClip account. You'll receive 50 free credits to get started!" if purpose == "register" else "Click the button below to securely sign in to ViralClip. This link expires in 30 minutes."}
                                </p>
                                <!-- CTA Button -->
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td align="center">
                                            <a href="{magic_link_url}"
                                               style="display:inline-block;padding:14px 32px;background-color:#34d399;color:#0f1117;font-size:16px;font-weight:700;text-decoration:none;border-radius:12px;">
                                                {action_text} →
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                <p style="color:#6b7280;font-size:12px;margin:20px 0 0;text-align:center;">
                                    If you didn't request this, you can safely ignore this email.
                                </p>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="padding:16px 32px;border-top:1px solid #2a2d37;text-align:center;">
                                <p style="color:#4b5563;font-size:11px;margin:0;">
                                    © 2026 ViralClip — AI-Powered Video Clipping
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    if not SMTP_USER or not SMTP_PASSWORD:
        # Dev mode: log the link instead of sending email
        logger.warning(f"📧 SMTP not configured. Magic link for {to_email}: {magic_link_url}")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = to_email
        msg.attach(MIMEText(f"Sign in to ViralClip: {magic_link_url}", "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"✅ Magic link email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send email to {to_email}: {e}")
        return False
