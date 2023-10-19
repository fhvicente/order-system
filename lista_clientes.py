from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import requests

class ListaClientes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation="vertical")
        self.add_widget(self.bl)

        self.scrollview = ScrollView()
        self.bl.add_widget(self.scrollview)

        self.clientes_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.scrollview.add_widget(self.clientes_layout)

        self.voltar_menu_btn = Button(text='Voltar ao Menu Inicial', size_hint_y=None, height=50)
        self.voltar_menu_btn.bind(on_release=self.voltar_menu_inicial)
        self.bl.add_widget(self.voltar_menu_btn)

    def on_enter(self):
        super().on_enter()
        self.carregar_clientes()

    def carregar_clientes(self):
        self.clientes_layout.clear_widgets()

        r = requests.get('http://127.0.0.1:5000/clientes')
        if r.status_code == 200:
            clientes = r.json()
            for cliente in clientes:
                self.clientes_layout.add_widget(Label(text=f'Nome: {cliente["nome"]}', size_hint_y=None, height=30))
                self.clientes_layout.add_widget(Label(text=f'Morada: {cliente["morada"]}', size_hint_y=None, height=30))
                self.clientes_layout.add_widget(Label(text=f'Telefone: {cliente["telefone"]}', size_hint_y=None, height=30))
                self.clientes_layout.add_widget(Divider(size_hint_y=None, height=1))

        # Atualiza o tamanho do GridLayout
        self.clientes_layout.bind(minimum_height=self.clientes_layout.setter('height'))

    def voltar_menu_inicial(self, *args):
        self.manager.current = 'menu_principal'

class Divider(Label):
    pass

class MyApp(App):
    def build(self):
        return ListaClientes()

if __name__ == '__main__':
    MyApp().run()
