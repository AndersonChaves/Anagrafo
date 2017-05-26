import numpy
import os
import networkx as nx
import csv

class EscritorDeDados():
    def escrever_vetores_fiedler(self, listaDeGrafos, diretorio, nomeDoArquivo):
        F = []
        for grafo in listaDeGrafos:
            F.append(grafo.obter_vetor_fiedler())
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        arquivo = open(diretorio + "\\" + nomeDoArquivo, "w")
        for i in range(len(F)):
            arquivo.write("Vetor Fiedler do grafo: " + str(i + 1) + "\n")
            arquivo.write("Grafo: " + listaDeGrafos[i].obter_nome() + "\n")
            arquivo.write(str(F[i]))
            arquivo.write("\n\n")

    def escrever_matriz_laplaciana(self, listaDeGrafos, diretorio, nomeDoArquivo):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        arquivo = open(diretorio + "\\" + nomeDoArquivo, "w")
        i = 0
        for grafo in listaDeGrafos:
            laplaciana = nx.laplacian_matrix(grafo).A
            arquivo.write("Matriz Laplaciana do grafo: " + str(i + 1) + "\n")
            arquivo.write(str(laplaciana))

            arquivo.write("\n\nAutovalores: \n")
            eigenvalues, _ = numpy.linalg.eig(laplaciana)
            arquivo.write(str(eigenvalues))
            arquivo.write("\n\n\n")
            i = i + 1

    def escrever_tabela_de_dados_gerais(self, listaDeGrafos, diretorio, nomeDoArquivo):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        arquivo = open(diretorio + "\\" + nomeDoArquivo, "w")

        if not 'e1 - Pb' in listaDeGrafos[0].dicionarioDeDados: return

        print listaDeGrafos[0].categoria

        fieldnames = ['n','m','#E','#~E','G','#E1','#E2','e1 - a','e1 - b', 'e1 - Pa', 'e1 - Pb', 'L2 (G + e1)',\
                      'e2 - a', 'e2 - b', 'e2 - Pa', 'e2 - Pb', 'L2 (G + e2)','eph - a', 'eph - b', 'eph - Pa', \
                      'eph - Pb', 'L2 (G + eph)','L2(G + e1)-L2(G + eph)', 'L2(G + e2) - L2(G + eph)', 'rel', 'relPercentVerm']
        csvWriter = csv.DictWriter(arquivo, fieldnames)
        csvWriter.writeheader()
        for grafo in listaDeGrafos:
            particionamento = grafo.obter_particionamento_pelo_vetor_fiedler()
            grafo.dicionarioDeDados["rel"] = float(len(particionamento[0]))/float(len(particionamento[1]))
            grafo.dicionarioDeDados["relPercentVerm"] = float(len(particionamento[0])) / float(grafo.grafo_nx.order())
            dicionarioDeDados = grafo.dicionarioDeDados
            csvWriter.writerow(dicionarioDeDados)

    def escrever_tabela_em_arquivo_csv(self, tabela, nome_dos_campos, diretorio, nome_do_arquivo):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        arquivo = open(diretorio + "\\" + nome_do_arquivo, "wb")
        csv_writer = csv.DictWriter(arquivo, nome_dos_campos)
        csv_writer.writeheader()
        for dicionario in tabela:
            csv_writer.writerow(dicionario)

    def escrever_objeto_tabela_em_arquivo_csv(self, objeto_tabela, diretorio):
        tabela = []
        campos = objeto_tabela.obter_campos()
        for linha in objeto_tabela.linhas:
            i = 0
            dicionario = {}
            for campo in campos:
                dicionario[campo] = linha[i]
                i += 1
            tabela.append(dicionario)

        self.escrever_tabela_em_arquivo_csv(tabela, campos, diretorio, objeto_tabela.obter_titulo() + ".csv")

    def escrever_texto_em_arquivo_txt(self, texto, nome_do_arquivo, diretorio):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        arquivo = open(diretorio + "\\" + nome_do_arquivo, "w")
        arquivo.write(texto)
        arquivo.close()
