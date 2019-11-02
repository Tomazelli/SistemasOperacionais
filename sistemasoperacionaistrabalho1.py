##      print("Aluno: Felipe Tomazelli Crespo")
##	print("DRE: 113203901")
##	print("Trabalho 1 de Sistemas operacionais (MAB-366) -- 2019/2")
##	print("Algoritmos de substituição de páginas")
##	print("Professora Silvana Rosseto")

import sys

numeroDeArgumentos = len(sys.argv)
listaDeArgumentos = str(sys.argv)

global nomeDoArquivo
#nomeDoArquivo = listaDeArgumentos[2]
nomeDoArquivo = "referencias.txt"

global quantosQuadrosTem
#quantosQuadrosTem = int(listaDeArgumentos[1])
quantosQuadrosTem = 4

def FIFO(quantidadeDeQuadros, referencias):
    falhas = 0
    quadros = []

    proximoASair = 0

    alterarQuadros = True
        #preenchendo os primeiros quadros
    for x in range(quantidadeDeQuadros):
        quadros.append(referencias[x])
        falhas = falhas + 1

    #preenchendo o resto dos quadros
    for x in range(quantidadeDeQuadros, quantidadeDeReferencias):

        #verificando se o valor esta presente nos quadros
        for y in range(quantidadeDeQuadros):
            if (referencias[x] == quadros[y]):
                alterarQuadros = False

        #caso precise alterar
        if alterarQuadros:
            quadros[proximoASair] = referencias[x]
            proximoASair = proximoASair + 1
            proximoASair = proximoASair % quantidadeDeQuadros
            falhas = falhas + 1
                
        #resetando a flag
        alterarQuadros = True
                    
    return falhas

def OPT(quantidadeDeQuadros, referencias):
    falhas = 0
    quadros = []
    #primeiro valor casa, segundo valor distancia
    trocar = [0,0]

    alterarQuadros = True

    #preenchendo os primeiros quadros
    for x in range(quantidadeDeQuadros):
        quadros.append(referencias[x])
        falhas = falhas + 1


    #preenchendo o resto dos quadros
    for x in range(quantidadeDeQuadros, quantidadeDeReferencias):

        #verificando se o valor esta presente nos quadros
        for y in range(quantidadeDeQuadros):
            if (referencias[x] == quadros[y]):
                alterarQuadros = False


        #caso precise alterar
        if alterarQuadros:
            
            #para cada quadro
            for quadroAtual in range(quantidadeDeQuadros):
                #varrer ate o final
                for posicaoNaListaDeReferencias in range(x,quantidadeDeReferencias):

                    #caso não exista mais ocorrencias
                    if posicaoNaListaDeReferencias + 1 == quantidadeDeReferencias:
                        if quadros[quadroAtual] != referencias[quantidadeDeReferencias-1]:
                            trocar[1] = posicaoNaListaDeReferencias + 2
                            trocar[0] = quadroAtual

                    
                    #procurando um valor igual ao do quadro

                    if quadros[quadroAtual] == referencias[posicaoNaListaDeReferencias]:
                        #se a distancia entre eles for maior que a maior distancia atual
                        if posicaoNaListaDeReferencias > trocar[1]:
                            #ela se torna a maior distancia atual
                            trocar[1] = posicaoNaListaDeReferencias
                            trocar[0] = quadroAtual
                        break

            #Efetua a troca e reseta a distancia
            quadros[trocar[0]] = referencias[x]
            trocar[1] = 0
                        
            falhas = falhas + 1

        alterarQuadros = True                        
            
    return falhas


def LRU(quantidadeDeQuadros, referencias):
    falhas = 0
    quadros = []

    #primeiro valor casa, segundo valor distancia
    trocar = [0,quantidadeDeReferencias]

    alterarQuadros = True
    
    #preenchendo os primeiros quadros
    for x in range(quantidadeDeQuadros):
        quadros.append(referencias[x])
        falhas = falhas + 1

    #preenchendo o resto dos quadros
    for x in range(quantidadeDeQuadros, quantidadeDeReferencias):

        #verificando se o valor esta presente nos quadros
        for y in range(quantidadeDeQuadros):
            if (referencias[x] == quadros[y]):
                alterarQuadros = False

        #caso precise alterar
        if alterarQuadros:
            
            #para cada quadro
            for quadroAtual in range(quantidadeDeQuadros):
                for posicaoNaListaDeReferencias in range(x, -1, -1):

                    #caso não exista mais ocorrencias
                    if posicaoNaListaDeReferencias - 1 == quantidadeDeReferencias:
                        if quadros[quadroAtual] != referencias[0]:
                            trocar[1] = quantidadeDeReferencias + 1
                            trocar[0] = quadroAtual

                    
                    #procurando um valor igual ao do quadro
                    if quadros[quadroAtual] == referencias[posicaoNaListaDeReferencias]:
                        #se a distancia entre eles for maior que a maior distancia atual
                        if posicaoNaListaDeReferencias < trocar[1]:
                            #ela se torna a maior distancia atual
                            trocar[1] = posicaoNaListaDeReferencias
                            trocar[0] = quadroAtual
                        break 

            #Efetua a troca e reseta a distancia
            quadros[trocar[0]] = referencias[x]
            trocar[1] = quantidadeDeReferencias + 1
                        
            falhas = falhas + 1

        alterarQuadros = True
            
    return falhas
    


def main():

    referencias = []
    quantidadeDeQuadros = quantosQuadrosTem
    
    global quantidadeDeReferencias
    quantidadeDeReferencias = 0

    #print("processando...")
    f=open(nomeDoArquivo, "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
	#removendo o /n ao final
            referencias.append(int(x.strip()))
            #print("(debug) ", x.strip())
            #incrementando a quantidade de referencias
            quantidadeDeReferencias = quantidadeDeReferencias + 1
            #print("(debug) ", quantidadeDeReferencias)
            
    #print("processando...")


    #caso tenha menos referencias do que a quantidade de quadros, nao haveram falhas de pagina
    if quantidadeDeQuadros < quantidadeDeReferencias:
        resultadoFifo = FIFO(quantidadeDeQuadros, referencias)
        #print("processando...")

        resultadoOPT = OPT(quantidadeDeQuadros, referencias)

        #print("processando...")

        resultadoLRU = LRU(quantidadeDeQuadros, referencias)
        #print("processando...")

    else:
        resultadoFifo = quantidadeDeReferencias
        resultadoOPT = quantidadeDeReferencias
        resultadoLRU = quantidadeDeReferencias

    print(quantidadeDeQuadros, " quadros, ", quantidadeDeReferencias ," refs: FIFO:", resultadoFifo ," PFs, LRU: ", resultadoLRU ," PFs, OPT: ", resultadoOPT ," PFs\n")
    input()

    

if __name__ == '__main__':
	main()
