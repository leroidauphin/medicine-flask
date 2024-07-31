import os

from dotenv import load_dotenv

# filenames
people_file_name = "people.csv"
medicines_file_name = "medicines.csv"
doses_file_name = "doses.csv"

load_dotenv()

# distinguish between local files and the app engine bucket
local_files_dir = os.environ.get("LOCAL_FILE_DIR")

files_dir = local_files_dir
if local_files_dir is None:
    project_name = os.environ.get("GOOGLE_CLOUD_PROJECT")
    files_dir = f"gs://{project_name}.appspot.com/"

people_file_path = os.path.join(files_dir, people_file_name)
medicines_file_path = os.path.join(files_dir, medicines_file_name)
doses_file_path = os.path.join(files_dir, doses_file_name)
