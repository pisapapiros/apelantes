#!/usr/bin/env python
# -⁻- coding: UTF-8 -*-
#Requiere tener instalado python y la libreria de reportlab
#Pablo Camino Bueno, AIUS, 2013

from Tkinter import *
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table
import codecs
import os.path


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
        print "bodyyy"
        print body
        body = body.replace('\n','<br />')
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
    #print cuerpo1
    cuerpo2 = crear_cuerpo2(rutaCarta)
    autoridades = crear_autoridades(rutaCarta)
    contadorCartas1 = 0
    contadorCartas2 = 0
    #print "Todos los apelantes:"
    #for apelante in apelantes:
    #    print apelante.nombre
    #print "_____________________"
    #print "Todas las autoridades:"
    #for autoridad in autoridades:
    #    print autoridad.nombre
    #print "_____________________"
    for apelante in apelantes:
    #    print "iteracion del for apelantes"
        crear_carta(apelante,cuerpo2,"",contadorCartas2)
    #    print "carta creada"
        contadorCartas2 = contadorCartas2+1
        #print "autoridades"
        for autoridad in autoridades:
            contadorCartas1 = contadorCartas1+1
            #print "vamos a crear carta"
            crear_carta(autoridad,cuerpo1,apelante,contadorCartas1)
            #print "creada!"
    res.set("Hecho, la lucha continúa!")
		
def crear_carta(destinatario,cuerpo,cierre, contadorCartas):
    doc = LetterMaker("carta"+str(contadorCartas)+".pdf", "AI", 10)
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
    #print "entro a crear_autoridades"
    ficheroCarta = open(rutaCarta, 'r')
    texto=""
    for line in ficheroCarta.readlines():
        texto=texto+line
    autoridadesAPelo =  textoEnMedio(texto, "#Destinatarios\n", "#Cuerpo1")
    #print autoridadesAPelo
    ficheroCarta.close()
    x=0
    autoridades=[]
    autoridadesRetocadas2=[]
    autoridadesRetocadas3=[]
    autoridadesRetocadas = autoridadesAPelo.split("#")
    for a in autoridadesRetocadas:
        autoridadesRetocadas2.append(a.split('\n'))
    #print autoridadesRetocadas2
    #print "__________________"
    for x in autoridadesRetocadas2:
    #    print x
    #    print
        autoridadesRetocadas3.append([elem for elem in x if elem !=""])
    #print "autoridadesRetocadas3"
    #for a in autoridadesRetocadas3:
        #print
        #print a
    for a in autoridadesRetocadas3:
        nombre = a[0]
        direccion1 = a[1]
        direccion2 = a[2]
        direccion3 = a[3]
        direccion4 = a[4]
        autoridades.append(Persona(nombre, direccion1, direccion2, direccion3, direccion4))
    #print "aqui vienen las autoridades"
    return autoridades

def crear_cuerpo1(rutaCarta):
    #print "creo cuerpo1"
    ficheroCarta = codecs.open(rutaCarta, "r", encoding='utf-8')
    #buscar cuerpo1, entonces leer hasta cuerpo2
    texto=""
    for line in ficheroCarta.readlines():
        texto=texto+line
    cuerpo =textoEnMedio(texto, "#Cuerpo1", "#Cuerpo2")
    ficheroCarta.close()
    #print cuerpo
    return cuerpo

def crear_cuerpo2(rutaCarta):
    #print "creo cuerpo2"
    ficheroCarta = open(rutaCarta, "r")
    texto=""
    for line in ficheroCarta.readlines():
        texto=texto+line
    cuerpo = textoEnMedio(texto, "#Cuerpo2", "#Fin")#.decode('utf8')
    ficheroCarta.close()
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
textRutaApelantes.insert(0, os.path.join(os.path.dirname(__file__), 'apelantes.txt').replace('\\','/'))

#caja de texto de la ruta 2
rutaCarta = StringVar()
textRutaCarta = Entry(frame, textvariable=rutaCarta, width=50)
textRutaCarta.pack(side=LEFT)
textRutaCarta.insert(0, os.path.join(os.path.dirname(__file__), 'cartas.txt').replace('\\','/'))

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