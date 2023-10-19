from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.spinner import Spinner
from datetime import datetime

import requests

class NovaEncomendaForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation="vertical")
        self.add_widget(self.bl)

        self.cliente_label = Label(text='Selecione um cliente:')
        self.bl.add_widget(self.cliente_label)

        self.cliente_dropdown = DropDown()
        self.carregar_clientes()
        self.cliente_btn = Button(text="Cliente", size_hint=(None, None), size=(200, 30), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.cliente_btn.bind(on_release=self.cliente_dropdown.open)
        self.cliente_dropdown.bind(on_select=self.selecionar_cliente)
        self.bl.add_widget(self.cliente_btn)

        self.pizza_label = Label(text='Selecione uma pizza:')
        self.bl.add_widget(self.pizza_label)

        self.pizza_dropdown = DropDown()
        self.carregar_pizzas()
        self.pizza_btn = Button(text="Pizza", size_hint=(None, None), size=(200, 30), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.pizza_btn.bind(on_release=self.pizza_dropdown.open)
        self.pizza_dropdown.bind(on_select=self.selecionar_pizza)
        self.bl.add_widget(self.pizza_btn)

        # Opção de tamanho
        self.tamanho_label = Label(text='Selecione o tamanho:')
        self.bl.add_widget(self.tamanho_label)

        self.tamanho_dropdown = DropDown()
        self.carregar_tamanhos()
        self.tamanho_btn = Button(text="Tamanho", size_hint=(None, None), size=(200, 30), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.tamanho_btn.bind(on_release=self.tamanho_dropdown.open)
        self.tamanho_dropdown.bind(on_select=self.selecionar_tamanho)
        self.bl.add_widget(self.tamanho_btn)

        # Opção de quantidade
        self.quantidade_label = Label(text='Selecione a quantidade:')
        self.bl.add_widget(self.quantidade_label)

        self.quantidade_spinner = Spinner(
            text='1',
            values=['1', '2', '3', '4', '5'],
            size_hint=(None, None),
            size=(200, 30),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.bl.add_widget(self.quantidade_spinner)

        self.fazer_encomenda_btn = Button(text='Fazer Encomenda', size_hint_y=None, height=50)
        self.fazer_encomenda_btn.bind(on_release=self.fazer_encomenda)
        self.bl.add_widget(self.fazer_encomenda_btn)

        self.voltar_menu_btn = Button(text='Voltar ao Menu Inicial', size_hint_y=None, height=50)
        self.voltar_menu_btn.bind(on_release=self.voltar_menu_inicial)
        self.bl.add_widget(self.voltar_menu_btn)

    def carregar_clientes(self):
        self.cliente_dropdown.clear_widgets()

        r = requests.get('http://127.0.0.1:5000/clientes')
        if r.status_code == 200:
            clientes = r.json()
            for cliente in clientes:
                btn = Button(text=cliente["nome"], size_hint_y=None, height=30)
                btn.bind(on_release=lambda btn, cliente=cliente: self.selecionar_cliente(btn, cliente["nome"]))
                btn.cliente_id = cliente["id_cliente"]
                self.cliente_dropdown.add_widget(btn)

                """
                A parte lambda btn, pizza=pizza: define uma função anônima com dois parâmetros: btn e pizza. 
                O parâmetro btn representa o próprio botão que foi pressionado e solto, 
                enquanto pizza é um parâmetro opcional que é atribuído
                ao valor da variável pizza no momento em que a função é definida.

                A função selecionar_pizza(btn, pizza) 
                é chamada com os argumentos btn e pizza (o valor atual da variável pizza).
                """

    def selecionar_cliente(self, instance, cliente):
        self.cliente_btn.text = cliente
        self.cliente_id = instance.cliente_id
        self.cliente_dropdown.dismiss()  # Recolhe o menu suspenso


    def carregar_pizzas(self):
        self.pizza_dropdown.clear_widgets()

        r = requests.get('http://127.0.0.1:5000/pizzas')
        if r.status_code == 200:
            pizzas = r.json()["pizzas"]  # Ajuste na estrutura dos dados
            for pizza in pizzas:
                nome_pizza = pizza["nome"]
                btn = Button(text=nome_pizza, size_hint_y=None, height=30)
                btn.bind(on_release=lambda btn, pizza=pizza: self.selecionar_pizza(btn, pizza))
                self.pizza_dropdown.add_widget(btn)

    def selecionar_pizza(self, instance, pizza):
        nome_pizza = pizza["nome"]
        self.pizza_btn.text = nome_pizza
        self.pizza_id = nome_pizza
        self.pizza_dropdown.dismiss()  # Recolhe o menu suspenso

    def carregar_tamanhos(self):
        self.tamanho_dropdown.clear_widgets()

        tamanhos = ['Pequeno', 'Médio', 'Grande']  # Exemplo de tamanhos disponíveis
        for tamanho in tamanhos:
            btn = Button(text=tamanho, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn, tamanho=tamanho: self.selecionar_tamanho(btn, tamanho))
            self.tamanho_dropdown.add_widget(btn)

    def selecionar_tamanho(self, instance, tamanho):
        self.tamanho_btn.text = tamanho
        self.tamanho_dropdown.dismiss()  # Recolhe o menu suspenso

    
    def fazer_encomenda(self, *args):
        cliente = self.cliente_btn.text
        pizza = self.pizza_btn.text
        quantidade = self.quantidade_spinner.text
        tamanho = self.tamanho_btn.text

        if cliente != 'Cliente' and pizza != 'Pizza':
            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            encomenda = {
                "data_hora": data_hora,
                "id_cliente": self.cliente_id,
                "nome_pizza": pizza,
                "quantidade": quantidade,  
                "tamanho": tamanho 
            }
            r = requests.post('http://127.0.0.1:5000/encomendas', json=encomenda)
            if r.status_code == 201:
                self.fazer_encomenda_btn.text = 'Encomenda adicionada!'

            else:
                print("Erro ao fazer a encomenda.")
        else:
            print("Selecione um cliente e uma pizza para fazer a encomenda.")


    def voltar_menu_inicial(self, *args):
        self.manager.current = 'menu_principal'


class MyApp(App):
    def build(self):
        return NovaEncomendaForm()

if __name__ == '__main__':
    MyApp().run()




