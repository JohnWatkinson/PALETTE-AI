import resend
from typing import Dict, List
from pathlib import Path
from jinja2 import Template
from premailer import transform
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
            # Load and render email templates
            html_content = self._render_template(palette)
            text_content = self._generate_text_version(palette)

            # Send email via Resend
            params = {
                "from": self.from_email,
                "to": [to_email],
                "subject": f"Your Color Season: {palette.season_display_name}",
                "html": html_content,
                "text": text_content,
            }

            response = resend.Emails.send(params)

            print(f"✅ Email sent to {to_email} - ID: {response.get('id')}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False

    def _render_template(self, palette: PaletteResult) -> str:
        """Render HTML email template with palette data and inline CSS"""

        template_path = self.template_dir / "palette-result.html"

        with open(template_path, "r") as f:
            template = Template(f.read())

        html_content = template.render(
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

        # Inline CSS for email client compatibility (Gmail, Outlook, etc.)
        inlined_html = transform(html_content)

        return inlined_html

    def _generate_text_version(self, palette: PaletteResult) -> str:
        """Generate plain text version of the email for accessibility"""

        text_parts = [
            "MAISON GUIDA",
            "Personal Color Analysis",
            "",
            f"YOUR COLOR SEASON: {palette.season_display_name.upper()}",
            f"Confidence: {palette.confidence}%",
            "",
            "YOUR CHARACTERISTICS",
            f"Undertone: {palette.undertone.capitalize()}",
            f"Value: {palette.value.capitalize()}",
            f"Chroma: {palette.chroma.capitalize()}",
            "",
            "CORE NEUTRALS",
        ]

        # Add core neutrals
        for color in palette.core_neutrals:
            text_parts.append(f"• {color.name} ({color.hex})")

        text_parts.extend(["", "ACCENT COLORS"])

        # Add accent colors
        for color in palette.accent_colors:
            text_parts.append(f"• {color.name} ({color.hex})")

        # Add colors to avoid
        if palette.avoid_colors:
            text_parts.extend(["", "COLORS TO AVOID", ", ".join(palette.avoid_colors)])

        text_parts.extend([
            "",
            "Shop your colors at https://maisonguida.com",
            "",
            "---",
            "This email was sent because you completed our color analysis questionnaire.",
            "Visit us at https://maisonguida.com"
        ])

        return "\n".join(text_parts)


# Global instance
email_service = EmailService()
