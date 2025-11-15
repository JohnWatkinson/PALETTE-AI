import resend
from typing import Dict, List
from pathlib import Path
from jinja2 import Template
from .config import settings
from .schemas import PaletteResult

# Configure Resend
if settings.RESEND_API_KEY:
    resend.api_key = settings.RESEND_API_KEY


class EmailService:
    """Handles sending palette results via Resend"""

    def __init__(self):
        self.from_email = settings.FROM_EMAIL
        self.template_dir = Path(__file__).parent.parent / "email_templates"

    def send_palette_email(self, to_email: str, palette: PaletteResult) -> bool:
        """
        Send personalized color palette email

        Args:
            to_email: Recipient email address
            palette: PaletteResult object with season and colors

        Returns:
            True if sent successfully, False otherwise
        """

        if not settings.RESEND_API_KEY:
            print("⚠️  No RESEND_API_KEY configured - skipping email")
            return False

        try:
            # Load and render email template
            html_content = self._render_template(palette)

            # Send email via Resend
            params = {
                "from": self.from_email,
                "to": [to_email],
                "subject": f"Your Color Season: {palette.season_display_name}",
                "html": html_content,
            }

            response = resend.Emails.send(params)

            print(f"✅ Email sent to {to_email} - ID: {response.get('id')}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False

    def _render_template(self, palette: PaletteResult) -> str:
        """Render HTML email template with palette data"""

        template_path = self.template_dir / "palette-result.html"

        with open(template_path, "r") as f:
            template = Template(f.read())

        return template.render(
            season=palette.season,
            season_name=palette.season_display_name,
            confidence=palette.confidence,
            undertone=palette.undertone,
            value=palette.value,
            chroma=palette.chroma,
            core_neutrals=palette.core_neutrals,
            accent_colors=palette.accent_colors,
            avoid_colors=palette.avoid_colors,
            explanation=palette.explanation
        )


# Global instance
email_service = EmailService()
