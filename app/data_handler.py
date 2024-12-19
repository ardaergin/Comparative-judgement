import os
import csv

def setup_data_file(participant_id):
    # Create data directory if it doesn't exist
    if not os.path.isdir('data'):
        os.makedirs('data')

    # Ensure unique file name
    dataFileName = os.path.join('data', f"{participant_id}.csv")
    baseName, fileExt = os.path.splitext(dataFileName)
    count = 1
    while os.path.exists(dataFileName):
        dataFileName = f"{baseName}_{count}{fileExt}"
        count += 1

    data_file = open(dataFileName, 'w', newline='')
    writer = csv.writer(data_file)
    writer.writerow(['trial', 'left_image', 'right_image', 'response', 'rt'])

    return data_file, writer
