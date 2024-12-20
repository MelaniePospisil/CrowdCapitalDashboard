import base64
import os
import pandas as pd

# Load the CSV file
df = pd.read_csv("path/to/your/csv/with/the/tokens.csv") #REPLACE!!

# Create a folder to store the QR code images
output_folder = "qr_codes"
os.makedirs(output_folder, exist_ok=True)

# Save each QR code as a PNG file
for index, row in df.iterrows():
    qr_code_data = row["qr_code"]
    user_id = row["user_id"]
    image_path = os.path.join(output_folder, f"{user_id}.png")
    
    with open(image_path, "wb") as img_file:
        img_file.write(base64.b64decode(qr_code_data))

print("QR code images saved in the 'qr_codes' folder.")