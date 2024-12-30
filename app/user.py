import json
import os

FILE_PATH = "./users.json"


def login(username, password):
    # Verificar si el archivo JSON existe
    if os.path.exists(FILE_PATH):
        # Si el archivo existe, leer los datos
        with open(FILE_PATH, 'r') as file:
            users = json.load(file)

        # Verificar si el usuario existe y la contraseña es correcta
        if username in users and users[username] == password:
            print("Inicio de sesión exitoso")
        else:
            print("Usuario o contraseña incorrectos")
    else:
        # Si no existe el archivo, crearlo y agregar el usuario
        with open(FILE_PATH, 'w') as file:
            # Crear un diccionario con el nuevo usuario
            users = {username: password}
            json.dump(users, file)
        print(
            f"Usuario '{username}' creado exitosamente. Ahora puedes iniciar sesión.")

####################################################################################


def user_exists(username):
    # Verificar si el archivo JSON existe
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            users = json.load(file)

        # Buscar si el usuario existe en el archivo
        if username in users:
            return True
        else:
            return False
    else:
        return False
