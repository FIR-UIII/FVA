import os

def clean_upload_directory():
    directory = "upload"
    files_in_directory = os.listdir(directory)

    # Filter
    files_to_delete = [file for file in files_in_directory if not file.startswith(".")] #<-- vulnerability allow persistance for file that start with '.'

    for file in files_to_delete:
        path_to_file = os.path.join(directory, file)
        if os.path.exists(path_to_file):
            try:
                os.remove(path_to_file)
                print(f"Deleted {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")