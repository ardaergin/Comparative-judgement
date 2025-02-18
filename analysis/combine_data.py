import json
import glob
import os
import pandas as pd

def main():
    folder_path = "data" # Path to the folder containing the JSON files
    json_files = glob.glob(os.path.join(folder_path, "*.json"))

    # List to collect each trial as a separate row
    rows = []

    for file in json_files:
        with open(file, "r") as f:
            data = json.load(f)
            
            # Participant basic info
            participant_id = data.get("participant_id")
            start_time = data.get("start_time")
            end_time = data.get("end_time")
            duration = data.get("duration")

            # Participant demographics
            demographics = data.get("demographics", {})
            gender = demographics.get("gender")
            age = demographics.get("age")
            nationality = demographics.get("nationality")
            diet = demographics.get("diet")
            eat_frequency = demographics.get("eat_frequency")

            # Loop over all trials in the file
            for trial in data.get("trials", []):
                row = {
                    # Participant ID
                    "participant_id": participant_id,

                    # Trial-specific info
                    "trial_num": trial.get("trial_num"),
                    "round_type": trial.get("round_type"),
                    "left_stimulus": trial.get("left_stimulus"),
                    "right_stimulus": trial.get("right_stimulus"),
                    "comparison_order": trial.get("comparison_order"),
                    "response": trial.get("response"),

                    # Paricipant-level info
                    "reaction_time": trial.get("reaction_time"),
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": duration,
                    "gender": gender,
                    "age": age,
                    "nationality": nationality,
                    "diet": diet,
                    "eat_frequency": eat_frequency,
                }
                rows.append(row)

    # Create the DataFrame
    df = pd.DataFrame(rows)

    # Ensure the 'working' folder exists under the 'data' folder
    os.makedirs("data/working", exist_ok=True)

    # Save the resulting DataFrame to a CSV file
    df.to_csv("data/working/combined_data.csv", index=False)

    # Display the resulting DataFrame
    print(df.head())

if __name__ == "__main__":
    main()
