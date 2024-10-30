import os

# Get the user's home directory
home_dir = os.path.expanduser("~")

# Full path to the directoryd
dir_path = os.path.join(home_dir, "iot_secure")

# Create the directory if it doesn't exist
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    print(f"Directory created at {dir_path}")

# Full path to the file
file_path = os.path.join(dir_path, "certificates.conf")

# Check if the file exists
if not os.path.exists(file_path):
    # Content to add to the file
    file_content = """#ca_certs=path_to_authority_certificate\n#certfile=path_to_device_certificate\n#keyfile=path_to_device_key\n#password=private_key_encryption_password"""

    # Create the file and write the content
    with open(file_path, 'w') as file:
        file.write(file_content)

    print(f"File created at {file_path}")
else:
    print(f"File already exists at {file_path}")
