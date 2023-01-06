from fastapi import APIRouter
from typing import Optional, List
from sqlmodel import Session, select
from myapi.db import engine

from myapi.app import (
    create_usuario,
    ingresar_usuario,
    create_rifa,
    mostrar_rifas,
    mostrar_numeros,
    mostrar_premios,
    eliminar_usuario,
    cerrar_rifa,
    sortear_rifa,
    modificar_nombre_usuario,
    modificar_clave_usuario,
    agregar_saldo_usuario,
    comprar_numeros,
    mostrar_usuarios,
    compra_individual,
)

from myapi.models import (
    Usuario,
    UsuarioCreate,
    UsuarioRead,
    RifasCreate,
    RifaNums,
    RifasLista,
)

router = APIRouter()


@router.post("/Nuevo-Usuario/", response_model=UsuarioCreate)
async def crear_usu(usu_c: UsuarioCreate):
    
    usu_c = create_usuario(usu=usu_c)
    return usu_c


@router.get("/Ingresar-Usuario/", response_model=UsuarioRead)
async def ingre_usu(nombre: str, clave: str):
    
    usu_c = ingresar_usuario(usu_nombre=nombre, usu_clave=clave)
    return usu_c


@router.patch("/Modificar-Usuario/{id}", response_model=str)
async def update_usuario(id: int, nombre: Optional[str] = None, clave: Optional[str] = None):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == id)
        resultado = session.exec(seleccion)
        usuario = resultado.first()
    
    if usuario == None:
        return "message: INGRESE UN ID DE USUARIO"
    if nombre == None:
        if clave == None:
            return "message: NO HAY CAMBIOS"
        else:
            return "message: NUEVA CLAVE --> " + modificar_clave_usuario(clave, id)
    if clave == None:
        return "message: NUEVO NOMBRE --> " + modificar_nombre_usuario(nombre, id)
    else:
        return "message: NUEVO NOMBRE --> " + modificar_nombre_usuario(nombre, id) + "    NUEVA CLAVE --> " + modificar_clave_usuario(clave, id)


@router.delete("/Deshabilitar-Usuario/{id}", response_model=str)
async def delete_usuario(id: int):
    
    eliminado = eliminar_usuario(id)
    return eliminado


@router.get("/Todos-los-Usuarios/", response_model=List[UsuarioRead])
async def show_usuarios():
    
    usuarios = List[UsuarioRead]
    usuarios = mostrar_usuarios()
    return usuarios


@router.post("/Crear-Rifa/", response_model=RifasCreate)
async def crear_rif(rifa_c: RifasCreate):
    
    rifa_c = create_rifa(rifa_c)
    return rifa_c


@router.get("/Todas-las-Rifas/", response_model=List[RifasLista])
async def show_rif():
    rifass: List[RifasLista]
    rifass = mostrar_rifas()
    return rifass


@router.get("/Numeros-de-Rifa/{rifa_id}", response_model=List[RifaNums])
async def num_rif(rif_id: int):
    
    numeross: List[RifaNums]
    numeross = mostrar_numeros(rif_id)
    return numeross


@router.get("/Ver-Premios-Rifa/{rifa_id}", response_model=list)
async def premios_rif(rifa_id: int):
    
    return mostrar_premios(rifa_id)



@router.post("/Sortear-la-Rifa/", response_model=list)
async def sort_rif(id: int):
    sorteo = sortear_rifa(id)
    return sorteo


@router.post("/Agregar-Saldo/", response_model=str)
async def saldo(id: int, saldo: int):
    agregado = agregar_saldo_usuario(id, saldo)
    return "Ahora tiene un saldo de " + agregado


@router.post("/Comprar-Numero/", response_model=list)
async def buy_numero(id_rifa: int, nombre: str, numero: int):
    comprados = compra_individual(id_rifa, nombre, numero)
    cerrar_rifa(id_rifa)
    return comprados


@router.post("/Comprar-Multiples-Numeros/", response_model=list)
async def buy_numeros(id_rifa: int, nombre: str, cantidad_comprar: int):
    comprados = comprar_numeros(id_rifa, nombre, cantidad_comprar)
    cerrar_rifa(id_rifa)
    return comprados


    

