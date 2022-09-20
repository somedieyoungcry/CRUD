from optparse import Values
import matplotlib.pyplot as plt 
import pandas as pd
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST = 'localhost'
MONGO_PUERTO = '27017'
MONGO_TIEMPO_FUERA = 1000
df = pd.read_csv("tether.csv")

MONGO_URI = "mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"
MONGO_BASEDATOS = "pFinal"
MONGO_COLECCION = "cryptos"
cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMs=MONGO_TIEMPO_FUERA)
baseDatos = cliente[MONGO_BASEDATOS]
coleccion = baseDatos[MONGO_COLECCION]
ID_Crypto = ""
def mostrarDatos():
    try:
        for documento in coleccion.find():
            tabla.insert('',0,text = documento["_id"], values=documento["Fecha"])
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print ("Tiempo excedido" + errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print ("Fallo al conectarse a mongoDB" + errorConexion)
def crearRegistro():
    if len(nombre.get())!=0 and len(op.get())!=0 and len(cl.get())!=0:
        try:
            documento =  {"Fecha":nombre.get(), "Open": op.get(), "Close": cl.get()}
            coleccion.insert_one(documento)
            nombre.delete(0,END)
            op.delete(0,END)
            cl.delete(0,END)
            
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Fallo de Registro")
    mostrarDatos()
        
def dobleClickTabla(event):
    global ID_Crypto 
    ID_Crypto = str(tabla.item(tabla.selection())["text"])
    documento = coleccion.find({"_id":ObjectId(ID_Crypto)})[0]
    #print(documento)
    nombre.delete(0,END)
    nombre.insert(0,documento["Fecha"])
    op.delete(0,END)
    op.insert(0,documento["Open"])
    cl.delete(0,END)
    cl.insert(0,documento["Close"])
    crear["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"          
def editarRegistro():
    global ID_Crypto
    if len(nombre.get())!=0 and len(op.get())!=0 and len(cl.get())!=0:
        try:
            idBuscar={"_id":ObjectId(ID_Crypto)}
            nuevosValores = {"Fecha":nombre.get(), "Open":op.get(), "Close":cl.get()}
            coleccion.update(idBuscar, nuevosValores)
            nombre.delete(0,END)
            op.delete(0,END)
            cl.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
        mostrarDatos()
    crear["state"]="normal"
    editar["state"]="disabled"  
    borrar["state"]="disabled"           
def borrarRegistro():
    global ID_Crypto
    try:
        idBuscar = {"_id":ObjectId(ID_Crypto)}
        coleccion.delete_one(idBuscar)
        nombre.delete(0,END)
        op.delete(0,END)
        cl.delete(0,END)
    except pymongo.errors.ConnectionFailure as error:      
        print(error) 
    crear["state"]="normal"
    editar["state"]="disabled"   
    borrar["state"]="disabled"        
    mostrarDatos()         
ventana = Tk()
ventana.title("CRUD")
ventana.configure(bg='#07EF32')
tabla = ttk.Treeview(ventana, columns = 2) 
tabla.grid(row=1, column=1,columnspan=20) 
tabla.heading("#0", text="ID")
tabla.heading("#1", text="Dia")
tabla.bind("<Double-Button-1>", dobleClickTabla)
#nombre
Label(ventana, text="Fecha", bg='#F5EE5A').grid(row=2, column=0, sticky=W+E)
nombre = Entry(ventana)
nombre.configure(bg='#F5EE5A')
nombre.grid(row=2, column=1, sticky=W+E)
nombre.focus()
#Open
Label(ventana, text="Open", bg='#F5EE5A').grid(row=3, column=0, sticky=W+E)
op = Entry(ventana)
op.configure(bg='#F5EE5A')
op.grid(row=3, column=1, sticky=W+E)
#Close
Label(ventana, text="Close", bg='#F5EE5A').grid(row=4, column=0, sticky=W+E)
cl = Entry(ventana)
cl.configure(bg='#F5EE5A')
cl.grid(row=4, column=1, sticky=W+E)
#Boton Crear
crear = Button(ventana, text = "Crear Registro", command=crearRegistro, bg="#2FF32F", fg="white")
crear.grid(row=5, columnspan=2, sticky=W+E)
#Boton editar
editar=Button(ventana, text = "Editar registro", command = editarRegistro, bg="#BBF32F")
editar.grid(row=6, columnspan=2, sticky=W+E)
editar["state"] = "disabled"
#Boton borrar
borrar=Button(ventana, text = "Borrar registro", command = borrarRegistro, bg="#E7F32F", fg="white")
borrar.grid(row=7, columnspan=2, sticky=W+E)
borrar["state"] = "disabled"
mostrarDatos()

ventana.mainloop() 

plot1 = df.plot("Date", "Open", color = '#03F9E6')
plt.title("Grafica de apertura")
plot2 = df.plot("Date", "Close", color = '#88c999')
plt.title("Grafica de Cierre")
plot3 = df.plot("Date", "Alto", color = '#DF3D1A')
plt.title("Valor mas alto")
plot4 = df.plot("Date", "Bajo", color = '#0AF903')
plt.title("Valor mas bajo")
#plot3 = plot2.scatter("Date", "Close")
#plot2.scatter("Date", "Close")
plt.show()