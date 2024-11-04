import mysql.connector

def get_selected_option():
    connection = mysql.connector.connect(
        host="localhost:3306",
        user="admin_user",
        password="root123",
        database="mydb"
    )

    cursor = connection.cursor()
    query = "SELECT * FROM web_server_securityoptions"
    cursor.execute(query)
    options = cursor.fetchall()
    selected_option = None
    for option in options:
        print(option)
        if option.is_selected:
            selected_option = option.option_code
            break

    cursor.close()
    connection.close()
    return selected_option
