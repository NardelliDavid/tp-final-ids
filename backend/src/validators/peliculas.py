def validar_titulo_pelicula(titulo):
    titulo = titulo.lower()
    caracteres_permitidos = "qwertyuiopasdfghjklñzxcvbnm1234567890 "
    for caracter in titulo:
        if caracter not in caracteres_permitidos:
            return {"Error":"El titulo tiene caracteres invalidos"}, 400
    return {"OK":"El titulo es valido"}, 200
