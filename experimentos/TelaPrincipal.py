import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
matplotlib.use('TkAgg')
from DesenhistaDeGrafos import DesenhistaDeGrafos
from GeradorDeGrafos import GeradorDeGrafos
from Rotulo import Rotulo
from GeradorDeHeuristica import GeradorDeHeuristica
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from DescritorDeGrafos import Descritor_de_grafos

import Tkinter as Tk

class TelaPrincipal:
    container_superior = None
    container_esquerdo = None
    container_inferior = None
    container_direito = None
    canvas = None

    edt_folhas_k = -1
    edt_folhas_l = -1
    edt_diametro = -1

    str_conectividade_algebrica_original = None
    str_nova_conectividade_algebrica = None
    str_melhor_aresta = None
    descritor_de_grafos = Descritor_de_grafos()

    def __init__(self, master):
        self.master = master
        self.inicializar_componentes()

    def inicializar_componentes(self):
        self.inicializar_container_superior()
        self.inicializar_container_inferior()
        self.inicalizar_container_esquerdo()
        self.inicializar_container_direito()
        self.btn_gerar_grafo_action()

    def inicializar_container_superior(self):
        self.container_superior = Tk.Frame(master=self.master, height=16, width=16)
        self.container_superior.pack()
        self.lbl_informe_os_dados = Tk.Label(self.container_superior, text="Informe os dados do grafo")
        self.lbl_folhas_k = Tk.Label(self.container_superior, text="Folhas \"K \":")
        self.lbl_folhas_l = Tk.Label(self.container_superior, text="Folhas \"L \":")
        self.lbl_diametro = Tk.Label(self.container_superior, text="Diametro:")
        self.edt_folhas_k = Tk.Spinbox(master=self.container_superior, from_=1, to=60, width = 2)
        self.edt_folhas_l = Tk.Spinbox(master=self.container_superior, from_=1, to=60, width = 2)
        self.edt_diametro = Tk.Spinbox(master=self.container_superior, from_=3, to=60, width = 2)
        self.lbl_informe_os_dados.pack(side=Tk.TOP)
        self.lbl_folhas_k.pack(side = Tk.LEFT)
        self.edt_folhas_k.pack(side = Tk.LEFT)
        self.lbl_folhas_l.pack(side = Tk.LEFT)
        self.edt_folhas_l.pack(side = Tk.LEFT)
        self.lbl_diametro.pack(side = Tk.LEFT)
        self.edt_diametro.pack(side = Tk.LEFT)
        self.btn_gerar_grafo = Tk.Button(master=self.container_superior, text='Gerar Grafo',
                                         command=self.btn_gerar_grafo_action, height=1, pady = 1)
        self.btn_gerar_grafo.pack(side=Tk.LEFT)
        self.btn_executar = Tk.Button(master=self.container_superior, text='Gerar Grafo',
                                         command=self.btn_gerar_grafo_action, height=1, pady = 1)
        self.btn_gerar_grafo.pack(side=Tk.LEFT)


    def inicalizar_container_esquerdo(self):
        figura = self.gerar_figura_a_partir_de_grafo(GeradorDeGrafos().gerar_arvore_t(3, 4, 3))
        self.canvas = FigureCanvasTkAgg(figura, master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)


    def inicializar_container_direito(self):
        self.container_direito = Tk.Frame(master=self.master, height=16, width=16)
        self.container_direito.pack(side=Tk.RIGHT)
        self.str_conectividade_algebrica = Tk.StringVar()
        self.str_melhor_aresta = Tk.StringVar()
        self.lbl_propriedades                           = Rotulo(self.container_direito, "Propriedades do Grafo:", Tk.TOP)
        self.ctn_conectividade_algebrica_original       = Tk.Frame(master=self.container_direito)
        self.lbl_conectividade_algebrica_original       = Rotulo(self.ctn_conectividade_algebrica_original, "Conectividade Algebrica:", Tk.LEFT)
        self.lbl_valor_conectividade_algebrica_original = Rotulo(self.ctn_conectividade_algebrica_original, "-", Tk.LEFT)
        self.ctn_nova_conectividade_algebrica           = Tk.Frame(master=self.container_direito)
        self.lbl_nova_conectividade_algebrica           = Rotulo(self.ctn_nova_conectividade_algebrica, "Nova Conectividade Algebrica:", Tk.LEFT)
        self.lbl_valor_nova_conectividade_algebrica     = Rotulo(self.ctn_nova_conectividade_algebrica, "-", Tk.LEFT)

        self.ctn_conectividade_algebrica_original.pack(side=Tk.TOP)
        self.ctn_nova_conectividade_algebrica.pack(side=Tk.TOP)
        self.ctn_melhor_aresta                 = Tk.Frame(master=self.container_direito)
        self.lbl_melhor_aresta                 = Rotulo(self.ctn_melhor_aresta, "Melhor Aresta:", Tk.LEFT)
        self.lbl_valor_melhor_aresta           = Rotulo(self.ctn_melhor_aresta, "9-1", Tk.LEFT)
        self.ctn_melhor_aresta.pack(side=Tk.TOP)

        self.int_gerar_complemento = Tk.IntVar()
        self.chk_gerar_complemento = Tk.Checkbutton(self.container_direito, text="Complemento", variable=self.int_gerar_complemento)
        self.chk_gerar_complemento.pack()

        self.ctn_botao_sair = Tk.Frame(master=self.container_direito)
        self.button = Tk.Button(master=self.ctn_botao_sair, text='Sair', command=self.btn_sair_action)
        self.button.pack(side=Tk.BOTTOM)
        self.ctn_botao_sair.pack(side=Tk.TOP)

    def inicializar_container_inferior(self):
        self.container_inferior = Tk.Frame(master=self.master, height=16, width=16)
        self.container_inferior.pack(side=Tk.BOTTOM)
        self.mmo_informacoes_do_grafo_original = Tk.Text(master=self.container_inferior, height=12, width = 70)
        self.mmo_informacoes_do_grafo_original.pack(side=Tk.LEFT)
        self.mmo_informacoes_do_novo_grafo = Tk.Text(master=self.container_inferior, height=12, width=70)
        self.mmo_informacoes_do_novo_grafo.pack(side=Tk.LEFT)

    def gerar_figura_a_partir_de_grafo(self, grafo, arestas_a_ressaltar = None):
        if arestas_a_ressaltar == None:
            arestas_a_ressaltar = []
        return DesenhistaDeGrafos().obter_grafo_plotado(grafo, arestas_a_ressaltar)


    def btn_gerar_grafo_action(self):
        k = int(self.edt_folhas_k.get().strip())
        l = int(self.edt_folhas_l.get().strip())
        d = int(self.edt_diametro.get().strip())
        if self.int_gerar_complemento.get() == 0:
          grafo = GeradorDeGrafos().gerar_arvore_t(k, l, d)
        else:
          grafo = GeradorDeGrafos().gerar_arvore_t(k, l, d).obter_grafo_complemento()

        self.canvas.figure.clf()

        self.lbl_valor_conectividade_algebrica_original.alterar_texto(grafo.obter_conectividade_algebrica())
        gerador_de_heuristica = GeradorDeHeuristica(AlgoritmoHeuristicaDeForcaBruta())
        melhor_aresta_fb = gerador_de_heuristica.estimar_aresta_de_maior_aumento_da_conectividade_algebrica(grafo)
        self.lbl_valor_melhor_aresta.alterar_texto(str(  (melhor_aresta_fb[0]+1, melhor_aresta_fb[1]+1) ))

        novo_grafo = grafo.copia().adicionar_aresta(melhor_aresta_fb)

        self.lbl_valor_nova_conectividade_algebrica.alterar_texto(novo_grafo.obter_conectividade_algebrica())
        self.canvas.figure = self.gerar_figura_a_partir_de_grafo(novo_grafo, [melhor_aresta_fb])
        #self.canvas.figure = self.gerar_figura_a_partir_de_grafo(grafo.obter_grafo_complemento(), [melhor_aresta_fb])
        #self.canvas.figure = self.gerar_figura_a_partir_de_grafo(grafo.obter_grafo_complemento())#, [melhor_aresta_fb])
        self.canvas.show()
        self.canvas.get_tk_widget().pack()

        dados_originais = self.descritor_de_grafos.obter_lista_de_informacoes_do_grafo(grafo)
        novos_dados     = self.descritor_de_grafos.obter_lista_de_informacoes_do_grafo(novo_grafo)

        self.mmo_informacoes_do_grafo_original.delete("1.0", Tk.END)
        self.mmo_informacoes_do_grafo_original.insert(Tk.END, "Grafo Original: " + grafo.obter_nome() + '\n\n')
        self.mmo_informacoes_do_grafo_original.insert(Tk.END, dados_originais + '\n\n')
        self.mmo_informacoes_do_novo_grafo.delete("1.0", Tk.END)
        self.mmo_informacoes_do_novo_grafo.insert(Tk.END, "Novo Grafo: " + novo_grafo.obter_nome() + '\n\n')
        self.mmo_informacoes_do_novo_grafo.insert(Tk.END, novos_dados + '\n\n')


    def btn_sair_action(self):
        root.quit()
        root.destroy()


root = Tk.Tk()
#root.state('zoomed')
root.wm_title("Gerador de Arvores")

tela_principal = TelaPrincipal(root)
root.protocol("WM_DELETE_WINDOW", tela_principal.btn_sair_action)

Tk.mainloop()
