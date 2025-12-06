import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# --- Load CSV ---
df = pd.read_csv("google_maps_leads_full.csv")

# --- Replace NaN with empty string ---
df = df.fillna("")

# --- Google Sheets authentication ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(
    "logical-air-480404-n1-8b84ade11508.json",
    scopes=SCOPES
)
client = gspread.authorize(creds)

# --- Open the sheet ---
spreadsheet_id = "1v9l_K1AazFBHG6XbwxMXS9UmV11Wc1-T-n6wSmpyDuM"
sheet = client.open_by_key(spreadsheet_id).sheet1

# --- Upload CSV data ---
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("Uploaded to Google Sheets successfully!")
