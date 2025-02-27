"""Parser module to parse gear config.json."""

from typing import Tuple
import os
import re
from flywheel_gear_toolkit import GearToolkitContext

def parse_config(context):
    """Parse the config and other options from the context, both gear and app options.

    Returns:
        gear_inputs
        gear_options: options for the gear
        app_options: options to pass to the app
    """

    # Extract tags from the destination analysis container
    tags = context.destination.get("tags", [])

    # Check if 'gpu' is in the list of tags
    if "gpu" in tags:
        print("GPU processing enabled.")
        model = 'gambas'
    else:
        print("GPU processing not requested.")
        model = 'SR'

    # Get the input file id
    input_container = context.client.get_analysis(context.destination["id"])

    # Get the subject id from the session id
    # & extract the subject container
    subject_id = input_container.parents['subject']
    subject_container = context.client.get(subject_id)
    subject = subject_container.reload()
    print("subject label: ", subject.label)
    subject_label = subject.label

    # Get the session id from the input file id
    # & extract the session container
    session_id = input_container.parents['session']
    session_container = context.client.get(session_id)
    session = session_container.reload()
    session_label = session.label
    session_label = session_label.replace(" ", "_")
    print("session label: ", session.label)

    # Specify the directory you want to list files from
    directory_path = '/flywheel/v0/input/input'

    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            filename_without_extension = filename.split('.')[0]  # Remove extension
            no_white_spaces = filename_without_extension.replace(" ", "")
            
            # Replace non-alphanumeric characters with underscores
            cleaned_string = re.sub(r'[^a-zA-Z0-9]', '_', no_white_spaces)
            input_label = cleaned_string.rstrip('_')  # Remove trailing underscores
            
            # Remove leading numbers and any remaining leading underscores
            input_label = re.sub(r'^\d+_?', '', input_label)

            print("Input label:", input_label)

    output_label = 'sub-' + subject_label + '_ses-' + session_label + '_acq-' + input_label + '_rec-' + model +'.nii.gz'
    print("output_label:", output_label)
    
    return output_label