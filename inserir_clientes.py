from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import requests

class NovoClienteForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation="vertical")
        self.add_widget(self.bl)

        self.bl.add_widget(Label(text='Nome do cliente'))
        self.nome_input = TextInput()
        self.bl.add_widget(self.nome_input)

        self.bl.add_widget(Label(text='Morada do cliente'))
        self.morada_input = TextInput()
        self.bl.add_widget(self.morada_input)

        self.bl.add_widget(Label(text='Telefone do cliente'))
        self.telefone_input = TextInput()
        self.bl.add_widget(self.telefone_input)

        self.adicionar_cliente_btn = Button(text='Adicionar Cliente', size_hint_y=None, height=50)
        self.adicionar_cliente_btn.bind(on_release=self.adicionar_cliente)
        self.bl.add_widget(self.adicionar_cliente_btn)

        self.voltar_menu_btn = Button(text='Voltar ao Menu Inicial', size_hint_y=None, height=50)
        self.voltar_menu_btn.bind(on_release=self.voltar_menu_inicial)
        self.bl.add_widget(self.voltar_menu_btn)


    def adicionar_cliente(self, *args):
        novo_cliente = {
            'nome': self.nome_input.text,
            'morada': self.morada_input.text,
            'telefone': self.telefone_input.text
        }
        r = requests.post('http://127.0.0.1:5000/clientes', json=novo_cliente)
        if r.status_code == 201:
            self.nome_input.text = ''
            self.morada_input.text = ''
            self.telefone_input.text = ''
            self.adicionar_cliente_btn.text = 'Cliente adicionado!'
        else:
            self.adicionar_cliente_btn.text = 'Erro ao adicionar cliente!'

    def voltar_menu_inicial(self, *args):
        self.manager.current = 'menu_principal'


class MyApp(App):
    def build(self):
        return NovoClienteForm()

if __name__ == '__main__':
    MyApp().run()
