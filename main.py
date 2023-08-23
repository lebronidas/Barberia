
from kivy.app import App 
import sqlite3
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from datetime import datetime as dt
import pandas as pd
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import os
from kivy.config import Config
import sys
import random


Config.set('kivy','window_icon','opt/Ilustración_sin_título.png')

#definimos las diferentes ventanas
Sm=ScreenManager()

class primera_pantalla(Screen):

    db = 'database/clientes.db'  # creamos conexion con BBDD

    nombre=ObjectProperty(None)
    precio=ObjectProperty(None)
    propina=ObjectProperty(None)

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:  # iniciamos conexion con BBDD alias con
            cursor = con.cursor()  # generamos un cursor para poder operar en la BBDD
            resultado = cursor.execute(consulta, parametros)  # se prepara la consulta con sus parametros si los tiene
            con.commit()  # se guardan los cambios realizados
        return resultado  # se devuelve el resultado

    def guardar_cliente(self):
        if self.nombre.text!='' and self.precio.text!='' and self.propina.text!='':
            query='INSERT INTO cliente VALUES(?,?,?,?,NULL)'
            parametros=(self.nombre.text,self.precio.text,dt.now(),self.propina.text)
            self.db_consulta(query, parametros)
            self.nombre.text=''
            self.precio.text=''
            self.propina.text=''
            self.ids.error.text=''

        elif self.nombre.text!='' and self.precio.text!='' and self.propina.text=='':
            query='INSERT INTO cliente VALUES(?,?,?,?,NULL)'
            parametros=(self.nombre.text,self.precio.text,dt.now(),0)
            self.db_consulta(query, parametros)
            self.nombre.text=''
            self.precio.text=''
            self.propina.text=''
            self.ids.error.text=''

        else:
            self.ids.error.text='Nombre y Precio obligatorios'

    def totales(self):
        con=sqlite3.connect('database/clientes.db')
        clientes=pd.read_sql_query('SELECT * from cliente',con)
        total_precio=clientes['precio'].sum()
        total_propina=clientes['propina'].sum()
        precios=str(total_precio)
        propinas=str(total_propina)
        self.ids.precios.text = f'Total precios:{precios}'
        self.ids.propinas.text = f'Total propinas:{propinas}'

    def on_enter(self):
        self.totales()
        self.ids.error.text=''

class segunda_pantalla(Screen):
    
    def spinner_clicked(self,cual):
        if cual =='Mas reciente':
            self.ids.lista.text = cual
            self.ordenar_fecha()
        elif cual =='Mas antiguo':
            self.ids.lista.text = cual
            self.ordenar_fecha_ascendente()
        elif cual =='Mayor propina':
            self.ids.lista.text = cual
            self.mayor_propina()
        else:
            pass

    def pandas(self):
        con=sqlite3.connect('database/clientes.db')
        clientes=pd.read_sql_query('SELECT * from cliente',con)
        (clientes.head())
        nombre=clientes.loc[:,['nombre']].to_string(index=False)
        precio=clientes.loc[:,['precio']].to_string(index=False)
        propina=clientes.loc[:,['propina']].to_string(index=False)
        name=self.ids.nombre.text
        self.ids.nombre.text = nombre
        self.ids.precio.text = precio
        self.ids.propina.text = propina
        return clientes

    def total(self):
        con=sqlite3.connect('database/clientes.db')
        clientes=pd.read_sql_query('SELECT * from cliente',con)
        total_precio=clientes['precio'].sum()
        total_propina=clientes['propina'].sum()
        precios=str(total_precio)
        propinas=str(total_propina)
        name=self.ids.precios.text
        names=self.ids.propinas.text
        self.ids.precios.text = f'total precios:{precios}'
        self.ids.propinas.text = f'total propinas:{propinas}'

    def ordenar_fecha(self):
        con=sqlite3.connect('database/clientes.db')
        clientes=pd.read_sql_query('SELECT * from cliente',con)
        clients=clientes.sort_values(by='fecha',ascending=False).head(16)
        nombre=clients.loc[:,['nombre']].to_string(index=False)
        precio=clients.loc[:,['precio']].to_string(index=False)
        propina=clients.loc[:,['propina']].to_string(index=False)
        name=self.ids.nombre.text
        self.ids.nombre.text = nombre
        self.ids.precio.text = precio
        self.ids.propina.text = propina

    def ordenar_fecha_ascendente(self):
        con=sqlite3.connect('database/clientes.db')
        clientes=pd.read_sql_query('SELECT * from cliente',con)
        clients=clientes.sort_values(by='fecha',ascending=True).head(16)
        nombre=clients.loc[:,['nombre']].to_string(index=False)
        precio=clients.loc[:,['precio']].to_string(index=False)
        propina=clients.loc[:,['propina']].to_string(index=False)
        name=self.ids.nombre.text
        self.ids.nombre.text = nombre
        self.ids.precio.text = precio
        self.ids.propina.text = propina

    def mayor_propina(self):
        con=sqlite3.connect('database/clientes.db')
        clientes=pd.read_sql_query('SELECT * from cliente',con)
        clients=clientes.sort_values(by='propina',ascending=False).head(16)
        nombre=clients.loc[:,['nombre']].to_string(index=False)
        precio=clients.loc[:,['precio']].to_string(index=False)
        propina=clients.loc[:,['propina']].to_string(index=False)
        name=self.ids.nombre.text
        self.ids.nombre.text = nombre
        self.ids.precio.text = precio
        self.ids.propina.text = propina

class tercera_pantalla(Screen):
        
    def convertirBBDD(self):
        mess=dt.now()
        mes=(mess.strftime("%B"))
        con=sqlite3.connect('database/clientes.db')
        clientes=pd.read_sql_query('SELECT * from cliente',con)
        clients=clientes.sort_values(by='fecha',ascending=False).to_string(index=False)
        name=self.ids.todos.text
        html=clientes.to_html()
        try:
            path=os.mkdir('../registros/')
        except:
            pass
        num=int(random.randint(0,9))
        nombre=f'registro_{mes}{num}.html'
        ruta='../registros/'
        direct=os.path.join(ruta,nombre)
        with open(direct, 'w') as f:
            f.write(html)
        self.ids.todos.text = 'Archivo guardado'
    
    db = 'database/clientes.db'
    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:  
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado
    
    def borrarBBDD(self):
        query='DELETE FROM cliente'
        parametros=''
        self.db_consulta(query,parametros)
        self.ids.todos.text='Base de datos vaciada'

class Manager(ScreenManager):
    pass

#cargamos el archivo con la configuracion kv
Builder.load_file('new_window.kv')

class Barberia(App):
    def build(self):
        self.icon= 'opt/Ilustración_sin_título.png'
        Sm.add_widget(primera_pantalla(name='primera_pantalla'))
        Sm.add_widget(segunda_pantalla(name='segunda_pantalla'))
        Sm.add_widget(tercera_pantalla(name='tercera_pantalla'))
        return Sm


if __name__ == '__main__':
    Barberia().run()
    primera_pantalla().totales()