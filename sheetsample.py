import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("logical-air-480404-n1-6a232b0e8c7b.json", scopes=SCOPES)
client = gspread.authorize(creds)

# List all sheets the service account can see
for s in client.openall():
    print(s.title)