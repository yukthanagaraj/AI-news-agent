import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

start = time.time()

print("Step 1: Loading credentials...")
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials/service_account.json", scope
)
print(f"  Done in {time.time() - start:.2f}s")

print("Step 2: Authorizing...")
t = time.time()
client = gspread.authorize(creds)
print(f"  Done in {time.time() - t:.2f}s")

print("Step 3: Opening spreadsheet...")
t = time.time()
sheet = client.open("AI News Blog Database").sheet1
print(f"  Done in {time.time() - t:.2f}s")

print("Step 4: Reading column C...")
t = time.time()
vals = sheet.col_values(3)
print(f"  Done in {time.time() - t:.2f}s")
print(f"  Got {len(vals)} values")

print(f"\nTotal time: {time.time() - start:.2f}s")
print("All steps completed successfully!")
