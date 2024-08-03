from datetime import datetime, timedelta
from flask import Flask, redirect, render_template, request
import pandas as pd

from medicine.config import people_file_path, medicines_file_path
from medicine.doses import add, doses_last_24hrs

app = Flask(__name__)


def display_next_doses(people, medicines, doses):
    doses_with_persons = doses.merge(people, left_on="people_id", right_index=True)
    full_df = doses_with_persons.merge(medicines, left_on="medicines_id", right_index=True)
    summary = full_df.groupby(['people_id', 'medicines_id']).agg(['min', 'max', 'size'])
    display_df = full_df.drop(["people_id", "medicines_id"], axis=1)

    output_rows = list()
    for _, row in summary.iterrows():
        person_name = row["name_x"]["max"]
        medicine_name = row["name_y"]["max"]

        daily_doses_agg = row["max_per_24hrs"]
        if daily_doses_agg["size"] >= daily_doses_agg["max"]:
            next_dose = row["dose_datetime"]["min"]
        elif row["dose_datetime"]["max"] + timedelta(hours=4) >= datetime.now():
            next_dose = row["dose_datetime"]["max"] + timedelta(hours=4)

        output_rows.append(
            {
                "name": person_name,
                "med": medicine_name,
                "datetime": next_dose
            }
        )

    return output_rows


@app.route("/")
def root():
    people_df = pd.read_csv(people_file_path)
    medicines_df = pd.read_csv(medicines_file_path) 
    doses = doses_last_24hrs()
    output_rows = display_next_doses(people_df, medicines_df, doses)

    return render_template(
        "index.html", 
        people=people_df.to_dict(orient="records"), 
        medicines=medicines_df.to_dict(orient="records"), 
        doses=output_rows
    )


@app.route("/", methods=["POST"])
def doses():
    people_df = pd.read_csv(people_file_path)
    medicines_df = pd.read_csv(medicines_file_path) 

    people_name = request.form["Person"]
    medicine_name = request.form["Medicine"]

    person_id = people_df[people_df["name"] == people_name].index[0]
    medicine_id = medicines_df[medicines_df["name"] == medicine_name].index[0]
    add(person_id, medicine_id)

    return redirect(request.url)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
