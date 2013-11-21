#!/usr/bin/env python
# -⁻- coding: UTF-8 -*-
#Requiere tener instalado python y la libreria de reportlab

from Tkinter import *
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table
import codecs


#======================CLASES===================
class LetterMaker(object):

    def __init__(self, pdf_file, org, seconds):
        self.c = canvas.Canvas(pdf_file, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.width, self.height = letter
        self.organization = org
        self.seconds  = seconds

    def createDocument(self, address, body, greetings):
        voffset = 120

        # create return address
        paragraph = Paragraph(address.nombre+"<br />"+address.direccion1+"<br />"+address.direccion2+"<br />"+address.direccion3+"<br />"+address.direccion4, self.styles["Normal"])
        header = [["",paragraph]]
        table = Table(header, colWidths=4*inch)
        table.setStyle([("VALIGN", (0,0), (0,0), "TOP")])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(18, 60, mm))

        # insert body of letter
        p = Paragraph(body, self.styles["Normal"])
        p.wrapOn(self.c, self.width-70, self.height)
        p.drawOn(self.c, *self.coord(20, voffset+50, mm))

        # greetings
        try:
            p = Paragraph(greetings.nombre+"<br />"+greetings.direccion1+"<br />"+greetings.direccion2+"<br />"+greetings.direccion3+"<br />"+greetings.direccion4, self.styles["Normal"])
        except:
            p = Paragraph("", self.styles["Normal"])
        p.wrapOn(self.c, self.width-70, self.height)
        p.drawOn(self.c, *self.coord(20, voffset+75, mm))


    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y

    #----------------------------------------------------------------------
    def createParagraph(self, ptext, x, y, style=None):
        if not style:
            style = self.styles["Normal"]
        p = Paragraph(ptext, style=style)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))

    #----------------------------------------------------------------------
    def savePDF(self):
        self.c.save()

#Persona puede ser apelante o destinatario
class Persona:
    def __init__(self, nombre, direccion1, direccion2, direccion3, direccion4):
        self.nombre = nombre
        self.direccion1 = direccion1
        self.direccion2 = direccion2
        self.direccion3 = direccion3
        self.direccion4 = direccion4

#======================FUNCIONES===================

def textoEnMedio(sCadena, sDelimitador1, sDelimitador2):
  pos=sCadena.find(sDelimitador1)+len(sDelimitador1)
  pos2=sCadena.find(sDelimitador2)
  return sCadena[pos:pos2]

def comenzar(rutaApelantes,rutaCarta):
    apelantes = crear_apelantes(rutaApelantes)
    cuerpo1 = crear_cuerpo1(rutaCarta)
    cuerpo2 = crear_cuerpo2(rutaCarta)
    autoridades = crear_autoridades(rutaCarta)
    contadorCartas1 = 0
    contadorCartas2 = 0
    for apelante in apelantes:
        crear_carta(apelante,cuerpo2,"",contadorCartas2)
        contadorCartas2 = contadorCartas2+1
        for autoridad in autoridades:
            contadorCartas1 = contadorCartas1+1
            crear_carta(autoridad,cuerpo1,apelante,contadorCartas1)
    res.set("Hecho, la lucha continúa!")
		
def crear_carta(destinatario,cuerpo,cierre, contadorCartas):
    doc = LetterMaker("carta"+str(contadorCartas)+".pdf", "The MVP", 10)
    doc.createDocument(destinatario, cuerpo, cierre)
    doc.savePDF()

def crear_apelantes(rutaApelantes):
    ficheroApelantes = open(rutaApelantes, 'r')
    apelantesAPelo = ficheroApelantes.readlines()
    ficheroApelantes.close()
    x=0
    apelantes=[]
    for i in range(len(apelantesAPelo)/5):
        nombre = apelantesAPelo[0+x]
        direccion1 = apelantesAPelo[1+x]
        direccion2 = apelantesAPelo[2+x]
        direccion3 = apelantesAPelo[3+x]
        direccion4 = "España"
        apelantes.append(Persona(nombre, direccion1, direccion2, direccion3, direccion4))
        x=x+6
    return apelantes

def crear_autoridades(rutaCarta):
    ficheroCarta = open(rutaCarta, 'r')
    autoridadesAPelo =  textoEnMedio(str(ficheroCarta.readlines()), "#Autoridades\n", "#Cuerpo1")
    ficheroCarta.close()
    x=1
    autoridades=[]
    autoridadesRetocadas = autoridadesAPelo.split("\\n")
    for i in range((len(autoridadesRetocadas)/6)):
        nombre = autoridadesRetocadas[0+x]
        direccion1 = autoridadesRetocadas[1+x]
        direccion2 = autoridadesRetocadas[2+x]
        direccion3 = autoridadesRetocadas[3+x]
        direccion4 = autoridadesRetocadas[4+x]
        autoridades.append(Persona(nombre, direccion1, direccion2, direccion3, direccion4))
        x=x+6
    return autoridades

def crear_cuerpo1(rutaCarta):
    ficheroCarta = codecs.open(rutaCarta, "r", encoding='utf-8')
    #buscar cuerpo1, entonces leer hasta cuerpo2
    cuerpo =textoEnMedio(str(ficheroCarta.readlines()), "#Cuerpo1", "#Cuerpo2")
    print cuerpo
    return cuerpo

def crear_cuerpo2(rutaCarta):
    ficheroCarta = open(rutaCarta, "r")
    cuerpo = textoEnMedio(str(ficheroCarta.readlines()), "#Cuerpo2", "#Fin")
    return cuerpo


#=======================MAIN=======================

#ventana principal
master = Tk()
frame = Frame(master, height=3200, width=80)
frame.pack()


#caja de texto de la ruta 1
rutaApelantes = StringVar()
textRutaApelantes = Entry(frame, textvariable=rutaApelantes, width=50)
textRutaApelantes.pack(side=LEFT)
#textRutaApelantes.insert(0, "Ruta completa del fichero de apelantes")
textRutaApelantes.insert(0, "C:/Users/Pablo/Dropbox/apuntes/AI Deberes/apelantes/apelantes.txt")

#caja de texto de la ruta 2
rutaCarta = StringVar()
textRutaCarta = Entry(frame, textvariable=rutaCarta, width=50)
textRutaCarta.pack(side=LEFT)
#textRutaCarta.insert(0, "Ruta completa de la carta")
textRutaCarta.insert(0, "C:/Users/Pablo/Dropbox/apuntes/AI Deberes/apelantes/cartas.txt")

#boton
accion = lambda: comenzar(rutaApelantes.get(), rutaCarta.get())
button = Button(frame, text="Crear cartas", command=accion)
button.pack(side=RIGHT)


#etiqueta para mostrar resultado
res = StringVar()
Label(frame, textvariable=res).pack()
res.set("Sin Empezar")


#para que se mantenga el programa sin cerrarse
frame.mainloop()



