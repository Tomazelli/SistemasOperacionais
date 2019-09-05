import queue
from queue import PriorityQueue
import heapq

def FCFS(qtdTarefas, ingressos, duracoes, prioridades):

	#trocas de contexto
	trocasDeContexto = -1
	#tempo
	tempoTotal = 0
	#soma do tempo do processo atual com os que ja terminaram para encontrar o termino dos processos
	terminoTotal = 0
	esperaTotal = 0
	for x in range(0,qtdTarefas):
		# calculando o tempo que cada elemento esperou
		esperaTotal = esperaTotal + terminoTotal - ingressos[x]

		# uma tarefa so comeca apos a anterior terminar, entao acumula os tempos totais mais a duracao da atual
		terminoTotal = terminoTotal + duracoes[x]

		tempoTotal = tempoTotal + terminoTotal - ingressos[x]

		trocasDeContexto = trocasDeContexto + 1

	tempoMedioExecucaoFCFS = tempoTotal / qtdTarefas

	tempoMedioEsperaFCFS = esperaTotal / qtdTarefas

	##print("tempo medio de execucao escalonamento FCFS: ", tempoMedioExecucaoFCFS)
	##print("tempo medio de espera escalonamento FCFS: ", tempoMedioEsperaFCFS)
	##print("trocas de contexto FCFS: ", trocasDeContexto)

	return tempoMedioExecucaoFCFS, tempoMedioEsperaFCFS, trocasDeContexto, tempoTotal

def RR(qtdTarefas, ingressos, duracoes, prioridades):


	trocasDeContexto = -1
	# tempo de chaveamento
	roundrobinAtual = 0
	roundrobinMax = 2

	# tempo total de execucao
	tempoTotal = 0
	for x in duracoes:
		tempoTotal = tempoTotal + x

	#fila de execucao
	fila = queue.Queue()

	#se alguem esta em execucao
	execucao = False
	#quem esta em execucao
	executando = -1

	tempoExecutadoDeCadaTarefa = []
	tempoTerminoDeCadaTarefa = []
	tempoEsperaDeCadaTarefa = []

	#lista contendo o tempo de cada tarefa
	for x in range(0,qtdTarefas):
		#para cada
		tempoExecutadoDeCadaTarefa.append(x)
		tempoTerminoDeCadaTarefa.append(x)
		tempoEsperaDeCadaTarefa.append(x)
		tempoExecutadoDeCadaTarefa[x] = 0
		tempoTerminoDeCadaTarefa[x] = 0
		tempoEsperaDeCadaTarefa[x] = 0
		##print("(debug) ", tempoExecutadoDeCadaTarefa, x)

	#passando o tempo 	
	for x in range(0,tempoTotal):
		for y in range(0,qtdTarefas):
			# varrendo se alguem comecou no tempo atual
			if ingressos[y]==x:
				fila.put(y)
				##print("(debug) a tarefa ", y, "foi colocada na fila em ", x, "segundos")

		# colocando alguem em execucao
		if not execucao:
			if not fila.empty():
				executando = fila.get()
				trocasDeContexto = trocasDeContexto + 1
				execucao = True
				##print("(debug) executando a tarefa ", executando)


		# verificando se o tempo de chaveamento foi atingido
		if roundrobinAtual == roundrobinMax:
			roundrobinAtual = 0
			fila.put(executando)
			if not fila.empty():
				executando = fila.get()
				trocasDeContexto = trocasDeContexto + 1
				##print("(debug) chaveamento por round robin para a tarefa ", executando)
			##print("(debug) round robin resetado")

		#passando 1 segundo
		tempoExecutadoDeCadaTarefa[executando] = tempoExecutadoDeCadaTarefa[executando] + 1

		#atualizando tempos de espera
		for y in range(0,qtdTarefas):
			if y != executando and ingressos[y] <= x and tempoTerminoDeCadaTarefa[y] == 0:
				tempoEsperaDeCadaTarefa[y] = tempoEsperaDeCadaTarefa[y] + 1


		# atualizando chaveamento e se a tarefa terminou naturalmente

		##print("(debug) executando a tarefa", executando, "em ", x + 1, "segundos")
		if duracoes[executando] - tempoExecutadoDeCadaTarefa[executando] != 0:			
			roundrobinAtual = roundrobinAtual + 1
			##print("(debug) a tarefa ", executando, "teve seu tempo de execucao incrementado, total = ", tempoExecutadoDeCadaTarefa[executando])

		# caso a tarefa em execucao tenha atingido o seu tempo total de execucao, a proxima sera colocada em execucao
		else:
			tempoTerminoDeCadaTarefa[executando] = x + 1
			##print("(debug) tempo de termino da tarefa ", executando, " ", tempoTerminoDeCadaTarefa[executando])

			execucao = False
			roundrobinAtual = 0

		

	tempoTotal = 0
	esperaTotal = 0

	for x in range(0,qtdTarefas):
		tempoTotal = tempoTotal + tempoTerminoDeCadaTarefa[x] - ingressos[x]
		esperaTotal = esperaTotal + tempoEsperaDeCadaTarefa[x]
		##print("(debug) ", x)
		##print("(debug) ", tempoTotal)
		##print("(debug) ", tempoEsperaDeCadaTarefa[x])
		##print("(debug) ", esperaTotal)


	tempoMedioExecucaoRR = tempoTotal / qtdTarefas

	tempoMedioEsperaRR = esperaTotal / qtdTarefas

	##print("tempo medio de execucao escalonamento RR: ", tempoMedioExecucaoRR)
	##print("tempo medio de espera escalonamento RR: ", tempoMedioEsperaRR)
	##print("trocas de contexto RR: ", trocasDeContexto)

	return tempoMedioExecucaoRR, tempoMedioEsperaRR, trocasDeContexto, tempoTotal

#[0] = ingressos // [1] = duracao // [2] = prioridades
def SJF(qtdTarefas, duracoes, todasAsTarefasPorDuracao):

	filaHeap = []

	trocasDeContexto = -1

	# tempo total de execucao
	tempoTotal = 0
	for x in duracoes:
		tempoTotal = tempoTotal + x


	#se alguem esta em execucao
	execucao = False
	#quem esta em execucao
	executando = -1

	tempoExecutadoDeCadaTarefa = []
	tempoTerminoDeCadaTarefa = []
	tempoEsperaDeCadaTarefa = []

	#lista contendo o tempo de cada tarefa
	for x in range(0,qtdTarefas):
		#para cada
		tempoExecutadoDeCadaTarefa.append(x)
		tempoTerminoDeCadaTarefa.append(x)
		tempoEsperaDeCadaTarefa.append(x)
		tempoExecutadoDeCadaTarefa[x] = 0
		tempoTerminoDeCadaTarefa[x] = 0
		tempoEsperaDeCadaTarefa[x] = 0
		##print("(debug) ", tempoExecutadoDeCadaTarefa, x)

	#passando o tempo 	
	for x in range(0,tempoTotal):
		for y in range(0,qtdTarefas):
			if todasAsTarefasPorDuracao[y][0]==x:
				#organizando pela duracao uma fila de todas as tarefas que ja tiveram seu tempo de inicio
				heapq.heappush(filaHeap,(todasAsTarefasPorDuracao[y][1],y))
				##print("(debug) duracao ", todasAsTarefasPorDuracao[y][1])


		#pegando o proximo a ser executado
		if not execucao:
			if filaHeap:
				# executando a tarefa y
				executando = heapq.heappop(filaHeap)[1]
				trocasDeContexto = trocasDeContexto + 1
				execucao = True
				##print("(debug) executando a tarefa ", executando, "em ",x, " segundos")


		#aumentando o tempo executado da tarefa y
		tempoExecutadoDeCadaTarefa[executando] = tempoExecutadoDeCadaTarefa[executando] + 1

		#atualizando tempos de espera
		for y in range(0,qtdTarefas):
			if y != executando and todasAsTarefasPorDuracao[y][0] <= x and tempoTerminoDeCadaTarefa[y] == 0:
				tempoEsperaDeCadaTarefa[y] = tempoEsperaDeCadaTarefa[y] + 1

		if todasAsTarefasPorDuracao[executando][1] - tempoExecutadoDeCadaTarefa[executando] == 0:
			tempoTerminoDeCadaTarefa[executando] = x + 1
			##print("(debug) tempo de termino da tarefa ", executando, " ", tempoTerminoDeCadaTarefa[executando])

			execucao = False

	tempoTotal = 0
	esperaTotal = 0

	for x in range(0,qtdTarefas):
		tempoTotal = tempoTotal + tempoTerminoDeCadaTarefa[x] - todasAsTarefasPorDuracao[x][0]
		esperaTotal = esperaTotal + tempoEsperaDeCadaTarefa[x]
		##print("(debug) ", x)
		##print("(debug) ", tempoTotal)
		##print("(debug) ", tempoEsperaDeCadaTarefa[x])
		##print("(debug) ", esperaTotal)


	tempoMedioExecucaoSJF = tempoTotal / qtdTarefas

	tempoMedioEsperaSJF = esperaTotal / qtdTarefas

	##print("tempo medio de execucao escalonamento SJF: ", tempoMedioExecucaoSJF)
	##print("tempo medio de espera escalonamento SJF: ", tempoMedioEsperaSJF)
	##print("trocas de contexto SJF: ", trocasDeContexto)


	return tempoMedioExecucaoSJF, tempoMedioEsperaSJF, trocasDeContexto, tempoTotal



#[0] = ingressos // [1] = duracao // [2] = prioridades
def SRTF(qtdTarefas, duracoes, todasAsTarefasPorDuracao):

	trocasDeContexto = -1


	##print("(debug) todas as tarefas por duracao: ", todasAsTarefasPorDuracao)
	filaHeap = []

	# tempo total de execucao
	tempoTotal = 0
	for x in duracoes:
		tempoTotal = tempoTotal + x


	#se alguem esta em execucao
	execucao = False
	#quem esta em execucao
	executando = -1

	tempoExecutadoDeCadaTarefa = []
	tempoTerminoDeCadaTarefa = []
	tempoEsperaDeCadaTarefa = []

	#lista contendo o tempo de cada tarefa
	for x in range(0,qtdTarefas):
		#para cada
		tempoExecutadoDeCadaTarefa.append(x)
		tempoTerminoDeCadaTarefa.append(x)
		tempoEsperaDeCadaTarefa.append(x)
		tempoExecutadoDeCadaTarefa[x] = 0
		tempoTerminoDeCadaTarefa[x] = 0
		tempoEsperaDeCadaTarefa[x] = 0
		##print("(debug) ", tempoExecutadoDeCadaTarefa, x)

	#passando o tempo 	
	for x in range(0,tempoTotal):
		for y in range(0,qtdTarefas):
			if todasAsTarefasPorDuracao[y][0]==x:
				#organizando pela duracao uma fila de todas as tarefas que ja tiveram seu tempo de inicio
				heapq.heappush(filaHeap,(todasAsTarefasPorDuracao[y][1],y))
				##print("(debug) duracao ", todasAsTarefasPorDuracao[y][1])


		#pegando o proximo a ser executado
		if not execucao:
			if filaHeap:
				# executando a tarefa y
				executando = heapq.heappop(filaHeap)[1]
				trocasDeContexto = trocasDeContexto +1
				execucao = True
				##print("(debug) executando a tarefa ", executando, "em ",x, " segundos")


		#aumentando o tempo executado da tarefa y
		tempoExecutadoDeCadaTarefa[executando] = tempoExecutadoDeCadaTarefa[executando] + 1

		#atualizando tempos de espera
		for y in range(0,qtdTarefas):
			if y != executando and todasAsTarefasPorDuracao[y][0] <= x and tempoTerminoDeCadaTarefa[y] == 0:
				tempoEsperaDeCadaTarefa[y] = tempoEsperaDeCadaTarefa[y] + 1

		tempoRestanteDaTarefaEmExecucao = todasAsTarefasPorDuracao[executando][1] - tempoExecutadoDeCadaTarefa[executando]

		if tempoRestanteDaTarefaEmExecucao == 0:
			tempoTerminoDeCadaTarefa[executando] = x + 1
			##print("(debug) tempo de termino da tarefa ", executando, " ", tempoTerminoDeCadaTarefa[executando])
			execucao = False

		for y in range(0,qtdTarefas):
			tempoRestanteDaTarefaComparada = todasAsTarefasPorDuracao[y][1] - tempoExecutadoDeCadaTarefa[y]
			if tempoRestanteDaTarefaEmExecucao > tempoRestanteDaTarefaComparada and tempoRestanteDaTarefaComparada > 0 and execucao:
				# a tarefa atual eh colocada na fila com o tempo restante como parametro para o sort
				##print("(debug) troca da tarefa ", executando, "pela ", y)
				##print("(debug) tempo restante da tarefa em execucao", tempoRestanteDaTarefaEmExecucao)
				##print("(debug) tempo restante da tarefa a tomar prioridade", tempoRestanteDaTarefaComparada)
				heapq.heappush(filaHeap,(tempoRestanteDaTarefaEmExecucao,executando))
				execucao = False
	

	tempoTotal = 0
	esperaTotal = 0

	for x in range(0,qtdTarefas):
		tempoTotal = tempoTotal + tempoTerminoDeCadaTarefa[x] - todasAsTarefasPorDuracao[x][0]
		esperaTotal = esperaTotal + tempoEsperaDeCadaTarefa[x]
		##print("(debug) ", x)
		##print("(debug) ", tempoTotal)
		##print("(debug) ", tempoEsperaDeCadaTarefa[x])
		##print("(debug) ", esperaTotal)


	tempoMedioExecucaoSRTF = tempoTotal / qtdTarefas

	tempoMedioEsperaSRTF = esperaTotal / qtdTarefas

	##print("tempo medio de execucao escalonamento SRTF: ", tempoMedioExecucaoSRTF)
	##print("tempo medio de espera escalonamento SRTF: ", tempoMedioEsperaSRTF)
	##print("trocas de contexto SRTF: ", trocasDeContexto)

	return tempoMedioExecucaoSRTF, tempoMedioEsperaSRTF, trocasDeContexto, tempoTotal

#[0] = ingressos // [1] = duracao // [2] = prioridades
def PRIOc(qtdTarefas, duracoes, todasAsTarefasPorPrioridade):

	trocasDeContexto = - 1

	##print("(debug) todas as tarefas por prioridade: ", todasAsTarefasPorPrioridade)
	filaHeap = []

	# tempo total de execucao
	tempoTotal = 0
	for x in duracoes:
		tempoTotal = tempoTotal + x


	#se alguem esta em execucao
	execucao = False
	#quem esta em execucao
	executando = -1

	tempoExecutadoDeCadaTarefa = []
	tempoTerminoDeCadaTarefa = []
	tempoEsperaDeCadaTarefa = []

	#lista contendo o tempo de cada tarefa
	for x in range(0,qtdTarefas):
		#para cada
		tempoExecutadoDeCadaTarefa.append(x)
		tempoTerminoDeCadaTarefa.append(x)
		tempoEsperaDeCadaTarefa.append(x)
		tempoExecutadoDeCadaTarefa[x] = 0
		tempoTerminoDeCadaTarefa[x] = 0
		tempoEsperaDeCadaTarefa[x] = 0
		##print("(debug) ", tempoExecutadoDeCadaTarefa, x)

	#passando o tempo 	
	for x in range(0,tempoTotal):
		for y in range(0,qtdTarefas):
			if todasAsTarefasPorPrioridade[y][0]==x:
				#organizando pela prioridade uma fila de todas as tarefas que ja tiveram seu tempo de inicio
				heapq.heappush(filaHeap,(-todasAsTarefasPorPrioridade[y][2],y))
				##print("(debug) prioridade ", todasAsTarefasPorPrioridade[y][2])


		#pegando o proximo a ser executado
		if not execucao:
			if filaHeap:
				# executando a tarefa y
				executando = heapq.heappop(filaHeap)[1]
				trocasDeContexto = trocasDeContexto + 1
				execucao = True
				##print("(debug) executando a tarefa ", executando, "em ",x, " segundos")


		#aumentando o tempo executado da tarefa y
		tempoExecutadoDeCadaTarefa[executando] = tempoExecutadoDeCadaTarefa[executando] + 1

		#atualizando tempos de espera
		for y in range(0,qtdTarefas):
			if y != executando and todasAsTarefasPorPrioridade[y][0] <= x and tempoTerminoDeCadaTarefa[y] == 0:
				tempoEsperaDeCadaTarefa[y] = tempoEsperaDeCadaTarefa[y] + 1

		tempoRestanteDaTarefaEmExecucao = todasAsTarefasPorPrioridade[executando][1] - tempoExecutadoDeCadaTarefa[executando]

		#encerrando a tarefa
		if tempoRestanteDaTarefaEmExecucao == 0:
			tempoTerminoDeCadaTarefa[executando] = x + 1
			##print("(debug) tempo de termino da tarefa ", executando, " ", tempoTerminoDeCadaTarefa[executando])
			execucao = False

	

	tempoTotal = 0
	esperaTotal = 0

	for x in range(0,qtdTarefas):
		tempoTotal = tempoTotal + tempoTerminoDeCadaTarefa[x] - todasAsTarefasPorPrioridade[x][0]
		esperaTotal = esperaTotal + tempoEsperaDeCadaTarefa[x]
		##print("(debug) ", x)
		##print("(debug) ", tempoTotal)
		##print("(debug) ", tempoEsperaDeCadaTarefa[x])
		##print("(debug) ", esperaTotal)


	tempoMedioExecucaoPRIOc = tempoTotal / qtdTarefas

	tempoMedioEsperaPRIOc = esperaTotal / qtdTarefas

	##print("tempo medio de execucao escalonamento PRIOc: ", tempoMedioExecucaoPRIOc)
	##print("tempo medio de espera escalonamento PRIOc: ", tempoMedioEsperaPRIOc)
	##print("trocas de contexto PRIOc: ", trocasDeContexto)
	return tempoMedioExecucaoPRIOc, tempoMedioEsperaPRIOc, trocasDeContexto, tempoTotal


#[0] = ingressos // [1] = duracao // [2] = prioridades
def PRIOp(qtdTarefas, duracoes, todasAsTarefasPorPrioridade):

	trocasDeContexto = - 1


	##print("(debug) todas as tarefas por prioridade: ", todasAsTarefasPorPrioridade)
	filaHeap = []

	# tempo total de execucao
	tempoTotal = 0
	for x in duracoes:
		tempoTotal = tempoTotal + x


	#se alguem esta em execucao
	execucao = False
	#quem esta em execucao
	executando = -1

	tempoExecutadoDeCadaTarefa = []
	tempoTerminoDeCadaTarefa = []
	tempoEsperaDeCadaTarefa = []

	#lista contendo o tempo de cada tarefa
	for x in range(0,qtdTarefas):
		#para cada
		tempoExecutadoDeCadaTarefa.append(x)
		tempoTerminoDeCadaTarefa.append(x)
		tempoEsperaDeCadaTarefa.append(x)
		tempoExecutadoDeCadaTarefa[x] = 0
		tempoTerminoDeCadaTarefa[x] = 0
		tempoEsperaDeCadaTarefa[x] = 0
		##print("(debug) ", tempoExecutadoDeCadaTarefa, x)

	#passando o tempo 	
	for x in range(0,tempoTotal):
		for y in range(0,qtdTarefas):
			if todasAsTarefasPorPrioridade[y][0]==x:
				#organizando pela prioridade uma fila de todas as tarefas que ja tiveram seu tempo de inicio
				heapq.heappush(filaHeap,(-todasAsTarefasPorPrioridade[y][2],y))
				##print("(debug) prioridade ", todasAsTarefasPorPrioridade[y][2])

		for y in range(0,qtdTarefas):
			if todasAsTarefasPorPrioridade[executando][2] < todasAsTarefasPorPrioridade[y][2] and tempoTerminoDeCadaTarefa[y] == 0 and execucao:
				# a tarefa atual eh colocada na fila com o tempo restante como parametro para o sort
				##print("(debug) troca da tarefa ", executando, "pela ", y)
				##print("(debug) prioridade da tarefa em execucao", todasAsTarefasPorPrioridade[executando][2])
				##print("(debug) prioridade da tarefa a tomar prioridade", todasAsTarefasPorPrioridade[y][2])
				heapq.heappush(filaHeap,(-todasAsTarefasPorPrioridade[executando][2],executando))
				execucao = False


		#pegando o proximo a ser executado
		if not execucao:
			if filaHeap:
				# executando a tarefa y
				executando = heapq.heappop(filaHeap)[1]
				trocasDeContexto = trocasDeContexto + 1
				execucao = True
				##print("(debug) executando a tarefa ", executando, "em ",x, " segundos")


		#aumentando o tempo executado da tarefa y
		tempoExecutadoDeCadaTarefa[executando] = tempoExecutadoDeCadaTarefa[executando] + 1

		#atualizando tempos de espera
		for y in range(0,qtdTarefas):
			if y != executando and todasAsTarefasPorPrioridade[y][0] <= x and tempoTerminoDeCadaTarefa[y] == 0:
				tempoEsperaDeCadaTarefa[y] = tempoEsperaDeCadaTarefa[y] + 1

		tempoRestanteDaTarefaEmExecucao = todasAsTarefasPorPrioridade[executando][1] - tempoExecutadoDeCadaTarefa[executando]

		#encerrando a tarefa
		if tempoRestanteDaTarefaEmExecucao == 0:
			tempoTerminoDeCadaTarefa[executando] = x + 1
			##print("(debug) tempo de termino da tarefa ", executando, " ", tempoTerminoDeCadaTarefa[executando])
			execucao = False


	

	tempoTotal = 0
	esperaTotal = 0

	for x in range(0,qtdTarefas):
		tempoTotal = tempoTotal + tempoTerminoDeCadaTarefa[x] - todasAsTarefasPorPrioridade[x][0]
		esperaTotal = esperaTotal + tempoEsperaDeCadaTarefa[x]
		##print("(debug) ", x)
		##print("(debug) ", tempoTotal)
		##print("(debug) ", tempoEsperaDeCadaTarefa[x])
		##print("(debug) ", esperaTotal)


	tempoMedioExecucaoPRIOp = tempoTotal / qtdTarefas

	tempoMedioEsperaPRIOp = esperaTotal / qtdTarefas

	##print("tempo medio de execucao escalonamento PRIOp: ", tempoMedioExecucaoPRIOp)
	##print("tempo medio de espera escalonamento PRIOp: ", tempoMedioEsperaPRIOp)
	##print("trocas de contexto PRIOp: ", trocasDeContexto)

	return tempoMedioExecucaoPRIOp, tempoMedioEsperaPRIOp, trocasDeContexto, tempoTotal


#[0] = ingressos // [1] = duracao // [2] = prioridades
def PRIOd(qtdTarefas, duracoes, todasAsTarefasPorPrioridade):

	trocasDeContexto = -1

	##print("(debug) todas as tarefas por prioridade: ", todasAsTarefasPorPrioridade)
	filaHeap = []
	filaHeapTemp = []

	# tempo total de execucao
	tempoTotal = 0
	for x in duracoes:
		tempoTotal = tempoTotal + x


	#se alguem esta em execucao
	execucao = False
	#quem esta em execucao
	executando = -1

	#controle se os valoers de prioridade devem ser atualizados
	atualizarValoresDePrioridade = False

	#controle se a tarefa atual tem prioridade menor que alguem da fila
	trocarTarefa = False

	#prioridade da tarefa atual
	prioridadeAtual = 0


	tempoExecutadoDeCadaTarefa = []
	tempoTerminoDeCadaTarefa = []
	tempoEsperaDeCadaTarefa = []

	prioridadeOriginalDeTodasAsTarefas = []

	#lista contendo o tempo de cada tarefa
	for x in range(0,qtdTarefas):
		#para cada
		tempoExecutadoDeCadaTarefa.append(x)
		tempoTerminoDeCadaTarefa.append(x)
		tempoEsperaDeCadaTarefa.append(x)
		prioridadeOriginalDeTodasAsTarefas.append(todasAsTarefasPorPrioridade[x][2])
		tempoExecutadoDeCadaTarefa[x] = 0
		tempoTerminoDeCadaTarefa[x] = 0
		tempoEsperaDeCadaTarefa[x] = 0
		##print("(debug) ", tempoExecutadoDeCadaTarefa, x)

	#passando o tempo 	
	for x in range(0,tempoTotal):
		##print("(debug) segundo ", x)
		for y in range(0,qtdTarefas):
			##colocarNaFila()
			# print("(debug) analizando tarefa ", y, "com prioridade ", todasAsTarefasPorPrioridade[y][2])

			if todasAsTarefasPorPrioridade[y][0]==x:
				#organizando pela prioridade uma fila de todas as tarefas que ja tiveram seu tempo de inicio
				heapq.heappush(filaHeap,(-todasAsTarefasPorPrioridade[y][2],y))
				##print("(debug) colocando na fila a tarefa", y , " com prioridade ", todasAsTarefasPorPrioridade[y][2])

		#pegando o proximo a ser executado
		if filaHeap:
			if not execucao or prioridadeAtual > heapq.nsmallest(1,filaHeap)[0][0]:
				if prioridadeAtual != 0 and tempoTerminoDeCadaTarefa[executando] == 0:
					heapq.heappush(filaHeap,(-todasAsTarefasPorPrioridade[executando][2],executando))
					##print("(debug) colocando na fila a tarefa", executando , " com prioridade ", todasAsTarefasPorPrioridade[executando][2])

				# executando a tarefa y
				tarefaAtual = heapq.heappop(filaHeap)
				executando = tarefaAtual[1]
				prioridadeAtual = tarefaAtual[0]
				trocasDeContexto = trocasDeContexto + 1
				execucao = True
				##print("(debug) executando a tarefa ", executando, "em ",x, " segundos, com prioridade ", prioridadeAtual)


				z = 0
				##print("(debug) aumentando prioridades")
				while filaHeap:
					filaHeapTemp.append(heapq.heappop(filaHeap))
					filaHeapTemp[z] = list(filaHeapTemp[z])
					filaHeapTemp[z][0] = filaHeapTemp[z][0] - 1
					z = z + 1
				##print("(debug) fila de prioridades :", filaHeapTemp)
				if filaHeapTemp:
					for y in (0,len(filaHeapTemp) - 1):
						if filaHeapTemp[y][1] != executando:
							heapq.heappush(filaHeap,(filaHeapTemp[y][0],filaHeapTemp[y][1]))
				filaHeapTemp = []

		#aumentando o tempo executado da tarefa y
		tempoExecutadoDeCadaTarefa[executando] = tempoExecutadoDeCadaTarefa[executando] + 1

		#atualizando tempos de espera
		for y in range(0,qtdTarefas):
			if y != executando and todasAsTarefasPorPrioridade[y][0] <= x and tempoTerminoDeCadaTarefa[y] == 0:
				tempoEsperaDeCadaTarefa[y] = tempoEsperaDeCadaTarefa[y] + 1

		tempoRestanteDaTarefaEmExecucao = todasAsTarefasPorPrioridade[executando][1] - tempoExecutadoDeCadaTarefa[executando]

		#encerrando a tarefa
		if tempoRestanteDaTarefaEmExecucao == 0:
			tempoTerminoDeCadaTarefa[executando] = x + 1
			##print("(debug) tempo de termino da tarefa ", executando, " ", tempoTerminoDeCadaTarefa[executando])
			execucao = False


	tempoTotal = 0
	esperaTotal = 0

	for x in range(0,qtdTarefas):
		tempoTotal = tempoTotal + tempoTerminoDeCadaTarefa[x] - todasAsTarefasPorPrioridade[x][0]
		esperaTotal = esperaTotal + tempoEsperaDeCadaTarefa[x]
		##print("(debug) ", x)
		##print("(debug) ", tempoTotal)
		##print("(debug) ", tempoEsperaDeCadaTarefa[x])
		##print("(debug) ", esperaTotal)


	tempoMedioExecucaoPRIOd = tempoTotal / qtdTarefas

	tempoMedioEsperaPRIOd = esperaTotal / qtdTarefas

	##print("tempo medio de execucao escalonamento PRIOd: ", tempoMedioExecucaoPRIOd)
	##print("tempo medio de espera escalonamento PRIOd: ", tempoMedioEsperaPRIOd)
	##print("trocas de contexto PRIOd: ", trocasDeContexto)

	return tempoMedioExecucaoPRIOd, tempoMedioEsperaPRIOd, trocasDeContexto, tempoTotal

def main():
	# lista onde serao armazenadas as tarefas
	tarefasString = []


	print("Aluno: Felipe Tomazelli Crespo")
	print("DRE: 113203901")
	print("Exercicio 2 de Sistemas operacionais (MAB-366) -- 2019/2")
	print("Algoritmos de escalonamento de tarefas")
	print("Professora Silvana Rosseto")

	print("")
	print("nomear o arquivo com as entradas como \"tarefas.txt\", ambos na mesma pasta")
	print("formato esperado:")
	print("1a linha = numero de tarefas")
	print("2a linha = tempso de ingresso")
	print("3a linha = duracoes")
	print("4a linha = prioridades")
	print("todos separados por espaços em branco \" \"")
	print("")
	print("pressione ENTER para continuar")
	input()

	# lendo o arquivo de tarefas e armazenando a lista em string
	f=open("tarefas.txt", "r")
	if f.mode == 'r':
		f1 = f.readlines()
		for x in f1:
			#removendo o /n ao final
			tarefasString.append(x.strip())
			#print(x.strip())



	##debug
	##print(tarefasString)
	##input()

	# armazenando os dados de forma clara e convertendo para inteiros
	qtdTarefas = int(tarefasString[0])
	
	ingressos = [int(x) for x in tarefasString[1].split()]
	duracoes = [int(x) for x in tarefasString[2].split()]
	prioridades = [int(x) for x in tarefasString[3].split()]

	todasAsTarefas = []

	#criando uma heap para organizar a lista de duracao e prioridade para os algoritmos
	todasAsTarefasPorDuracaoHeap = []
	todasAsTarefasPorPrioridadeHeap = []

	for x in range(0,qtdTarefas):
		todasAsTarefas.append((ingressos[x],duracoes[x],prioridades[x]))
		heapq.heappush(todasAsTarefasPorDuracaoHeap,(duracoes[x],todasAsTarefas[x]))
		heapq.heappush(todasAsTarefasPorPrioridadeHeap,(prioridades[x],todasAsTarefas[x]))


	#convertendo de heap para lista
	todasAsTarefasPorDuracao = []
	todasAsTarefasPorPrioridade = []

	while todasAsTarefasPorDuracaoHeap:
		next_item = heapq.heappop(todasAsTarefasPorDuracaoHeap)
		todasAsTarefasPorDuracao.append(next_item[1])
		next_item = heapq.heappop(todasAsTarefasPorPrioridadeHeap)
		todasAsTarefasPorPrioridade.append(next_item[1])

	##print("(debug) todas as tarefas: \n", todasAsTarefas)
	##print("(debug) todas as tarefas por duracao: \n", todasAsTarefasPorDuracao)

	
	##print("(debug) quantidade de tarefas: ", qtdTarefas)
	##print("(debug) tempos de ingresso: ", ingressos)
	##print("(debug) tempos de duracoes: ", duracoes)
	##print("(debug) valor das prioridades: ", prioridades)

	resultadosFinais = []
	#seria mais facil passar o tempo total em vez das duracoes para SJF em diante...
	resultadosFinais.append(FCFS(qtdTarefas,ingressos,duracoes,prioridades))
	resultadosFinais.append(RR(qtdTarefas,ingressos,duracoes,prioridades))
	resultadosFinais.append(SJF(qtdTarefas, duracoes, todasAsTarefasPorDuracao))
	resultadosFinais.append(SRTF(qtdTarefas, duracoes, todasAsTarefasPorDuracao))
	resultadosFinais.append(PRIOc(qtdTarefas, duracoes, todasAsTarefasPorPrioridade))
	resultadosFinais.append(PRIOp(qtdTarefas, duracoes, todasAsTarefasPorPrioridade))
	resultadosFinais.append(PRIOd(qtdTarefas, duracoes, todasAsTarefasPorPrioridade))

	print("_______________________________________________________________________")
	print("")
	print("     Algoritmo     | FCFS |  RR  |  SJF | SRTF | PRIOc | PRIOp | PRIOd |" )
	print("_______________________________________________________________________")
	print("")
	print("Tempo Medio Tt     |", resultadosFinais[0][0], " |", resultadosFinais[1][0], " |", resultadosFinais[2][0], " |", resultadosFinais[3][0], " |", resultadosFinais[4][0], "  |", resultadosFinais[5][0], "  |", resultadosFinais[6][0], "  |")
	print("Tempo Medio Tw     |", resultadosFinais[0][1], " |", resultadosFinais[1][1], " |", resultadosFinais[2][1], " |", resultadosFinais[3][1], " |", resultadosFinais[4][1], "  |", resultadosFinais[5][1], "  |", resultadosFinais[6][1], "  |")
	print("Trocas de Contexto |", resultadosFinais[0][2], "   |", resultadosFinais[1][2], "   |", resultadosFinais[2][2], "   |", resultadosFinais[3][2], "   |", resultadosFinais[4][2], "    |", resultadosFinais[5][2], "    |", resultadosFinais[6][2], "    |")
	print("Tempo Total        |", resultadosFinais[0][2], "   |", resultadosFinais[1][2], "   |", resultadosFinais[2][2], "   |", resultadosFinais[3][2], "   |", resultadosFinais[4][2], "    |", resultadosFinais[5][2], "    |", resultadosFinais[6][2], "    |")
	print("_______________________________________________________________________")
	print("OBS: Nao foram estabelecidos criterios para desempate nos algoritmos")
	print("em casos de empate simplesmente utilizei a posicao na heap")
	print("")
	print("pressione ENTER para encerrar")
	input()


if __name__ == '__main__':
	main()
