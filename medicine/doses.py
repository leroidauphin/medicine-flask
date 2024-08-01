from datetime import datetime, timedelta
import pandas as pd

from medicine.config import doses_file_path



def add(people_id, medicine_id):
    doses = pd.read_csv(doses_file_path)
    new_row = pd.DataFrame(
        {
            "people_id": [people_id],
            "medicines_id": [medicine_id],
            "dose_datetime": [datetime.now()],
        }
    )
    new_doses = pd.concat([doses, new_row])
    new_doses.to_csv(doses_file_path, index=False)


def doses_last_24hrs():
    doses = pd.read_csv(doses_file_path, parse_dates=["dose_datetime"])
    start_timestamp = datetime.now() - timedelta(hours=24)
    rows_last_24hrs = doses[doses["dose_datetime"] > start_timestamp]
    return rows_last_24hrs
