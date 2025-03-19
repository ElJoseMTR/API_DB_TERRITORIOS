from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel

router = APIRouter()


@router.get("/users")
async def get_users():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return {"users": users}
    finally:
        cursor.close()
        connection.close()

@router.get("/openWeb/{username}/{password}")
async def get_users(username: str, password: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try: 
        query = "SELECT rol FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return{"status": "success", "role": user["rol"]}
        else:
            return{"status": "error", "message": "Usuario o Contraseña incorrectos"}
    finally:
        cursor.close()
        connection.close()    

@router.delete("/usuarios/{username}")
def eliminar_usuario(username: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    usuario = cursor.fetchone()
    if not usuario:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cursor.execute("SELECT * FROM mapas WHERE username = %s", (username,))
    mapas_usuario = cursor.fetchall()

    if mapas_usuario:
        cursor.execute("UPDATE mapas SET username = 'LuisCastañeda' WHERE username = %s", (username,))
        connection.commit()

    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": f"Usuario {username} eliminado correctamente"}

class RolUpdateRequest(BaseModel):
    nuevo_rol: str

@router.put("/usuariosupdaterole/{username}")
def editar_usuario(username: str, request: RolUpdateRequest):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cursor.execute("UPDATE users SET rol = %s WHERE username = %s", (request.nuevo_rol, username))
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": f"El rol de {username} ha sido actualizado a {request.nuevo_rol}"}

class PasswordUpdate(BaseModel):
    password: str

@router.put("/usuariosupdatepassword/{username}")
def actualizar_password(username: str, datos: PasswordUpdate):
    nueva_password = datos.password

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    usuario = cursor.fetchone()
    
    if not usuario:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (nueva_password, username))
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": f"Contraseña de {username} actualizada correctamente"}

class UserCreate(BaseModel):
    username: str
    password: str
    role: str


@router.post("/usuarioscreate/")
def crear_usuario(user: UserCreate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    usuario_existente = cursor.fetchone()

    if usuario_existente:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    cursor.execute("INSERT INTO users (username, password, rol) VALUES (%s, %s, %s)", 
                   (user.username, user.password, user.role))
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": f"Usuario {user.username} creado correctamente"}
