from typing import Optional
from sqlmodel import Field, Session, SQLModel
from myapi.db import engine



class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    clave: str
    saldo: int
    recargas: Optional[str] = Field(default=None) 
    mis_premios: Optional[str] = Field(default=None)


class UsuarioCreate(SQLModel):
    c_nombre: str
    c_clave: str


class UsuarioRead(SQLModel):
    id: Optional[int] = Field(default=0)
    nombre: Optional[str] = Field(default="NULO")
    clave: Optional[str] = Field(default="NULO")
    saldo: Optional[int] = Field(default=0)
    recargas: Optional[str] = Field(default="0")
    mis_premios: Optional[str] = Field(default="Ninguno")






class Rifas(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(index=True, foreign_key="usuario.id")  #este es el id del usuario propietario de la rifa
    estado: str = Field(default="Abierta")
    cantidad: int
    precio: int 
    premios: Optional[str] = Field(default=None)
    numero: Optional[str] = Field(default=None)
    estado_numero: Optional[str] = Field(default=None)


class RifasCreate(SQLModel):
    id_usu: int
    cantidad: int
    precio: int
    premios: str


class RifaNums(SQLModel):
    numero: str
    estado_numero: str

class RifasLista(SQLModel):
    id: int
    estado: str
    cantidad: int
    precio: int
    premios: str






