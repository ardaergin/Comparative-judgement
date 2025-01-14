import os
import csv

def setup_data_file(participant_id):
    """
    Set up the data file for saving participant responses.
    The participant_id includes a timestamp to ensure unique filenames.

    Parameters:
        participant_id: The unique participant identifier with timestamp.

    Returns:
        data_file: The file object for writing data.
        writer: The CSV writer object.
    """
    # Create data directory if it doesn't exist
    if not os.path.isdir('data'):
        os.makedirs('data')

    # Ensure unique file name (though timestamp usually suffices)
    dataFileName = os.path.join('data', f"{participant_id}.csv")
    baseName, fileExt = os.path.splitext(dataFileName)
    count = 1
    while os.path.exists(dataFileName):
        dataFileName = f"{baseName}_{count}{fileExt}"
        count += 1

    data_file = open(dataFileName, 'w', newline='')
    writer = csv.writer(data_file)
    writer.writerow(['trial', 'round_type', 'left_image', 'right_image', 'response', 'rt'])

    return data_file, writer
