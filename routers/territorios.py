from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

class MapaUpdate(BaseModel):
    territorio: str
    mapa: str
    fecha: Optional[str] = None
    hecho: str
    username: str

@router.put("/updateMapa")
async def update_mapa(data: MapaUpdate):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT fecha, hecho FROM mapas WHERE territorio = %s AND mapa = %s", (data.territorio, data.mapa))
    resultado = cursor.fetchone()

    if not resultado:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    if data.hecho == "sí":
        if resultado["fecha"] and resultado["hecho"] == "sí":
            cursor.close()
            connection.close()
            return {"message": "La manzana ya está hecha"}
        else:
            cursor.execute("UPDATE mapas SET username = %s, fecha = %s, hecho = %s WHERE territorio = %s AND mapa = %s",
                           (data.username, fecha_actual, "sí", data.territorio, data.mapa))
    
    elif data.hecho == "falta":
        if resultado["hecho"] == "falta":
            cursor.close()
            connection.close()
            return {"message": "La manzana ya estaba incompleta"}
        else:
            cursor.execute("UPDATE mapas SET username = %s, fecha = %s, hecho = %s WHERE territorio = %s AND mapa = %s",
                           (data.username, fecha_actual, "falta", data.territorio, data.mapa))
    
    elif data.hecho == "no":
        if resultado["hecho"] == "no":
            cursor.close()
            connection.close()
            return {"message": "La manzana ya estaba no realizada"}
        else:
            cursor.execute("UPDATE mapas SET username = %s, fecha = %s, hecho = %s WHERE territorio = %s AND mapa = %s",
                       ("LuisCastañeda", None, "no", data.territorio, data.mapa))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Estado actualizado correctamente"}


@router.get("/getTerritorios")
async def get_territorios():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT territorios FROM territorios")
    territorios = [row[0] for row in cursor.fetchall()]  
    
    cursor.close()
    connection.close()
    
    return {"territorios": territorios}



@router.get("/getTerritoriosCapitan")
async def get_territorios():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT territorios FROM territorios WHERE Vista = 'TRUE'")
    territorios = [row[0] for row in cursor.fetchall()]  
    
    cursor.close()
    connection.close()
    
    return {"territorios": territorios}

@router.put("/updateTerritorioVista")
async def update_territorio_vista(nombre: str, vista: bool):
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("UPDATE territorios SET Vista = %s WHERE territorios = %s", (str(vista).upper(), nombre))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return {"message": "Territorio actualizado correctamente"}

class Territorio(BaseModel):
    nombre: str

@router.post("/createTerritorio")
async def createTerritorio(territorio: Territorio):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM territorios WHERE territorios = %s", (territorio.nombre,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="El territorio ya existe.")

        cursor.execute("INSERT INTO territorios (territorios, Vista) VALUES (%s, %s)", 
                       (territorio.nombre, "TRUE"))
        
        cursor.executemany(
            "INSERT INTO mapas (territorio, mapa, fecha, username, grupo, hecho) VALUES (%s, %s, %s, %s, %s, %s)", 
            [(territorio.nombre, "MSalon", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MChacon", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MLaBotella", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFCarvajal", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFMaldonado", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFrenteSalon", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFPolanco", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFVargas", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MTiendaLaPoderosa", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFCriales", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFEcheverria", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MHIslanda", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFCastro", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MFSantiagoChacon", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MIslita", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MBicicletasBikebar", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MTiendaSureña", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MCasaCarnaval", None, "LuisCastañeda", 1, "no"),
             (territorio.nombre, "MSede", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MColegioCorazonSantuario", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFCantillo", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFCera", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MMiselaneaEdgar", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFNuma", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFCastañeda", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MHJulia", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MParquecito", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MTiendaDiosConNosotros", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MTiendaMiAngelDeAmor", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MLos6Hermanos", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MHKelly", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFMartinez", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MAlFrenteFMartinez", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MTiendaMerkanubar", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MAlLadoParqueAbandonado", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MAlLadoTiendaPrecioEsCorrecto", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MParqueGoldaMeir", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MAlLadoFCoronado", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFCoronado", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MParqueAbandonado", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFrenteFSuarez", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFarmaciaJyH", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MTiendaPrecioEsCorrecto", None, "LuisCastañeda", 2, "no"),
             (territorio.nombre, "MFPerezSegura", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MFPerezCarvajal", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTiendaLaRenovacion", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MPanaderiaElLider", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MLosGallos", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MMuebleriaLuxuryHouse", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTiendaLaFeEnDios", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MVariedadesFenicia", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTiendaElBacan", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MEstaderoLaRetoba", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTallerCarlos", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MSeñoraLevix", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MHFrancelina", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTiendaElEden", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTiendaDondeTotto", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTiendaNuevoRenacer", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MAlLadoDondeTotto", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MFSuarez", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MLasPiedras", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MLaIslita3", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MFrenteFTapia", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MFTapia", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MTiendaRivero", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MLaBombonera", None, "LuisCastañeda", 3, "no"),
             (territorio.nombre, "MVariedadesSofy", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MBillaresLasPernicias", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MFrenteColegioLasAmericas", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MFCeren", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MColegioJesusDeNazareth", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MColegioAtanacioGirardot", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MPanaderiaEsquinaDelSabor", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MHEloina", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MHGloria2", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MHGloria", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MTiendaJJ", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MFrenteLaPanaderiaLaEsquinaDel", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MFTorregrosa", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MRestauranteChino", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MFerreteriaElAmigo", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MHBelen", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MAlLadoFundacionChildrenIntern", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MFundacionChildrenInternationa", None, "LuisCastañeda", 4, "no"),
             (territorio.nombre, "MIslitaDelBrazil", None, "LuisCastañeda", 4, "no")]
        )

        connection.commit()

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar: {str(e)}")

    finally:
        cursor.close()
        connection.close()

    return {"message": "Territorio añadido con éxito", "territorio": territorio.nombre, "Vista": True}

@router.get("/getVistaMapas")
async def getVistaMapas(territorio: str, grupo: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)  

    query = "SELECT mapa, hecho FROM mapas WHERE territorio = %s AND grupo = %s;"
    cursor.execute(query, (territorio, grupo))
    resultados = cursor.fetchall()  

    cursor.close()
    connection.close()


    response_data = {row["mapa"]: row["hecho"] for row in resultados}

    return response_data




@router.get("/getFechaMapa")
async def get_fecha_mapa(territorio: str, grupo: int, mapa: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT mapa, fecha, username FROM mapas 
        WHERE territorio = %s AND grupo = %s AND mapa = %s;
    """
    cursor.execute(query, (territorio, grupo, mapa))
    resultado = cursor.fetchone() 

    cursor.close()
    connection.close()

    if not resultado:
        return {"error": "No se encontró el mapa en la base de datos"}

    return resultado  


@router.put("/updateFechaMapa")
async def update_fecha_mapa(territorio: str, mapa: str, fecha: str = None):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE mapas 
        SET fecha = %s 
        WHERE territorio = %s AND mapa = %s;
    """
    cursor.execute(query, (fecha, territorio, mapa))
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Fecha actualizada correctamente", "mapa": mapa, "nueva_fecha": fecha}    

class TerritorioRequest(BaseModel):
    territorio: str


@router.get("/usuarios")
def obtener_usuarios():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT username, rol FROM users"
    cursor.execute(query)
    usuarios = cursor.fetchall()

    cursor.close()
    connection.close()

    return usuarios

@router.delete("/deleteTerritorio")
async def delete_territorio(data: TerritorioRequest):
    territorio = data.territorio 

    if not territorio:
        raise HTTPException(status_code=400, detail="El territorio es requerido.")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM territorios WHERE territorios = %s;", (territorio,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Territorio no encontrado")

    cursor.execute("DELETE FROM mapas WHERE territorio = %s;", (territorio,))
    
    cursor.execute("DELETE FROM territorios WHERE territorios = %s;", (territorio,))
    
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": f"Territorio {territorio} eliminado."}