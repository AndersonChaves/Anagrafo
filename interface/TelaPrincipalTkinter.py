# *-* coding=utf-8 *-*
import matplotlib
matplotlib.use('TkAgg')
from DesenhistaDeGrafosNovo import DesenhistaDeGrafos
from GeradorDeGrafos import GeradorDeGrafos
from Rotulo import Rotulo
from GeradorDeHeuristica import GeradorDeHeuristica
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta

import Tkinter as Tk

from Botao import Botao
from EditComLabel import EditComLabel
from Canvas import Canvas

class TelaPrincipalTkinter:
    raiz = None
    grafo_exibido = GeradorDeGrafos().gerar_double_broom(1, 12, 8)

    def __init__(self, raiz):
        self.raiz = raiz
        self.inicializar_componentes()

    def inicializar_componentes(self):
        self.inicializar_container_superior()
        #self.inicializar_container_inferior()
        #self.inicalizar_container_esquerdo()
        #self.inicializar_container_direito()
        #self.btn_gerar_grafo_action()

    def inicializar_container_superior(self):
        self.inicializar_container_parametros_de_entrada()
        self.inicalizar_container_visualizacao_do_grafo()

    def inicializar_container_parametros_de_entrada(self):
        self.container_parametros_de_entrada = Tk.Frame(master=self.raiz, height=16, width=16)
        self.container_parametros_de_entrada.pack(side=Tk.LEFT)
        self.inicializar_componentes_de_entrada()

    def inicializar_componentes_de_entrada(self):
        self.lbl_parametros  = Tk.Label(self.container_parametros_de_entrada, text="Parâmetros")
        self.lbl_parametros.pack(side=Tk.TOP)
        self.edit_ordem      = EditComLabel(self.container_parametros_de_entrada, "Ordem (n):", minimo=6)
        self.edit_diametro   = EditComLabel(self.container_parametros_de_entrada, "Diâmetro (d):", minimo=3)
        self.edit_folhas     = EditComLabel(self.container_parametros_de_entrada, "Folhas (k):", minimo=1)
        self.btn_gerar_grafo = Botao(self.container_parametros_de_entrada, "Gerar Grafo", self.btn_gerar_grafo_action)

    def inicalizar_container_visualizacao_do_grafo(self):
        self.inicializar_primeiro_canvas_de_visualizacao()
        self.inicializar_segundo_canvas_de_visualizacao()

    def inicializar_primeiro_canvas_de_visualizacao(self):
        figura = self.gerar_figura_a_partir_de_grafo(self.grafo_exibido)
        self.canvas_espectral = Canvas(self.raiz, figura)

    def inicializar_segundo_canvas_de_visualizacao(self):
        figura = self.gerar_figura_a_partir_de_grafo(self.grafo_exibido,
                                                      tipo_de_particionamento="Espectral")
        self.canvas_isoperimetrico = Canvas(self.raiz, figura)

    def atualizar_canvas(self):
        self.canvas_espectral.atualizar_figura(self.gerar_figura_a_partir_de_grafo(self.grafo_exibido,
                                                      tipo_de_particionamento="Espectral"))
        self.canvas_isoperimetrico.atualizar_figura(self.gerar_figura_a_partir_de_grafo(self.grafo_exibido))

    def inicializar_container_direito(self):
        self.container_direito = Tk.Frame(master=self.raiz, height=16, width=16)
        self.container_direito.pack(side=Tk.RIGHT)
        self.str_conectividade_algebrica = Tk.StringVar()
        self.str_melhor_aresta = Tk.StringVar()
        self.lbl_propriedades = Rotulo(self.container_direito, "Propriedades do Grafo:", Tk.TOP)
        self.ctn_conectividade_algebrica_original = Tk.Frame(master=self.container_direito)
        self.lbl_conectividade_algebrica_original = Rotulo(self.ctn_conectividade_algebrica_original,
                                                           "Conectividade Algebrica:", Tk.LEFT)
        self.lbl_valor_conectividade_algebrica_original = Rotulo(self.ctn_conectividade_algebrica_original, "-",
                                                                 Tk.LEFT)
        self.ctn_nova_conectividade_algebrica = Tk.Frame(master=self.container_direito)
        self.lbl_nova_conectividade_algebrica = Rotulo(self.ctn_nova_conectividade_algebrica,
                                                       "Nova Conectividade Algebrica:", Tk.LEFT)
        self.lbl_valor_nova_conectividade_algebrica = Rotulo(self.ctn_nova_conectividade_algebrica, "-", Tk.LEFT)

        self.ctn_conectividade_algebrica_original.pack(side=Tk.TOP)
        self.ctn_nova_conectividade_algebrica.pack(side=Tk.TOP)
        self.ctn_melhor_aresta = Tk.Frame(master=self.container_direito)
        self.lbl_melhor_aresta = Rotulo(self.ctn_melhor_aresta, "Melhor Aresta:", Tk.LEFT)
        self.lbl_valor_melhor_aresta = Rotulo(self.ctn_melhor_aresta, "9-1", Tk.LEFT)
        self.ctn_melhor_aresta.pack(side=Tk.TOP)

        self.int_gerar_complemento = Tk.IntVar()
        self.chk_gerar_complemento = Tk.Checkbutton(self.container_direito, text="Complemento",
                                                    variable=self.int_gerar_complemento)
        self.chk_gerar_complemento.pack()

        self.ctn_botao_sair = Tk.Frame(master=self.container_direito)
        self.button = Tk.Button(master=self.ctn_botao_sair, text='Sair', command=self.btn_sair_action)
        self.button.pack(side=Tk.BOTTOM)
        self.ctn_botao_sair.pack(side=Tk.TOP)

    def inicializar_container_inferior(self):
        self.container_inferior = Tk.Frame(master=self.raiz, height=16, width=16)
        self.container_inferior.pack(side=Tk.BOTTOM)
        self.mmo_informacoes_do_grafo_original = Tk.Text(master=self.container_inferior, height=12, width=70)
        self.mmo_informacoes_do_grafo_original.pack(side=Tk.LEFT)
        self.mmo_informacoes_do_novo_grafo = Tk.Text(master=self.container_inferior, height=12, width=70)
        self.mmo_informacoes_do_novo_grafo.pack(side=Tk.LEFT)

    def gerar_figura_a_partir_de_grafo(self, grafo, arestas_a_ressaltar=None, tipo_de_particionamento="Isoperimetrico"):
        if arestas_a_ressaltar == None:
            arestas_a_ressaltar = []
        desenhista = DesenhistaDeGrafos(grafo)
        if tipo_de_particionamento == "Isoperimetrico":
            desenhista.efetuar_particionamento_isoperimetrico()
        elif tipo_de_particionamento == "Espectral":
            desenhista.efetuar_particionamento_espectral()
        desenhista.adicionar_labels()
        return desenhista.obter_grafo_plotado()

    def btn_gerar_grafo_action(self):
        k = self.edit_ordem.obter_valor_como_inteiro()
        l = self.edit_diametro.obter_valor_como_inteiro()
        d = self.edit_folhas.obter_valor_como_inteiro()

        self.grafo_exibido = GeradorDeGrafos().gerar_double_broom(k, l, d)

        self.atualizar_canvas()

        #self.canvas_espectral.figure.clf()

        #self.lbl_valor_conectividade_algebrica_original.alterar_texto(grafo.obter_conectividade_algebrica())
        #gerador_de_heuristica = GeradorDeHeuristica(AlgoritmoHeuristicaDeForcaBruta())
        #melhor_aresta_fb = gerador_de_heuristica.estimar_aresta_de_maior_aumento_da_conectividade_algebrica(grafo)
        #self.lbl_valor_melhor_aresta.alterar_texto(str((melhor_aresta_fb[0] + 1, melhor_aresta_fb[1] + 1)))

        #novo_grafo = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(melhor_aresta_fb)

        #self.lbl_valor_nova_conectividade_algebrica.alterar_texto(novo_grafo.obter_conectividade_algebrica())
        #self.canvas_espectral.figure = self.gerar_figura_a_partir_de_grafo(novo_grafo, [melhor_aresta_fb])
        # self.canvas.figure = self.gerar_figura_a_partir_de_grafo(grafo.obter_grafo_complemento(), [melhor_aresta_fb])
        # self.canvas.figure = self.gerar_figura_a_partir_de_grafo(grafo.obter_grafo_complemento())#, [melhor_aresta_fb])
        #self.canvas_espectral.show()
        #self.canvas_espectral.get_tk_widget().pack()

        #self.mmo_informacoes_do_novo_grafo.insert(Tk.END, novos_dados + '\n\n')

    def btn_sair_action(self):
        self.raiz.quit()
        self.raiz.destroy()

#root = Tk.Tk()
# root.state('zoomed')
#root.wm_title("Gerador de Arvores")

#tela_principal = TelaPrincipal(root)
#root.protocol("WM_DELETE_WINDOW", tela_principal.btn_sair_action)

#Tk.mainloop()
