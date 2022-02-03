from turtle import width
from geopy.geocoders import Nominatim
import requests
from datetime import datetime
import PySimpleGUI as sg

class Tela:
    def __init__(self):
        sg.theme('Reddit')

        lado_a = [
            [sg.Text('Cidade:', size=(10,1), font='Arial 12' ), sg.Input(key='cidade', size=(45,5), font='Arial 12'), sg.Button('Pesquisar', size=(10,1))],  
            [sg.Text('Temperatura:',size=(10,1), font='Arial 12'), sg.Text(key='temp', size=(20,1), font='Arial 12')],        
            [sg.Text('Mínima:',size=(10,1), font='Arial 12'), sg.Text(key='minima', size=(20,1), font='Arial 12')],
            [sg.Text('Máxima:',size=(10,1), font='Arial 12'), sg.Text(key='maxima', size=(20,1), font='Arial 12')],
            [sg.Text('Situação:',size=(10,1), font='Arial 12'), sg.Text(key='descricao', size=(20,1), font='Arial 12')],
            [sg.Text('Data/Hora:',size=(10,1), font='Arial 12'), sg.Text(key='data_hora', size=(20,1), font='Arial 12')],
            [sg.Text('Localização:',size=(10,1), font='Arial 12'), sg.Text(key='location', size=(50,3), font='Arial 12')]            
        ]

        lado_b = [
            [sg.Image(source='logo.png')]            
        ]

        layout = [
            [
                sg.Column(lado_a),
                sg.VSeparator(),
                sg.Column(lado_b)
            ]
        ]

        self.janela = sg.Window('Previsão do Tempo', layout)

    def Iniciar(self):

        while True:
            self.event, self.values = self.janela.Read()


            if self.event == sg.WINDOW_CLOSED:
                break
            if self.event == 'Pesquisar': 

                try:
                    #obtendo a latitude e longitude

                    cidade = self.values['cidade']

                    geolocator = Nominatim(user_agent="main")
                    location = geolocator.geocode(cidade)
                    lon = location.longitude
                    lat = location.latitude

                    #fazendo a requisição da API
                    key = '8cef1367f56402ade307b1eb06187765'
                
                    request = requests.get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&lang=pt_br&appid={}'.format(lat,lon, key))
                    tempo = request.json()  

                    self.janela['temp'].update("{:.1f} º Celsius".format(tempo['main']['temp'] - 273.15))
                    self.janela['minima'].update("{:.1f} º Celsius".format(tempo['main']['temp_min'] - 273.15))
                    self.janela['maxima'].update("{:.1f} º Celsius".format(tempo['main']['temp_max'] - 273.15))
                    self.janela['data_hora'].update(datetime.today().strftime('%d-%m-%Y - %H:%M'))
                    self.janela['descricao'].update(tempo['weather'][0]['description'])
                    self.janela['location'].update(location)
                except:
                    self.janela['cidade'].update('Cidade não encontrada. Favor digitar novamente.')
                    self.janela['temp'].update('')
                    self.janela['minima'].update('')
                    self.janela['maxima'].update('')
                    self.janela['data_hora'].update('')
                    self.janela['descricao'].update('')
                    self.janela['location'].update('')

tela = Tela()
tela.Iniciar()