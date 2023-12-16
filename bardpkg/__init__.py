from bardapi import Bard
import os


def checkapi(api):
        os.environ["_BARD_API_KEY"] = api
        print(api+" bardpkg")
        try:
                message = "Hola bard"
                #solver = TwoCaptcha(api)
                print(Bard().get_answer(str(message))['content'])
        except:
                
                return "error"


def respuesta(api,tema,dificultad):
        os.environ["_BARD_API_KEY"] = api
        message = f"Crea 10 preguntas tipo test sobre {tema} de nivel {dificultad} serán 10 preguntas tipo test con 4 respuestas posibles (a,b,c,d), haz que las preguntas sean muy rebuscadas y que las respuestas correctas no siempre esten en la posición (a), han de tener el siguiente formato: número de la pregunta) + (pregunta) (2 saltos de linea) (letra a) (Respuesta 1) (1 salto de linea) (letra b) (Respuesta 2) (1 salto de linea) (letra c) (Respuesta 3) (1 salto de linea) (letra d) (Respuesta 4), (2 saltos de linea) (letra de la respuesta correcta sin texto adicional, solo entre corchetes), las letras de cada respuesta deben ir entre parentesis(), el número de la pregunta entre brackets <> y la letra de la respuesta correcta entre corchetes [], sigue este formato al pie de la letra y no pongas subrayados ni negritas"
        retorno = Bard().get_answer(str(message))['content']
        print(retorno)
        archivo = open('output.txt', 'w')
        archivo.write(str(retorno.replace("*", "")))
        archivo.close()

