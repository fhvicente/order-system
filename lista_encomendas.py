from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import json
import requests

class ListaEncomendas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation="vertical")
        self.add_widget(self.bl)

        self.scrollview = ScrollView()
        self.bl.add_widget(self.scrollview)

        self.encomendas_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.scrollview.add_widget(self.encomendas_layout)

        self.voltar_menu_btn = Button(text='Voltar ao Menu Inicial', size_hint_y=None, height=50)
        self.voltar_menu_btn.bind(on_release=self.voltar_menu_inicial)
        self.bl.add_widget(self.voltar_menu_btn)

    def on_enter(self):
        super().on_enter()
        self.carregar_encomendas()

    def carregar_encomendas(self):
        self.encomendas_layout.clear_widgets()

        r = requests.get('http://127.0.0.1:5000/encomendas')
        if r.status_code == 200:
            response_data = json.loads(r.text) # Converter a resposta JSON em um dicionário

            encomendas = response_data['encomendas'] # Aceder a lista de encomendas

            for encomenda in encomendas:
                self.encomendas_layout.add_widget(Label(text=f'ID Cliente: {encomenda["id_cliente"]}', size_hint_y=None, height=30))
                self.encomendas_layout.add_widget(Label(text=f'Nome da Pizza: {encomenda["nome_pizza"]}', size_hint_y=None, height=30))
                self.encomendas_layout.add_widget(Label(text=f'Quantidade: {encomenda["quantidade"]}', size_hint_y=None, height=30))
                self.encomendas_layout.add_widget(Label(text=f'Tamanho: {encomenda["tamanho"]}', size_hint_y=None, height=30))
                self.encomendas_layout.add_widget(Label(text=f'Data e Hora: {encomenda["data_hora"]}', size_hint_y=None, height=30))
                self.encomendas_layout.add_widget(Divider(size_hint_y=None, height=1))


        # Atualiza o tamanho do GridLayout
        self.encomendas_layout.bind(minimum_height=self.encomendas_layout.setter('height'))

    def voltar_menu_inicial(self, *args):
        self.manager.current = 'menu_principal'

class Divider(Label):
    pass

class MyApp(App):
    def build(self):
        return ListaEncomendas()

if __name__ == '__main__':
    MyApp().run()