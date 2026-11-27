from flask import session

def verificar_administrador(token):
    if not token:
        return False

    usuario = session.get("usuario") or {}

    if usuario.get("rol") == "administrador":
        return True

    return False


def verificar_cliente(token):
    if not token:
        return False

    usuario = session.get("usuario") or {}

    if usuario.get("rol") == "cliente":
        return True

    return False