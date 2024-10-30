def read_certificate_conf_file(file_path):
    """The paths of the SSL certificates and keys are needed to use SSL.
        It is unsafe to store this in the code, so they must be stored
        separately on the machine that will run the MQTT client.
        The MQTT client needs to be provided with the path to these files.
        Instead of using a standard path for each file, we use a standard path
        for the configuration file and the files can be stored wherever the user
        wishes. The format of the file should be
        key=path
        key=path
    """

    # Dictionary to store key-value pairs
    certs = {}

    # Open the file and read it line by line
    with open(file_path, 'r') as file:
        for line in file:
            # skip commented out lines
            if  line.startswith("#"):
                continue

            # Split the line by '=' to separate key and value
            key_value = line.strip().split('=')

            # Check if the line contains exactly two elements (key and value)
            if len(key_value) == 2:
                key, value = key_value
                # Store the key-value pair in the dictionary
                certs[key.strip()] = value.strip()
    return certs

def should_use_ssl(file_path):
    if len(file_path) == 0:
        return False
    
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith("#"):
                return True
        return False