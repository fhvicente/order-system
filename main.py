from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from inserir_clientes import NovoClienteForm
from lista_clientes import ListaClientes
from nova_encomenda import NovaEncomendaForm
from lista_encomendas import ListaEncomendas

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation="vertical")
        self.add_widget(self.bl)

        self.bl.add_widget(Label(text='Menu Principal'))

        self.btn = Button(text='Novo Cliente')
        self.btn.bind(on_release=self.novo)
        self.bl.add_widget(self.btn)

        self.btn = Button(text='Lista de Clientes')
        self.btn.bind(on_release=self.lista)
        self.bl.add_widget(self.btn)

        self.btn = Button(text='Nova Encomenda')
        self.btn.bind(on_release=self.nova)
        self.bl.add_widget(self.btn)

        self.btn = Button(text='Lista de Encomendas')
        self.btn.bind(on_release=self.lista_enco)
        self.bl.add_widget(self.btn)

    def novo(self, *args):
        self.manager.current = 'novo_cliente'

    def lista(self, *args):
        self.manager.current = 'lista_cliente'

    def nova(self, *args):
        self.manager.current = 'nova_encomenda'

    def lista_enco(self, *args):
        self.manager.current = 'lista_encomenda'

    

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu_principal'))
        sm.add_widget(NovoClienteForm(name='novo_cliente'))
        sm.add_widget(ListaClientes(name='lista_cliente'))
        sm.add_widget(NovaEncomendaForm(name='nova_encomenda'))
        sm.add_widget(ListaEncomendas(name='lista_encomenda'))
        return sm

if __name__ == '__main__':
    MainApp().run()