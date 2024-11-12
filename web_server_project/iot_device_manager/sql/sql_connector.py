import mariadb
from datetime import datetime

con_params = {
        "host" : "127.0.0.1",
        "user" :"admin_user",
        "password" : "root123",
        "database" : "mydb",
        "port" : 3306
    }

def get_selected_option():
    connection = mariadb.connect(**con_params)

    cursor = connection.cursor()
    query = "SELECT option_code FROM web_server_securityoptions where is_selected=true"
    cursor.execute(query)
    option = cursor.fetchone()
    if option is None:
        return None
    cursor.close()
    connection.close()
    return option[0]

def insert_measurement(device_name, value):
    connection = mariadb.connect(**con_params)
    cursor = connection.cursor()
    time = datetime.now()
    cursor.execute("INSERT INTO events (device_name, value, time) VALUES (%s, %s, %s)", (device_name, value, time))
    connection.commit()