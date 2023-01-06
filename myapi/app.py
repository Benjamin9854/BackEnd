from typing import Optional, List
from sqlmodel import Session, select
from myapi.db import engine
import random


#IMPORTO LOS MODELOS
from myapi.models import (
    Usuario,
    UsuarioCreate,
    UsuarioRead,
    Rifas,
    RifasCreate,
    RifaNums,
    RifasLista,
)



#PARA LA CREACION DE UN NUEVO USUARIO
def create_usuario(usu: UsuarioCreate):
    usu_1 = Usuario(nombre=usu.c_nombre, clave=usu.c_clave, saldo=10000)

    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.nombre == usu_1.nombre)         #Esto es para ver si no hay un usuario con el mismo nombre
        resultado = session.exec(seleccion)
        usu = resultado.first()       #con esto se guarda, en "usuario", el primer registro encontrado

        if usu == None:
            session.add(usu_1)  #guarda el registro en la "session"
            session.commit()    #guarda los datos en la database
            session.refresh(usu_1)
            usu.c_nombre = usu_1.nombre
            usu.c_clave = usu_1.clave
            return usu




#PARA LA CREACCION DE UNA NUEVA RIFA
def create_rifa(rif: RifasCreate):

    lista_premios = rif.premios.split(" ")
    with Session(engine) as session:
        rrifa = Rifas(id_usuario=rif.id_usu, estado="Abierta", cantidad=rif.cantidad, precio=rif.precio)


        rrifa.estado_numero = ""
        rrifa.numero = ""
        for i in range(rif.cantidad):
            rrifa.numero += str(i)
            rrifa.estado_numero += "Comprar"

            if i != (rif.cantidad-1):
                rrifa.numero += " "
                rrifa.estado_numero += " "

        rrifa.premios = ' '.join(lista_premios)

        session.add(rrifa)  #guarda el registro en la "session"
        session.commit()    #guarda los datos en la database
        session.refresh(rrifa)

        rif.id_usu = rrifa.id_usuario
        rif.cantidad = rrifa.cantidad
        rif.precio = rrifa.precio
        rif.premios = rrifa.premios
        return rif



#PARA CUANDO SE DESEA ENTRAR CON LA CUENTA DE UN USUARIO
def ingresar_usuario(usu_nombre: str, usu_clave: str):

    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.nombre == usu_nombre, Usuario.clave == usu_clave)         #Eso le dice que queremos seleccionar todas las columnas necesarias de la tabla USUARIO donde el ID sea 0.
        resultado = session.exec(seleccion)     #Esto le indicará a la "sesión"que debe ejecutar ese SELECT en la base de datos y recuperar los resultados.

        usu = resultado.first()       #con esto se guarda, en "usuario", el primer registro encontrado
        mostrar = UsuarioRead()
        if usu != None:
            mostrar.id = usu.id
            mostrar.nombre = usu.nombre
            mostrar.clave = usu.clave
            mostrar.saldo = usu.saldo

            if(usu.recargas != None):
                mostrar.recargas = usu.recargas
            if(usu.mis_premios != None):
                mostrar.mis_premios = usu.mis_premios
        return mostrar




#PARA MOSTRAR TODAS LAS RIFAS EXISTENTES
def mostrar_rifas():
    with Session(engine) as session:
        seleccion = select(Rifas)
        resultado = session.exec(seleccion)
        lista = list()

        if resultado != None:
            for rifa in resultado:
                agregar = RifasLista(id=rifa.id, estado=rifa.estado, cantidad=rifa.cantidad, precio=rifa.precio, premios=rifa.premios)
                lista.append(agregar)

        return lista


#PARA MOSTRAR TODOS LOS USUARIOS EXISTENTES
def mostrar_usuarios():
    with Session(engine) as session:
        seleccion = select(Usuario)
        resultado = session.exec(seleccion)
        lista = list()

        if resultado != None:
            for usu in resultado:
                agregar = UsuarioRead(id=usu.id, nombre=usu.nombre, clave=usu.clave, saldo=usu.saldo)
                if(usu.recargas != None):
                    agregar.recargas = usu.recargas
                if(usu.mis_premios != None):
                    agregar.mis_premios = usu.mis_premios
                lista.append(agregar)

        return lista




#PARA MOSTRAR LOS NUMEROS DE UNA RIFA SELECCIONADA
def mostrar_numeros(rif_id: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()
        numeros = list()

        lista_numeros = rifa.numero.split(" ")
        lista_estados = rifa.estado_numero.split(" ")
        x=0
        for i in lista_numeros:
            num = RifaNums(numero=i, estado_numero=lista_estados[x])
            numeros.append(num)
            x += 1
    
    return numeros



#PARA MOSTRAR LOS PREMIOS DE UNA RIFA SELECCIONADA
def mostrar_premios(rif_id: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()

        lista_premios = rifa.premios.split(" ")

    return lista_premios




#PARA CUANDO EL USUARIO DESEE DESHABILITAR SU CUENTA
def eliminar_usuario(usu_id: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)
        usuario = resultado.first()
        if usuario == None:
            return "message: ID DE USUARIO INVALIDO"


        seleccion = select(Rifas).where(Rifas.id_usuario == usu_id)
        resultado = session.exec(seleccion)

        for rifa_delete in resultado:
            session.delete(rifa_delete)   #Se eliminan todas las rifas del usuario
            session.commit()

        session.delete(usuario)         #se elimina el usuario
        session.commit()                #se modifica la database

        return ("message: " + usuario.nombre + " ha sido deshabilitado")
        #el objeto "usuario" aun se puede usar para su retorno




#PARA CUENDO SE HAYAN COMPRADO TODOS LOS NUMEROS DE UNA RIFA
def cerrar_rifa(rifa_id: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rifa_id)
        resultado = session.exec(seleccion)

        rifa = resultado.first()
        if rifa != None:
            lista_estados = rifa.estado_numero.split(" ")
            for i in lista_estados:
                if i == 'Comprar':
                    return 'message: NO SE HAN COMPRADO TODOS LOS NUMEROS'
            rifa.estado = "Cerrada"
            session.add(rifa)
            session.commit()
            return rifa.estado




#PARA CUANDO EL USUARIO DECIDA CAMBIAR SU NOMBRE
def modificar_nombre_usuario(new_nombre: str, usu_id: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)

        usuario = resultado.first()
        usuario.nombre = new_nombre
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario.nombre




#PARA CUANDO EL USUARIO DECIDA CAMBIAR SU CLAVE
def modificar_clave_usuario(new_clave: str, usu_id: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)

        usuario = resultado.first()
        usuario.clave = new_clave
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario.clave




#PARA RECARGAR EL SALDO DEL USUARIO
def agregar_saldo_usuario(usu_id: int, re_saldo: int):
    with Session(engine) as session:
        seleccion = select(Usuario).where(Usuario.id == usu_id)
        resultado = session.exec(seleccion)

        usuario = resultado.first()
        usuario.saldo += re_saldo      #se modifica el saldo
        if usuario.recargas == None:
            usuario.recargas = str(re_saldo)
        else:
            usuario.recargas += (" " + str(re_saldo))   #el saldo recargado se agrega al historial del usuario
        session.add(usuario)            #se modifica la sesion
        session.commit()                #se modifica la database
        session.refresh(usuario)        #se actualiza el objeto

    return str(usuario.saldo)





def compra_individual(rif_id: int, usu_nombre: str, numero: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()
        seleccion = select(Usuario).where(Usuario.nombre == usu_nombre)
        resultado = session.exec(seleccion)
        usu = resultado.first()
        error = list()

        if rifa == None:
            error.append("message: INGRESE UNA RIFA VALIDA")
            return error
        if rifa.estado == 'Cerrada':
            error.append("message: ESTA RIFA ESTA CERRADA")
            return error
        if rifa.estado == 'Sorteada':
            error.append("message: ESTA RIFA YA HA SIDO SORTEADA")
            return error
        if usu == None:
            error.append("message: INGRESE SU NOMBRE DE USUARIO")
            return error
        

        lista_estados = rifa.estado_numero.split(" ")
        

        if numero >= len(lista_estados):         #SE COMPRUEBA QUE EL NUMERO ELEGIDO SEA VALIDO
            error.append("message: EL NUMERO A COMPRAR NO EXISTE EN ESTA RIFA")
            return error
        if lista_estados[numero] != 'Comprar':
            error.append("message: EL NUMERO QUE DESEA COMPRAR YA HA SIDO VENDIDO")
            return error
        else:
            lista_estados[numero] = usu_nombre   #EL ESTADO DEL NUMERO SE CAMBIA POR EL NOMBRE DEL USUARIO QUE LO COMPRO
            usu.saldo -= rifa.precio
            rifa.estado_numero = " "
            rifa.estado_numero = rifa.estado_numero.join(lista_estados)
            session.add(rifa)
            session.commit()
            return lista_estados



def comprar_numeros(rif_id: int, usu_nombre: str, numeros: int):
    with Session(engine) as session:
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()
        seleccion = select(Usuario).where(Usuario.nombre == usu_nombre)
        resultado = session.exec(seleccion)
        usu = resultado.first()
        error = list()

        if rifa == None:
            error.append("message: INGRESE UNA RIFA VALIDA")
            return error
        if rifa.estado == 'Cerrada':
            error.append("message: ESTA RIFA ESTA CERRADA")
            return error
        if rifa.estado == 'Sorteada':
            error.append("message: ESTA RIFA YA HA SIDO SORTEADA")
            return error
        if usu == None:
            error.append("message: INGRESE SU NOMBRE DE USUARIO")
            return error
        

        lista_estados = rifa.estado_numero.split(" ")
        x = 0
        for i in lista_estados:        
            if i == 'Comprar':
                x += 1
        

        if numeros <= x:         #SE COMPRUEBA QUE LA CANTIDAD DE NUMEROS A COMPRAR ESTE DISPONIBLE
            for i in range(numeros):
                x = random.randint(0,(len(lista_estados)-1))    #PARA RECORRER TODOS LOS NUMEROS DE FORMA AL AZAR
                while lista_estados[x] != 'Comprar':
                    x = random.randint(0,(len(lista_estados)-1))

                lista_estados[x] = usu_nombre   #EL ESTADO DEL NUMERO SE CAMBIA POR EL NOMBRE DEL USUARIO QUE LO COMPRO
                usu.saldo -= rifa.precio

            rifa.estado_numero = " "
            rifa.estado_numero = rifa.estado_numero.join(lista_estados)
            
            session.add(rifa)
            session.commit()
            return lista_estados
        else:
            mensaje = list()
            mensaje.append("message: CANTIDAD DE NUMEROS INVALIDA    MAX-->" + str(x))
            return mensaje




#PARA CUANDO EL PROPIETARIO DECIDA SORTEAR LA RIFA
def sortear_rifa(rif_id: int):
    with Session(engine) as session:
        mensaje = list()
        seleccion = select(Rifas).where(Rifas.id == rif_id)
        resultado = session.exec(seleccion)
        rifa = resultado.first()

        if rifa == None:
            mensaje.append('message: EL ID ES INVALIDO')
            return mensaje


        if rifa.estado == 'Cerrada':
            lista_estados = rifa.estado_numero.split(" ")
            lista_premios = rifa.premios.split(" ")
            ganadores = list()

            for i in lista_premios:
                x = random.randint(0,(len(lista_estados)-1))    #PARA RECORRER TODOS LOS NUMEROS DE FORMA AL AZAR
                while lista_estados[x] == 'GANADOR':
                    x = random.randint(0,(len(lista_estados)-1)) 

                ganadores.append(lista_estados[x])
                lista_estados[x] = 'GANADOR'




            x=0
            for i in ganadores:
                seleccion = select(Usuario).where(Usuario.nombre == i)
                resultado = session.exec(seleccion)
                usuario = resultado.first()
                if usuario.mis_premios == None:
                    usuario.mis_premios = ""
                    usuario.mis_premios += str(lista_premios[x])
                else:
                    usuario.mis_premios += ("   "+str(lista_premios[x]))
                x += 1
                session.add(usuario)
                session.commit()


            x=0
            for i in ganadores:
                lista_premios[x] += ("-->" + str(i))
                if x != (len(ganadores)-1):
                    lista_premios[x] += (" ")
                x += 1

            rifa.premios = " "
            rifa.premios = rifa.premios.join(lista_premios)
            rifa.estado = "Sorteada"
            session.add(rifa)
            session.commit()
            return lista_premios
        else:
            mensaje.append('message: LA RIFA SIGUE ABIERTA')
            return mensaje
