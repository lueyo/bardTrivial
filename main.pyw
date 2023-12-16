import tkinter as tk
from tkinter import messagebox
from bardpkg import checkapi, respuesta
import re
import os


#from grepclone import grep

class TrivialGame(tk.Frame):
    def __init__(self):
        self.makeapiopup()
        #self.makewindow()

    def makeapiopup(self):
        self.apiwn = tk.Tk()
        self.apiwn.title("API Key")
        self.apiwn.geometry("300x100")
        self.apiwn.resizable(False, False)
        self.apiwn.wm_attributes("-topmost", 1)
        self.inputapi = tk.Entry(self.apiwn)
        self.inputapi.pack()
        self.buttonapi = tk.Button(self.apiwn, text="OK", command=self.sendapi)
        self.buttonapi.pack()
        
        self.apiwn.mainloop()
    
    def sendapi(self):
        self.apikey= self.inputapi.get() 
        #(self.apikey)
        if (checkapi(self.apikey)=="error"):
            messagebox.showinfo("Error", "API KEY INCORRECTA")
        else:
            self.apiwn.destroy()
            self.makewindow()

    def makewindow(self):
        self.mwn = tk.Tk()
        self.mwn.title("Trivial Game")
        self.mwn.geometry("600x600")
        self.mwn.wm_attributes("-topmost", 1)
        self.canvas = tk.Canvas(self.mwn)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.frame = tk.Frame(self.canvas)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.pack()
        
        self.difficulty_var = tk.StringVar(self.frame) 
        self.respuestavar = tk.StringVar()
        

        self.generarElementos()
        
        self.mwn.resizable(False, False)
        #self.genanswers()
        self.mwn.mainloop()
    
    def generarElementos(self):
        self.npregunta = 0
        self.aciertos = 0
        self.inputTema = tk.Entry(self.frame) #input de tema
        self.inputTema.pack()
        self.difficulty_var.set("Select an Option") 
        self.difficulty_dropdown = tk.OptionMenu(self.frame, self.difficulty_var, "principiante", "intermedio", "avanzado")
        self.difficulty_dropdown.pack()
        
        self.preguntaLabel = tk.Label(self.frame, text="p")
        self.preguntaLabel.pack()
        self.radio_button1 = tk.Radiobutton(self.frame, text="a", variable=self.respuestavar, value="[a]")
        self.radio_button1.pack()

        self.radio_button2 = tk.Radiobutton(self.frame, text="b", variable=self.respuestavar, value="[b]")
        self.radio_button2.pack()

        self.radio_button3 = tk.Radiobutton(self.frame, text="c", variable=self.respuestavar, value="[c]")
        self.radio_button3.pack()

        self.radio_button4 = tk.Radiobutton(self.frame, text="d", variable=self.respuestavar, value="[d]")
        self.radio_button4.pack()
        
        self.start_button = tk.Button(self.frame, text="Comenzar", command=self.genanswers)
        self.start_button.pack()
        
    def delElementos(self):
        self.preguntaLabel.destroy()
        self.radio_button1.destroy()
        self.radio_button2.destroy()
        self.radio_button3.destroy()
        self.radio_button4.destroy()
        self.start_button.destroy()
        self.continue_button.destroy()
    def encontrar_linea(self, texto, dato):
        lineas = texto.split('\n')
        for i, linea in enumerate(lineas, start=1):
            if re.search(fr'<{dato}>', linea):
                #print(i)
                return i
        return -1
    def genanswers(self):
        self.tema = self.inputTema.get()
        self.difficulty = self.difficulty_var.get()
        #print(str(self.apikey+" "+self.tema+" "+self.difficulty))
        respuesta(self.apikey,self.tema,self.difficulty)
        self.setanswers()


    def setanswers(self): 
        self.arrayPreguntas:str = []
        self.arrayRespuestas:str = [[],[],[],[]]
        self.arrayCorrectas:str = []
        self.arrayTusRespuestas= []
        self.archivo = open('output.txt', 'r')
        self.archivoContent = self.archivo.read()
        
  
        
        for i in range(1, 11):
            line = re.search(fr"<{i}>.*", self.archivoContent)
            #offset:str = self.archivoContent.find("<{i}>") + len("<{i}>")
            if line:
                self.arrayPreguntas.append(line.group())
            #print(self.arrayPreguntas[i-1])# Search for the lines containing the letters "a", "b", "c", and "d" enclosed in parentheses
            #matches_a = re.search(r"\(a\).*", self.archivoContent
            start_index = line.end() if line else 0
            
            matches_a = re.search(r"\(a\).*", self.archivoContent[start_index:])
            matches_b = re.search(r"\(b\).*", self.archivoContent[start_index:])
            matches_c = re.search(r"\(c\).*", self.archivoContent[start_index:])
            matches_d = re.search(r"\(d\).*", self.archivoContent[start_index:])
            matches_correct = re.search(r"\[?.\].*", self.archivoContent[start_index:])
            
            
            
            if matches_a:
                self.arrayRespuestas[0].append(matches_a.group())
                #(self.arrayRespuestas)
            if matches_b:
                self.arrayRespuestas[1].append(matches_b.group())
            if matches_c:
                self.arrayRespuestas[2].append(matches_c.group())
            if matches_d:
                self.arrayRespuestas[3].append(matches_d.group())
            if matches_correct:
                self.arrayCorrectas.append(matches_correct.group())

        # Append the lines to the respective arrays in self.arrayRespuestas
                
        #print(self.arrayPreguntas)
        #print(self.arrayRespuestas)
        #print(self.arrayCorrectas)
        self.ponerPreguntas()
            
            
            
    """ def ventanaCorrección(self):
        self.wcrrtn = tk.Tk()
        self.wcrrtn.title("Corrección")
        self.wcrrtn.geometry("300x500")
        self.labelCoreccion = tk.Label(self.wcrrtn)
        self.labelCoreccion.pack()
        if self.arrayRespuestas == self.arrayTusRespuestas:
            self.preguntaLabel.config(text=self.arrayRespuestas[0], color=#00ff00)
        self.wcrrtn.resizable(False, False)
        self.wcrrtn.wm_attributes("-topmost", 1)
        self.wcrrtn.mainloop()     """    
    def ponerPreguntas(self):
        
        
        
        
        self.inputTema.destroy()
        self.difficulty_dropdown.destroy()
        self.start_button.destroy()
        
        self.preguntaLabel.config(text=self.arrayPreguntas[self.npregunta])
        self.radio_button1.config(text=self.arrayRespuestas[0][self.npregunta])
        self.radio_button2.config(text=self.arrayRespuestas[1][self.npregunta])
        self.radio_button3.config(text=self.arrayRespuestas[2][self.npregunta])
        self.radio_button4.config(text=self.arrayRespuestas[3][self.npregunta])
        
        if self.npregunta == 0:
            self.continue_button = tk.Button(self.frame, text="Siguiente", command=self.siguientePregunta)
            self.continue_button.pack()
    
    def siguientePregunta(self):
        
        self.arrayTusRespuestas.append(self.respuestavar.get())
        if self.arrayTusRespuestas[self.npregunta]==self.arrayCorrectas[self.npregunta]:
            self.aciertos = self.aciertos + 1
        
        self.npregunta = self.npregunta + 1
        if self.npregunta < 10:
            self.ponerPreguntas()
        else:
            self.retry()
    def retry(self):
        aciertosprev = self.aciertos
        self.delElementos()
        self.generarElementos()
        messagebox.showinfo("Nota", f"{str(aciertosprev)}/10")
        
        
    
    
trivialGame = TrivialGame()