import jwt
import time
import uuid
import csv
import pandas as pd
import qrcode
from io import BytesIO
import base64


# Geheimschlüssel für die Signatur
SECRET_KEY = "tCZZyiuphjunibB5ljKTPZSVw5vNzsDc"

# Funktion zum Generieren eines JWT
def generate_token(user_id):
    payload = {
        "sub": user_id,                     # Benutzer-ID
        "iat": int(time.time()),            # Ausstellungszeitpunkt
        "exp": int(time.time()) + 3000000,    
        "jti": str(uuid.uuid4()),           # Eindeutige Token-ID
        "scopes": ["read", "write"]         # Zugriffsrechte
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# 250 Tokens generieren
tokens = []
for i in range(350):
    user_id = f"user_{i + 1}"  # Beispiel-Benutzer-IDs
    token = generate_token(user_id)
    tokens.append({"user_id": user_id, "token": token})

# Tokens als CSV speichern
csv_file = "tokens.csv"
with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["user_id", "token"])
    writer.writeheader()
    writer.writerows(tokens)

print(f"350 Tokens wurden generiert und in '{csv_file}' gespeichert.")

df = pd.read_csv("/Users/melaniepospisil/CrowdCapital/TokensCards_exported_1.csv")

import qrcode
from PIL import Image

qr_codes = []

# Funktion, um QR-Codes zu generieren
# Funktion, um QR-Codes zu generieren
def generate_qr_code(token):
    url = f"http://crowdinvest.startmunich.de?token={token}"
    
    # QR-Code erstellen
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Bild mit gewünschter Farbe generieren
    img = qr.make_image(fill_color="#00002c", back_color="white")
    
    # QR-Code als Base64-String speichern
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_base64

# QR-Codes für jede Zeile generieren und in 'qr_code'-Spalte speichern
df["qr_code"] = df["token"].apply(generate_qr_code)
df.to_csv("/Users/melaniepospisil/CrowdCapital/TokensCards_exported_2.csv")
# Ergebnis anzeigen oder weiterverarbeiten
# import ace_tools as tools; tools.display_dataframe_to_user(name="Tokens mit QR-Codes", dataframe=df)
print("QR-Codes wurden erfolgreich generiert und im DataFrame gespeichert.")

