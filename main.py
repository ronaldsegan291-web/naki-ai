import os
import random
import requests
import threading
from datetime import datetime

# Kivy Framework Imports
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

# Optional Plyer Import for Android Integration
try:
    from plyer import notification
except ImportError:
    notification = None


# ==========================================
# CUSTOM UI WIDGET CLASSES FOR PREMIUM DESIGN
# ==========================================
class ModernTextInput(TextInput):
    """Sleek, heavily padded dark input area with rounded borders."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0.1, 0.14, 0.22, 1)  # Premium Dark Navy (#1A2238)
        self.foreground_color = (0.95, 0.96, 0.98, 1)
        self.cursor_color = (0.0, 0.9, 1.0, 1)        # Cyan Accent
        self.hint_text_color = (0.5, 0.55, 0.65, 1)
        self.padding = [15, 12, 15, 12]
        self.font_name = 'Roboto' if os.path.exists('Roboto') else 'sans-serif'


class ModernButton(Button):
    """Flat modern button with smooth dynamic hover states and text handling."""
    def __init__(self, bg_color=(0.0, 0.7, 0.8, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # Drawn manually
        self.custom_bg = bg_color
        self.bold = True
        self.color = (1, 1, 1, 1)
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.custom_bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[8])


# ==========================================
# PART 5: AUTHENTICATION MODULE
# ==========================================
class NAKI_Auth:
    def __init__(self):
        self.current_user = None
        self.otp_db = {}  # Format: {phone: otp}

    def send_otp(self, phone):
        phone = phone.strip()
        if not (phone.startswith("07") and len(phone) == 10):
            return "Namba eno si nnungi. Ssaamu namba entuufu."
        
        otp = str(random.randint(1000, 9999))
        self.otp_db[phone] = otp
        print(f"SMS TO {phone}: NAKI OTP yo ye {otp}")
        return f"OTP esindikiddwa ku {phone}"

    def verify_otp(self, phone, otp_input):
        phone = phone.strip()
        otp_input = otp_input.strip()
        if self.otp_db.get(phone) == otp_input:
            self.current_user = phone
            return f"Welcome {phone}! Yingira NAKI AI"
        return "OTP ensobi, gezaako nate."

    def is_logged_in(self):
        return self.current_user is not None

    def get_user_phone(self):
        return self.current_user


# ==========================================
# PART 4: PREMIUM & MONETIZATION MANAGEMENT
# ==========================================
class NAKI_Premium:
    def __init__(self):
        self.is_gold = False
        self.is_platinum = False
        self.chat_count = 0
        self.mtn_number = "0768559022"
        self.airtel_number = "0757343236"

    def check_premium(self, feature):
        if feature == "chat" and self.chat_count >= 10 and not self.is_gold and not self.is_platinum:
            return False, "Gold 15k needed"
        if feature == "image" and self.chat_count >= 1 and not self.is_gold and not self.is_platinum:
            return False, "Gold 15k needed"
            
        if feature == "video" and not self.is_platinum:
            return False, "Platinum 30k for videos"
        if feature in ["advert", "branding", "guardian"] and not self.is_platinum:
            return False, "Platinum 30k for advert & branding"
            
        return True, "Allowed"

    def verify_payment(self, tx_id):
        tx_id = tx_id.strip()
        if "15k" in tx_id.lower():
            self.is_gold = True
            return "🎉 Gold Subscription Activated!"
        elif "30k" in tx_id.lower():
            self.is_platinum = True
            return "👑 Platinum Suite Activated!"
        return "⚠️ Wabadewo ensobi mu TxID. Gezaako nate."


# ==========================================
# PART 1 & 2: CORE BRAIN & CREATOR MULTIMEDIA
# ==========================================
class NAKI_Brain:
    def __init__(self):
        self.SUNBIRD_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSb2JlcnQiLCJhY2NvdW50X3R5cGUiOiJGcmVlIiwidHYiOjEsImV4cCI6NDk0NDE0MTY2NH0.LoiIKvVXnPEa1qOKDaIzCzoz8AGwJPeTHV6YVW2n5ME"
        self.SUNBIRD_BASE_URL = "https://sunbird.ai"
        self.GROQ_API_KEY = "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"

    def think(self, user_text):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.GROQ_API_KEY}"}
        prompt = f"You are NAKI AI, a sweet 24years Ugandan girl, 95% Luganda. Answer: {user_text}"
        
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            r = requests.post(url, headers=headers, json=data, timeout=12)
            if r.status_code == 200:
                return r.json()["choices"]["message"]["content"]
            return "Kati nze nfunye obuzibu muli. (Error communicating with AI Brain Server)"
        except Exception as e:
            return f"Failure connecting to brain network: {str(e)}"

    def speak_luganda(self, text):
        tts_url = f"{self.SUNBIRD_BASE_URL}/tasks/audio/speech"
        headers = {
            "Authorization": f"Bearer {self.SUNBIRD_API_TOKEN}",
            "Content-Type": "application/json"
        }
        tts_payload = {
            "text": text,
            "voice": "salt_lug_0001",
            "language": "lug",
            "response_mode": "url"
        }
        try:
            tts_response = requests.post(tts_url, headers=headers, json=tts_payload, timeout=15)
            if tts_response.status_code == 200:
                audio_url = tts_response.json().get("url")
                audio_data = requests.get(audio_url).content
                output_path = "/sdcard/naki.mp3"
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                os.system(f"mpv {output_path}")
            else:
                print("Failed synthesizing local voice system stream.")
        except Exception as e:
            print(f"TTS Engine Failure Exception: {e}")


class NAKI_Creator:
    def __init__(self, brain_instance):
        self.brain = brain_instance

    def luganda_to_english(self, luganda_text):
        return self.brain.think(f"Translate Luganda to English: {luganda_text}")

    def generate_image(self, luganda_prompt):
        english = self.luganda_to_english(luganda_prompt)
        url = f"https://pollinations.ai{english}?width=512&height=512"
        return url

    def generate_video(self, luganda_prompt):
        english = self.luganda_to_english(luganda_prompt)
        return f"https://pollinations.ai{english}"

    def image_to_video(self, image_path):
        return self.generate_video(f"animate this image {image_path} smiling, blinking")

    def make_cartoon(self, luganda_prompt):
        return self.generate_image(f"cartoon style: {luganda_prompt}")

    def make_advert(self, product_image_path, business_name):
        return f"ADVERT for {business_name} from {product_image_path}"

    def make_branding(self, product_image_path):
        return f"BRANDING logo and colors for {product_image_path}"


# ==========================================
# PART 3: HARDWARE ACTION CONTROL INTERFACE
# ==========================================
class NAKI_Action:
    def __init__(self, creator_instance):
        self.creator = creator_instance

    def process_command(self, text):
        text = text.lower()
        
        if "gulawo" in text or "open" in text:
            app = text.replace("gulawo", "").replace("open", "").strip()
            return self.open_app(app)
            
        if "kubila" in text or "call" in text:
            name = text.replace("kubila", "").replace("call", "").strip()
            return f"Opening call logs to dial {name}..."
            
        if "yimba" in text or "play" in text:
            return "Sings + Playing localized music request..."
            
        if "weather" in text or "obudde" in text:
            return "Obudde mu Kampala bwa kyakayaze (Weather is warm and clear)."
            
        if "health" in text or "obulamu" in text:
            return "Checking health vitals tracker..."
            
        if "business" in text or "enteekateeka" in text:
            return "Entrepreneur advice: Tandika n'akatono kolina okulaakulana."
            
        if "light" in text or "ettaala" in text:
            return "Connecting with Smart Home Samsung/Hisense hub... Lights adjusted."
            
        if "help" in text or "emergency" in text:
            return self.guardian_mode()
            
        return None

    def open_app(self, app_name):
        import webbrowser
        if "youtube" in app_name:
            webbrowser.open("https://youtube.com")
            return "Gulawo YouTube done"
        if "whatsapp" in app_name:
            webbrowser.open("https://wa.me")
            return "Gulawo WhatsApp done"
        return f"Could not open {app_name} automatically."

    def guardian_mode(self):
        if notification:
            notification.notify(title="NAKI Guardian Alert", message="Calling emergency support configuration!")
        return "NAKI Guardian: I remember your family, calling for help!"


# ==========================================
# KIVY MOBILE APP UI SCREENS WITH PREMIUM DESIGN
