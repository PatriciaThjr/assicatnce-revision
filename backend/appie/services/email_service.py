import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List
from datetime import datetime

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
    
    def send_planning_notification(self, user_email: str, planning: List[dict]):
        subject = "🎯 Votre planning de révision est prêt !"
        
        next_session = planning[0] if planning else None
        
        html_content = f"""
        <html>
          <body>
            <h2>📚 Votre Planning de Révision</h2>
            <p>Bonjour,</p>
            <p>Votre planning de révision pour le semestre a été généré avec succès !</p>
            
            {self._format_next_session(next_session) if next_session else ""}
            
            <p>Connectez-vous à votre dashboard pour consulter le planning complet.</p>
            <br>
            <p>Cordialement,<br>L'équipe Assistant de Révisions</p>
          </body>
        </html>
        """
        
        self._send_email(user_email, subject, html_content)
    
    def _format_next_session(self, session: dict) -> str:
        session_date = datetime.fromisoformat(session['date']).strftime("%d/%m/%Y à %H:%M")
        
        return f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
          <h3>📖 Prochaine session :</h3>
          <p><strong>Module:</strong> {session['module_name']}</p>
          <p><strong>Date:</strong> {session_date}</p>
          <p><strong>Durée:</strong> {session['duration']} minutes</p>
          <p><strong>Priorité:</strong> {session['priority'].capitalize()}</p>
          <p><strong>Objectifs:</strong></p>
          <ul>
            {''.join([f'<li>{obj}</li>' for obj in session['objectives']])}
          </ul>
        </div>
        """
    
    def _send_email(self, recipient: str, subject: str, html_content: str):
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            print(f"Email envoyé à {recipient}")
            
        except Exception as e:
            print(f"Erreur envoi email: {e}")