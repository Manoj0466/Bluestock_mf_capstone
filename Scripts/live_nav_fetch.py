import requests
import pandas as pd

schemes = {
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_LargeCap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

for fund_name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    data = response.json()

    nav_data = data["data"]

    df = pd.DataFrame(nav_data)

    df.to_csv(
        f"Raw data/{fund_name}.csv",
        index=False
    )

    print(f"{fund_name} downloaded successfully")