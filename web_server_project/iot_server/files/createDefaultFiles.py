import os

def create_certificates_conf_file():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Full path to the file
    file_path = os.path.join(home_dir, "certificates.conf")

    # Check if the file exists
    if not os.path.exists(file_path):
        # Content to add to the file
        file_content = """#ca_certs=path_to_authority_certificate
        #certfile=path_to_device_certificate
        #keyfile=path_to_device_key"""

        # Create the file and write the content
        with open(file_path, 'w') as file:
            file.write(file_content)

        print(f"File created at {file_path}")
    else:
        print(f"File already exists at {file_path}")


# Usage example
create_certificates_conf_file('cert_config.txt')