import mariadb


def get_selected_option():
    con_params = {
        "host" : "127.0.0.1",
        "user" :"admin_user",
        "password" : "root123",
        "database" : "mydb",
        "port" : 3306
    }
    
    connection = mariadb.connect(**con_params)

    cursor = connection.cursor()
    query = "SELECT option_code FROM web_server_securityoptions where is_selected=true"
    cursor.execute(query)
    option = cursor.fetchone()
    if option is None:
        return None
    cursor.close()
    connection.close()
    return option
