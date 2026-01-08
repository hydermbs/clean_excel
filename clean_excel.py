import pandas as pd
import re
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent

df = pd.read_csv(script_dir / 'data_for_clean_excel.csv')
df = df.dropna()
#clean Column

df.columns = df.columns.str.strip().str.title()

#Normalize Person and City name
df['Customer Name'] = df['Customer Name'].str.title()
df['City'] = df['City'].str.title()

#Validate Email:
def validate_email(email):
    if pd.isna(email):
        return "invalid"
    email = email.lower()
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return email if re.match(pattern,email) else "invalid"

df['Email'] = df['Email'].apply(validate_email)

#Validate Phone

def validate_phone(phone):
    if pd.isna(phone):
        return "invalid"
    digits = re.sub(r"\D","",phone)
    if digits.startswith("92"):
        digits = "0"+digits[2:]
    if len(digits)==11 and digits.startswith('03'):
        return digits
    else:
        return "invalid"

df['Phone'] = df['Phone'].apply(validate_phone)

df['Amount'] = pd.to_numeric(df['Amount'],errors='coerce').fillna(0).astype(int)

df['Date'] = pd.to_datetime(df['Date'],errors='coerce')

merged = df.groupby("Customer Name", as_index=False).agg({
        "Customer Name": "first",
        "Phone": "first",
        "Email":"first",
        "City": "last",
        "Amount": "sum",
        "Date": "max"
    })

merged = merged.sort_values("Amount", ascending=False)

merged.to_csv(script_dir / "Clean_final.csv")