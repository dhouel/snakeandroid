import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.button import Button
from kivy.clock import Clock
from random import randint
import math

tamanho_segmento = 20
velocidade = 0.2

class SnakeGame(Widget):
    pontos = NumericProperty(0)
    maior_pontuacao = NumericProperty(0)
    direcao = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.inicializar_jogo()

    def inicializar_jogo(self):
        self.cobra = [(60, 60), (40, 60), (20, 60)]
        self.direcao = [0, 0]
        self.pontos = 0
        self.novo_tesouro()
        Clock.schedule_interval(self.mover_cobra, velocidade)

    def novo_tesouro(self):
        self.ids.tesouro.pos = (
            randint(0, (self.width - tamanho_segmento) // tamanho_segmento) * tamanho_segmento,
            randint(0, (self.height - tamanho_segmento) // tamanho_segmento) * tamanho_segmento
        )

    def mover_cobra(self, dt):
        if self.direcao == [0, 0]:
            return
        x, y = self.cobra[-1]
        dx, dy = self.direcao
        nova_posicao = (x + dx * tamanho_segmento, y + dy * tamanho_segmento)
        if not (0 <= nova_posicao[0] < self.width and 0 <= nova_posicao[1] < self.height) or nova_posicao in self.cobra:
            self.fim_de_jogo()
            return
        self.cobra.append(nova_posicao)
        self.cobra.pop(0)
        self.atualizar_seguimentos()

        if self.colisao(self.ids.seg3, self.ids.tesouro):
            self.pontos += 1
            self.novo_tesouro()

    def atualizar_seguimentos(self):
        for i, pos in enumerate(self.cobra):
            self.ids[f'seg{i+1}'].pos = pos

    def fim_de_jogo(self):
        if self.pontos > self.maior_pontuacao:
            self.maior_pontuacao = self.pontos
        Clock.unschedule(self.mover_cobra)
        self.inicializar_jogo()

    def colisao(self, cobra, tesouro):
        x_cobra = cobra.center_x
        y_cobra = cobra.center_y
        x_tesouro = tesouro.center_x
        y_tesouro = tesouro.center_y
        distancia = math.sqrt((x_cobra - x_tesouro) ** 2 + (y_cobra - y_tesouro) ** 2)
        return distancia < tamanho_segmento

class SnakeApp(App):
    def build(self):
        game = SnakeGame()

        # Adicionando botões de controle
        btn_up = Button(text="UP", size_hint=(None, None), size=(100, 50), pos=(100, 200))
        btn_down = Button(text="DOWN", size_hint=(None, None), size=(100, 50), pos=(100, 100))
        btn_left = Button(text="LEFT", size_hint=(None, None), size=(100, 50), pos=(50, 150))
        btn_right = Button(text="RIGHT", size_hint=(None, None), size=(100, 50), pos=(150, 150))

        btn_up.bind(on_press=lambda x: setattr(game, 'direcao', [0, 1]))
        btn_down.bind(on_press=lambda x: setattr(game, 'direcao', [0, -1]))
        btn_left.bind(on_press=lambda x: setattr(game, 'direcao', [-1, 0]))
        btn_right.bind(on_press=lambda x: setattr(game, 'direcao', [1, 0]))

        game.add_widget(btn_up)
        game.add_widget(btn_down)
        game.add_widget(btn_left)
        game.add_widget(btn_right)

        return game

if __name__ == '__main__':
    SnakeApp().run()
