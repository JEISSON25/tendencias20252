import requests
import json
from django.conf import settings

class EmailApiService:
    BASE_URL = "https://smtp.maileroo.com/api/v2/emails"

    def __init__(self):
        self.api_key = settings.MAILEROO_API_KEY
        if not self.api_key:
            raise EnvironmentError("MAILEROO_API_KEY no está configurada.")

    def send_email(self, recipient_email: str, subject: str, html_content: str, attachments: list = None):
        """
        Interfaz genérica para enviar correos usando la API de Maileroo.

        :param recipient_email: Correo del destinatario.
        :param subject: Asunto del correo.
        :param html_content: Contenido del correo en formato HTML.
        :param attachments: Lista de diccionarios de adjuntos (opcional).
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # La API de Maileroo requiere el 'to' como lista de objetos
        payload = {
            "from": {
                "address": settings.MAILEROO_FROM_EMAIL,
                "display_name": "Reservas Inteligentes"
            },
            "to": [
                {"address": recipient_email}
            ],
            "subject": subject,
            "html": html_content,
            "attachments": attachments if attachments else []
        }

        try:
            response = requests.post(self.BASE_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            
            return response.json() 
            
        except requests.exceptions.HTTPError as errh:
            print(f"Error HTTP al enviar correo: {errh}")
            print(f"Respuesta de la API: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión al enviar correo: {e}")
            return None