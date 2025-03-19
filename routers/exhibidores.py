from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

class Exhibidor(BaseModel):
    nombre: str
    username: str
    fecha: datetime

@router.post("/addregistro")
async def addregistro(exhibidor: Exhibidor):
    connection = get_connection()
    cursor = connection.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    try:
        cursor.execute("INSERT INTO exhibidores (nombre, username, fecha) VALUES (%s, %s, %s)", 
                       (exhibidor.nombre, exhibidor.username, exhibidor.fecha))
        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar: {str(e)}")

    finally:
        cursor.close()
        connection.close()

    return {"message": "Registro de exhibidor añadido con exito"}    

@router.get("/exhibidores/")
def obtener_exhibidores(nombre: str, año: int, mes: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    fecha_inicio = f"{año}-{mes:02d}-01"
    if mes == 12:
        fecha_fin = f"{año}-12-31"
    else:
        fecha_fin = f"{año}-{mes+1:02d}-01"

    cursor.execute(
        "SELECT * FROM exhibidores WHERE nombre = %s AND fecha >= %s AND fecha < %s",
        (nombre, fecha_inicio, fecha_fin)
    )
    exhibidores = cursor.fetchall()

    cursor.close()
    connection.close()

    if not exhibidores:
        raise HTTPException(status_code=404, detail="No se encontraron exhibidores con esos datos")

    return {"exhibidores": exhibidores}

@router.get("/exhibidores/lista")
def obtener_lista_exhibidores(nombre: str, año: str, mes: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    fecha_like = f"{año}-{mes}%"

    cursor.execute("SELECT nombre, fecha, username FROM exhibidores WHERE nombre = %s AND fecha LIKE %s", (nombre, fecha_like))
    exhibidores = cursor.fetchall()

    cursor.close()
    connection.close()

    if not exhibidores:
        raise HTTPException(status_code=404, detail="No se encontraron exhibidores para la fecha y nombre especificados.")

    return {"exhibidores": exhibidores}
@router.get("/exhibidores/uso")
def contar_uso_exhibidor(nombre: str, año: str, mes: str):
    connection = get_connection()
    cursor = connection.cursor()

    fecha_like = f"{año}-{mes}%"

    cursor.execute("SELECT COUNT(*) FROM exhibidores WHERE nombre = %s AND fecha LIKE %s", (nombre, fecha_like))
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {"nombre": nombre, "mes": f"{año}-{mes}", "uso": count}


@router.delete("/exhibidores/eliminar")
def eliminar_exhibidor(nombre: str, fecha: str, username: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM exhibidores WHERE nombre = %s AND fecha = %s AND username = %s",
        (nombre, fecha, username)
    )
    exhibidor = cursor.fetchone()

    if not exhibidor:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Exhibidor no encontrado")

    cursor.execute(
        "DELETE FROM exhibidores WHERE nombre = %s AND fecha = %s AND username = %s",
        (nombre, fecha, username)
    )
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": f"Exhibidor {nombre} con fecha {fecha} y username {username} eliminado correctamente"}
