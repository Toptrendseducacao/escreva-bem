import random
from tkinter import *
from tkinter import messagebox
import pygame
import cv2
import sqlite3

with sqlite3.connect('escrevabem.db') as dados:
    c = dados.cursor()

c.execute(
    'CREATE TABLE IF NOT EXISTS cadastros (codigo int auto_increment, nome varchar(50) not null, usuario varchar(30) not null unique, email varchar(100) not null unique, senha varchar(30) not null, pergunta varchar(100) not null, resposta varchar(50) not null, primary key(codigo));')
dados.commit()
dados.close()

pygame.init()

# INTRODUÇÃO TOP TRENDS EDUCAÇÃO
intro = cv2.VideoCapture('videos/intro.mp4')

while intro.isOpened():
    ret, janela = intro.read()

    if ret:

        cv2.imshow('ESCREVA BEM', janela)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
intro.release()
cv2.destroyAllWindows()

# JANELA E SUAS VARIÁVEIS

janela = Tk()  # CRIAR JANELA

janela.title("ESCREVA BEM")  # TÍTULO DA JANELA

janela.iconbitmap('imagens/logojogo.ico')  # ÍCONE DA JANELA

janela.geometry("800x600+275+50")  # TAMANHO E POSIÇÃO DA JANELA

janela.resizable(width=False, height=False)  # RECONFIGURAR TAMANHO DA JANELA

janela.configure(bg='black')  # COR DA JANELA


# MÚSICA DO JOGO
def musicaJogo():
    pygame.mixer.music.load('sons/musicajogo1.mp3')
    pygame.mixer.music.play(loops=10)


# EFEITOS SONOROS
sound = pygame.mixer.Sound('sons/select2.wav')
soundhover = pygame.mixer.Sound('sons/hover3.wav')


# SAIR DO JOGO
def quit():
    pygame.mixer.music.stop()
    janela.quit()


# BOTÕES DE MUTAR E DESMUTAR
muteimg = PhotoImage(file='imagens/mute3.png')
label3 = Label(janela, image=muteimg)
label3.pack()
label3.place(x=5, y=6)

desmuteimg = PhotoImage(file='imagens/desmute3.png')
label4 = Label(janela, image=desmuteimg)
label4.pack()
label4.place(x=5, y=6)


def mutar():
    pygame.mixer.music.pause()
    desmute = Button(janela, image=desmuteimg, bg='black', activebackground='black', command=desmutar)
    desmute.place(x=5, y=6)


def desmutar():
    pygame.mixer.music.unpause()
    mute = Button(janela, image=muteimg, bg='black', activebackground='black', command=mutar)
    mute.place(x=5, y=6)


# DEPÓSITO DE PERGUNTAS
questoes = [["IREI AO RESTAURANTE...", "ALMOSSAR", "AUMOÇAR", "AUMOSSAR", "ALMOÇAR"],
            ["IREI CONTATAR MEU...", "ADEVOGADO", "ADIVOGADO", "ADIVOGADU", "ADVOGADO"],
            ["COMPREI 200 GRAMAS DE...", "MORTADELLA", "MORTANDELA", "MOTADELA", "MORTADELA"],
            ["VOU DAR UM PASSEIO DE...", "BICECLETA", "BECICLETA", "BECECLETA", "BICICLETA"],
            ["É SEMPRE UM ... RECEBÊ-LO(A) EM MINHA CASA!", "PRASER", "PRAZÊ", "PRASÊ", "PRAZER"]]


# REMOVER ELEMENTOS DA JANELA
def limparElementos():
    elementos = janela.grid_slaves()
    for e in elementos:
        e.destroy()


# TOTAL DE QUESTÕES
totalPerg = 30


# INICIAR JOGO ALUNO
class IniciarJogo:
    def __init__(self, quest):
        limparElementos()
        pygame.mixer.music.pause()

        # BACKGROUND
        self.fundo = PhotoImage(file='imagens/bg.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        # ACRESCENTAR PERGUNTAS
        self.Perguntar = []
        for n in quest:
            self.Perguntar.append(n)
        self.travar = False

        # CONTADOR DE RESPOSTAS CORRETAS
        self.correta = 0

        # CONTADOR DE RESPOSTAS ERRADAS
        self.errada = 0

        # BOTÃO DE AVANÇAR
        self.avancar = Button(janela, width=7, height=1,
                              text="PRÓXIMA",
                              bg='#0099ff',
                              fg='white',
                              font=("BigNoodleTitling", 22),
                              command=self.Questao)

        self.numero = 0
        self.Questao()

    # AVANÇAR QUESTÃO
    def Questao(self):
        self.avancar.place(x=352, y=1000)

        # RANDOMIZADOR DE PERGUNTAS
        if len(self.Perguntar) > 0 and self.numero < totalPerg:
            self.numero += 1
            self.travar = False
            NumAleatorio = random.randint(0, len(self.Perguntar) - 1)

            # FRASE AUXÍLIO
            PerguntarText = self.Perguntar[NumAleatorio][0]

            self.proxQuest = self.Perguntar[NumAleatorio][-1]
            respostas = []

            for i in range(1, 5):
                respostas.append(self.Perguntar[NumAleatorio][i])

            # ------------------------------ EMBARALHAR RESPOSTAS ------------------------------ #

            random.shuffle(respostas)

            self.alternativa1 = respostas[0]
            self.alternativa2 = respostas[1]
            self.alternativa3 = respostas[2]
            self.alternativa4 = respostas[3]

            # ------------------------ CONFIGURAÇÕES DA FRASE DE AUXÍLIO ----------------------- #

            Questao = Entry(janela,
                            font=('BigNoodleTitling', 30),
                            bg='white',
                            fg='black',
                            width=45,
                            justify='center',
                            highlightbackground="#37d3ff")
            Questao.insert(END, PerguntarText)
            Questao.grid(row=0,
                         column=0,
                         columnspan=4,
                         pady=4)
            Questao.place(x=60, y=90)

            # -------------------------- CONFIGURAÇÕES DOS BOTÕES DE RESPOSTA -------------------------- #
            self.opcao1 = Button(janela,
                                 text=self.alternativa1,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 1
                                 height=2,
                                 command=self.fiscalizar1,
                                 bg='#e6ac00', fg='black')
            self.opcao1.place(x=60, y=200)

            # ---------------------------------------------------------------------------------------#

            self.opcao2 = Button(janela,
                                 text=self.alternativa2,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 2
                                 height=2,
                                 command=self.fiscalizar2,
                                 bg='#e6ac00', fg='black')
            self.opcao2.place(x=415, y=200)

            # ---------------------------------------------------------------------------------------#

            self.opcao3 = Button(janela,
                                 text=self.alternativa3,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 3
                                 height=2,
                                 command=self.fiscalizar3,
                                 bg='#e6ac00', fg='black')
            self.opcao3.place(x=60, y=330)

            # ---------------------------------------------------------------------------------------#

            self.opcao4 = Button(janela,
                                 text=self.alternativa4,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 4
                                 height=2,
                                 command=self.fiscalizar4,
                                 bg='#e6ac00', fg='black')
            self.opcao4.place(x=415, y=330)

            # ---------------------------------------------------------------------------------------#

            if self.alternativa1 == self.proxQuest:
                self.BtProxQuestao = self.opcao1
            elif self.alternativa2 == self.proxQuest:
                self.BtProxQuestao = self.opcao2
            elif self.alternativa3 == self.proxQuest:
                self.BtProxQuestao = self.opcao3
            elif self.alternativa4 == self.proxQuest:
                self.BtProxQuestao = self.opcao4
            self.Perguntar.pop(NumAleatorio)
        else:
            limparElementos()

            self.white = PhotoImage(file='imagens/resultado.png')
            Label(janela, image=self.white).place(relwidth=1, relheight=1)

            # ----------------------------------- CONFIGURAÇÕES DO RESULTADO ------------------------------------- #

            lb = Label(janela, bg='white', fg='black',
                       text=f'{str(self.correta)}' + f'\n{str(self.errada)}',
                       font=('BigNoodleTitling', 55),
                       justify='center')
            lb.grid(column=0,
                    row=0,  # CONTADOR DE CORRETAS E INCORRETAS
                    padx=50,
                    pady=(188, 15))

            # --------------------------------------------------------------------------------------------------- #

            self.btmenu = Button(janela,
                                 text="RETORNAR",
                                 bg='#bfbfbf',
                                 font=('BigNoodleTitling', 25),
                                 command=voltarMenuAluno)  # BOTÃO DE VOLTAR AO MENU
            self.btmenu.grid(column=0,
                             row=1,
                             pady=150)
            self.btmenu.place(x=350, y=500)

            self.btmenu.bind('<Enter>', self.hover)
            self.btmenu.bind('<Leave>', self.hover_leave)

    def hover(self, e):
        self.btmenu.configure(bg='white')

    def hover_leave(self, e):
        self.btmenu.configure(bg='#bfbfbf')

        # --------------------------------------------------------------------------------------------------- #

    def fiscalizar1(self):
        if not self.travar:
            if self.proxQuest != self.alternativa1:
                self.opcao1.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao1.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)

    def fiscalizar2(self):
        if not self.travar:
            if self.proxQuest != self.alternativa2:
                self.opcao2.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao2.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)

    def fiscalizar3(self):
        if not self.travar:
            if self.proxQuest != self.alternativa3:
                self.opcao3.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao3.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)

    def fiscalizar4(self):
        if not self.travar:
            if self.proxQuest != self.alternativa4:
                self.opcao4.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao4.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)


# INICIAR JOGO PROFESSOR
class IniciarJogo2:
    def __init__(self, quest):
        limparElementos()
        pygame.mixer.music.pause()

        # BACKGROUND
        self.fundo = PhotoImage(file='imagens/bg.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        # ACRESCENTAR PERGUNTAS
        self.Perguntar = []
        for n in quest:
            self.Perguntar.append(n)
        self.travar = False

        # CONTADOR DE RESPOSTAS CORRETAS
        self.correta = 0

        # CONTADOR DE RESPOSTAS ERRADAS
        self.errada = 0

        # BOTÃO DE AVANÇAR
        self.avancar = Button(janela, width=7, height=1,
                              text="PRÓXIMA",
                              bg='#0099ff',
                              fg='white',
                              font=("BigNoodleTitling", 22),
                              command=self.Questao)

        self.numero = 0
        self.Questao()

    # AVANÇAR QUESTÃO
    def Questao(self):
        self.avancar.place(x=352, y=1000)

        # RANDOMIZADOR DE PERGUNTAS
        if len(self.Perguntar) > 0 and self.numero < totalPerg:
            self.numero += 1
            self.travar = False
            NumAleatorio = random.randint(0, len(self.Perguntar) - 1)

            # FRASE AUXÍLIO
            PerguntarText = self.Perguntar[NumAleatorio][0]

            self.proxQuest = self.Perguntar[NumAleatorio][-1]
            respostas = []

            for i in range(1, 5):
                respostas.append(self.Perguntar[NumAleatorio][i])

            # ------------------------------ EMBARALHAR RESPOSTAS ------------------------------ #

            random.shuffle(respostas)

            self.alternativa1 = respostas[0]
            self.alternativa2 = respostas[1]
            self.alternativa3 = respostas[2]
            self.alternativa4 = respostas[3]

            # ------------------------ CONFIGURAÇÕES DA FRASE DE AUXÍLIO ----------------------- #

            Questao = Entry(janela,
                            font=('BigNoodleTitling', 30),
                            bg='white',
                            fg='black',
                            width=45,
                            justify='center',
                            highlightbackground="#37d3ff")
            Questao.insert(END, PerguntarText)
            Questao.grid(row=0,
                         column=0,
                         columnspan=4,
                         pady=4)
            Questao.place(x=60, y=90)

            # -------------------------- CONFIGURAÇÕES DOS BOTÕES DE RESPOSTA -------------------------- #
            self.opcao1 = Button(janela,
                                 text=self.alternativa1,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 1
                                 height=2,
                                 command=self.fiscalizar1,
                                 bg='#e6ac00', fg='black')
            self.opcao1.place(x=60, y=200)

            # ---------------------------------------------------------------------------------------#

            self.opcao2 = Button(janela,
                                 text=self.alternativa2,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 2
                                 height=2,
                                 command=self.fiscalizar2,
                                 bg='#e6ac00', fg='black')
            self.opcao2.place(x=415, y=200)

            # ---------------------------------------------------------------------------------------#

            self.opcao3 = Button(janela,
                                 text=self.alternativa3,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 3
                                 height=2,
                                 command=self.fiscalizar3,
                                 bg='#e6ac00', fg='black')
            self.opcao3.place(x=60, y=330)

            # ---------------------------------------------------------------------------------------#

            self.opcao4 = Button(janela,
                                 text=self.alternativa4,
                                 font=("BigNoodleTitling", 26),
                                 width=24,  # BOTÃO 4
                                 height=2,
                                 command=self.fiscalizar4,
                                 bg='#e6ac00', fg='black')
            self.opcao4.place(x=415, y=330)

            # ---------------------------------------------------------------------------------------#

            if self.alternativa1 == self.proxQuest:
                self.BtProxQuestao = self.opcao1
            elif self.alternativa2 == self.proxQuest:
                self.BtProxQuestao = self.opcao2
            elif self.alternativa3 == self.proxQuest:
                self.BtProxQuestao = self.opcao3
            elif self.alternativa4 == self.proxQuest:
                self.BtProxQuestao = self.opcao4
            self.Perguntar.pop(NumAleatorio)
        else:
            limparElementos()

            self.white = PhotoImage(file='imagens/resultado.png')
            Label(janela, image=self.white).place(relwidth=1, relheight=1)

            # ----------------------------------- CONFIGURAÇÕES DO RESULTADO ------------------------------------- #

            lb = Label(janela, bg='white', fg='black',
                       text=f'{str(self.correta)}' + f'\n{str(self.errada)}',
                       font=('BigNoodleTitling', 55),
                       justify='center')
            lb.grid(column=0,
                    row=0,  # CONTADOR DE CORRETAS E INCORRETAS
                    padx=50,
                    pady=(188, 15))

            # --------------------------------------------------------------------------------------------------- #

            self.btmenu = Button(janela,
                                 text="RETORNAR",
                                 bg='#bfbfbf',
                                 font=('BigNoodleTitling', 25),
                                 command=voltarMenuProfessor)  # BOTÃO DE VOLTAR AO MENU
            self.btmenu.grid(column=0,
                             row=1,
                             pady=150)
            self.btmenu.place(x=350, y=500)

            self.btmenu.bind('<Enter>', self.hover)
            self.btmenu.bind('<Leave>', self.hover_leave)

    def hover(self, e):
        soundhover.play()
        self.btmenu.configure(bg='white')

    def hover_leave(self, e):
        self.btmenu.configure(bg='#bfbfbf')

        # --------------------------------------------------------------------------------------------------- #

    def fiscalizar1(self):
        if not self.travar:
            if self.proxQuest != self.alternativa1:
                self.opcao1.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao1.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)

    def fiscalizar2(self):
        if not self.travar:
            if self.proxQuest != self.alternativa2:
                self.opcao2.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao2.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)

    def fiscalizar3(self):
        if not self.travar:
            if self.proxQuest != self.alternativa3:
                self.opcao3.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao3.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)

    def fiscalizar4(self):
        if not self.travar:
            if self.proxQuest != self.alternativa4:
                self.opcao4.configure(bg='#b30000', fg='#f2f2f2')
                pygame.mixer.music.load('sons/errado.mp3')
                pygame.mixer.music.play()
                self.errada += 1
                self.avancar.place(x=352, y=510)

            else:
                self.opcao4.configure(bg='#006622', fg='#f2f2f2')
                pygame.mixer.music.load('sons/correto.mp3')
                pygame.mixer.music.play()
                self.correta += 1
            self.BtProxQuestao.configure(bg='#006622')
            self.travar = True
            self.avancar.place(x=352, y=510)


# MENU ALUNO
class Menu:
    def __init__(self):
        limparElementos()
        self.fundo = PhotoImage(file='imagens/menu.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        musicaJogo()

        mutar()
        desmutar()

        # ------------------------------------ BOTÃO DE INICIAR ------------------------------------ #

        self.Iniciar = Button(janela, text="INICIAR",
                              padx=17, pady=19, width=20,
                              font=('BigNoodleTitling', 26),
                              bg='#e6ac00', fg='black',
                              activebackground='#006622',
                              activeforeground='white', command=self.criarQuiz)
        self.Iniciar.grid(column=0, row=0, padx=420, pady=100)

        # ------------------------------------- BOTÃO DE SAIR ------------------------------------- #

        self.Sair = Button(janela, text='SAIR', width=20,
                           padx=17, pady=19,
                           font=('BigNoodleTitling', 26),
                           bg='#e6ac00', fg='black',
                           activebackground='#b30000',
                           activeforeground='white',
                           command=janela.destroy)
        self.Sair.place(x=420, y=380)

        self.BotRetornar = Button(janela, text="RETORNAR",
                                  padx=17, pady=19, width=20,
                                  font=('BigNoodleTitling', 26),
                                  bg='#e6ac00', fg='black',
                                  activebackground='#004d66',
                                  activeforeground='white', command=voltarmododejogo)
        self.BotRetornar.place(x=420, y=240)

        self.Sair.bind('<Enter>', self.hover)
        self.Sair.bind('<Leave>', self.hover_leave)
        self.Iniciar.bind('<Enter>', self.hover2)
        self.Iniciar.bind('<Leave>', self.hover_leave2)
        self.BotRetornar.bind('<Enter>', self.hover3)
        self.BotRetornar.bind('<Leave>', self.hover_leave3)

    def hover(self, e):
        soundhover.play()
        self.Sair.configure(bg='white')

    def hover_leave(self, e):
        self.Sair.configure(bg='#e6ac00')

    def hover2(self, e):
        soundhover.play()
        self.Iniciar.configure(bg='white')

    def hover_leave2(self, e):
        self.Iniciar.configure(bg='#e6ac00')

    def hover3(self, e):
        soundhover.play()
        self.BotRetornar.configure(bg='white')

    def hover_leave3(self, e):
        self.BotRetornar.configure(bg='#e6ac00')

    def criarQuiz(self):
        sound.play()
        self.Sair.destroy()
        q = IniciarJogo(questoes)


# MENU PROFESSOR
class Menu2:
    def __init__(self):
        limparElementos()
        self.fundo = PhotoImage(file='imagens/menu.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        desmutar()

        # ------------------------------------ BOTÃO DE INICIAR ------------------------------------ #

        self.Iniciar = Button(janela, text="INICIAR",
                              padx=17, pady=19, width=20,
                              font=('BigNoodleTitling', 26),
                              bg='#e6ac00', fg='black',
                              activebackground='#006622',
                              activeforeground='white', command=self.criarQuiz)
        self.Iniciar.grid(column=0, row=0, padx=420, pady=65)

        # ------------------------------------- BOTÃO DE SAIR ------------------------------------- #

        self.Sair = Button(janela, text='SAIR', width=20,
                           padx=17, pady=19,
                           font=('BigNoodleTitling', 26),
                           bg='#e6ac00', fg='black',
                           activebackground='#b30000',
                           activeforeground='white',
                           command=janela.destroy)
        self.Sair.place(x=420, y=425)

        self.Retornar = Button(janela, text='RETORNAR', width=20,
                               padx=17, pady=19,
                               font=('BigNoodleTitling', 26),
                               bg='#e6ac00', fg='black',
                               activebackground='#004d66',
                               activeforeground='white',
                               command=confirma_retornar)
        self.Retornar.place(x=420, y=305)

        self.Sair.bind('<Enter>', self.hover)
        self.Sair.bind('<Leave>', self.hover_leave)
        self.Iniciar.bind('<Enter>', self.hover2)
        self.Iniciar.bind('<Leave>', self.hover_leave2)
        self.Retornar.bind('<Enter>', self.hover3)
        self.Retornar.bind('<Leave>', self.hover_leave3)

    def hover(self, e):
        soundhover.play()
        self.Sair.configure(bg='white')

    def hover_leave(self, e):
        self.Sair.configure(bg='#e6ac00')

    def hover2(self, e):
        soundhover.play()
        self.Iniciar.configure(bg='white')

    def hover_leave2(self, e):
        self.Iniciar.configure(bg='#e6ac00')

    def hover3(self, e):
        soundhover.play()
        self.Retornar.configure(bg='white')

    def hover_leave3(self, e):
        self.Retornar.configure(bg='#e6ac00')

    def criarQuiz(self):
        sound.play()
        self.Sair.destroy()
        q = IniciarJogo2(questoes)


# ADICIONAR PERGUNTAS
class Personalizado:
    def __init__(self):

        self.BotPersonalizar = Button(janela, text="PERSONALIZAR",
                                      padx=17, pady=19, width=20,
                                      font=('BigNoodleTitling', 26),
                                      bg='#e6ac00', fg='black',
                                      activebackground='#660080',
                                      activeforeground='white', command=self.adicionarQuestoes)
        self.BotPersonalizar.place(x=420, y=185)

        self.BotPersonalizar.bind('<Enter>', self.hover)
        self.BotPersonalizar.bind('<Leave>', self.hover_leave)

    def hover(self, e):
        soundhover.play()
        self.BotPersonalizar.configure(bg='white')

    def hover_leave(self, e):
        self.BotPersonalizar.configure(bg='#e6ac00')

    def adicionarQuestoes(self):

        sound.play()

        self.fundo = PhotoImage(file='imagens/bgpersonalizar.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        mutar()

        self.box1 = Entry(janela,
                          font=('BigNoodleTitling', 30),
                          bg='white',
                          fg='black',
                          width=45,
                          justify='center',
                          highlightbackground="#37d3ff")
        self.box1.place(x=60, y=65)

        self.box2 = Entry(janela,
                          font=("BigNoodleTitling", 26),
                          width=24, justify='center',
                          bg='#cc0000', fg='white'
                          )

        self.box2.place(x=230, y=180)

        self.box3 = Entry(janela,
                          font=("BigNoodleTitling", 26),
                          width=24, justify='center',
                          bg='#cc0000', fg='white'
                          )
        self.box3.place(x=230, y=230)

        self.box4 = Entry(janela,
                          font=("BigNoodleTitling", 26),
                          width=24, justify='center',
                          bg='#cc0000', fg='white'
                          )
        self.box4.place(x=230, y=280)

        self.box5 = Entry(janela,
                          font=("BigNoodleTitling", 26),
                          width=24, justify='center',
                          bg='#004d00', fg='white'
                          )
        self.box5.place(x=230, y=390)

        self.BotAdicionar = Button(janela, text="ADICIONAR", width=20, height=1,
                                   font=('BigNoodleTitling', 25),
                                   bg='#003300', fg='white',
                                   activebackground='#006622',
                                   activeforeground='white', command=self.adicionando)
        self.BotAdicionar.place(x=130, y=520)

        self.BotFechar = Button(janela, text="FECHAR", width=20, height=1,
                                font=('BigNoodleTitling', 25),
                                bg='#990000', fg='white',
                                activebackground='#e60000',
                                activeforeground='white', command=self.quitp)
        self.BotFechar.place(x=420, y=520)

        self.BotAdicionar.bind('<Enter>', self.hover3)
        self.BotAdicionar.bind('<Leave>', self.hover_leave3)
        self.BotFechar.bind('<Enter>', self.hover4)
        self.BotFechar.bind('<Leave>', self.hover_leave4)

        self.botDeletar_adicionar = Button(janela, width=23, font=('bignoodletitling', 13),
                                           command=self.limparBanco)
        self.botDeletar_adicionar.place(x=230, y=450)

        self.x = ["IREI AO RESTAURANTE...", "ALMOSSAR", "AUMOÇAR", "AUMOSSAR", "ALMOÇAR"]
        self.x2 = ["IREI CONTATAR MEU...", "ADEVOGADO", "ADIVOGADO", "ADIVOGADU", "ADVOGADO"]
        self.x3 = ["COMPREI 200 GRAMAS DE...", "MORTADELLA", "MORTANDELA", "MOTADELA", "MORTADELA"]
        self.x4 = ["VOU DAR UM PASSEIO DE...", "BICECLETA", "BECICLETA", "BECECLETA", "BICICLETA"]
        self.x5 = ["É SEMPRE UM ... RECEBÊ-LO(A) EM MINHA CASA!", "PRASER", "PRAZÊ", "PRASÊ", "PRAZER"]

        if self.x and self.x2 and self.x3 and self.x4 and self.x5 in questoes:
            self.botDeletar_adicionar.configure(text='QUESTÕES PADRÕES: ON ')
        else:
            self.botDeletar_adicionar.configure(text='QUESTÕES PADRÕES: OFF')

    def limparBanco(self):
        if self.x and self.x2 and self.x3 and self.x4 and self.x5 in questoes:
            self.botDeletar_adicionar.configure(text='QUESTÕES PADRÕES: OFF')
            messagebox.showinfo('LIMPO!', 'AS QUESTÕES PADRÕES FORAM RETIRADAS!')
            questoes.remove(["IREI AO RESTAURANTE...", "ALMOSSAR", "AUMOÇAR", "AUMOSSAR", "ALMOÇAR"])
            questoes.remove(["IREI CONTATAR MEU...", "ADEVOGADO", "ADIVOGADO", "ADIVOGADU", "ADVOGADO"])
            questoes.remove(["COMPREI 200 GRAMAS DE...", "MORTADELLA", "MORTANDELA", "MOTADELA", "MORTADELA"])
            questoes.remove(["VOU DAR UM PASSEIO DE...", "BICECLETA", "BECICLETA", "BECECLETA", "BICICLETA"])
            questoes.remove(["É SEMPRE UM ... RECEBÊ-LO(A) EM MINHA CASA!", "PRASER", "PRAZÊ", "PRASÊ", "PRAZER"])

        else:
            self.retornar_questoes()

    def retornar_questoes(self):

        self.botDeletar_adicionar.configure(text='QUESTÕES PADRÕES: ON ')
        messagebox.showinfo('OK!', 'AS QUESTÕES PADRÕES FORAM ADICIONADAS!')
        questoes.append(["IREI AO RESTAURANTE...", "ALMOSSAR", "AUMOÇAR", "AUMOSSAR", "ALMOÇAR"])
        questoes.append(["IREI CONTATAR MEU...", "ADEVOGADO", "ADIVOGADO", "ADIVOGADU", "ADVOGADO"])
        questoes.append(["COMPREI 200 GRAMAS DE...", "MORTADELLA", "MORTANDELA", "MOTADELA", "MORTADELA"])
        questoes.append(["VOU DAR UM PASSEIO DE...", "BICECLETA", "BECICLETA", "BECECLETA", "BICICLETA"])
        questoes.append(["É SEMPRE UM ... RECEBÊ-LO(A) EM MINHA CASA!", "PRASER", "PRAZÊ", "PRASÊ", "PRAZER"])

    def hover3(self, e):
        soundhover.play()
        self.BotAdicionar.configure(bg='green')

    def hover_leave3(self, e):
        self.BotAdicionar.configure(bg='#003300')

    def hover4(self, e):
        soundhover.play()
        self.BotFechar.configure(bg='red')

    def hover_leave4(self, e):
        self.BotFechar.configure(bg='#990000')

    def quitp(self):
        sound.play()
        s = Menu2()
        l = Personalizado()

    def adicionando(self):

        sound.play()

        b1 = self.box1.get()
        b2 = self.box2.get()
        b3 = self.box3.get()
        b4 = self.box4.get()
        b5 = self.box5.get()

        self.novas = [b1, b2, b3, b4, b5]

        if b1 == '':
            messagebox.showerror("ERRO", "VOCÊ NÃO PREENCHEU TODOS OS CAMPOS!", parent=janela)

        elif b2 == '':
            messagebox.showerror("ERRO", "VOCÊ NÃO PREENCHEU TODOS OS CAMPOS!", parent=janela)

        elif b3 == '':
            messagebox.showerror("ERRO", "VOCÊ NÃO PREENCHEU TODOS OS CAMPOS!", parent=janela)

        elif b4 == '':
            messagebox.showerror("ERRO", "VOCÊ NÃO PREENCHEU TODOS OS CAMPOS!", parent=janela)

        elif b5 == '':
            messagebox.showerror("ERRO", "VOCÊ NÃO PREENCHEU TODOS OS CAMPOS!", parent=janela)

        else:
            questoes.append(self.novas)
            self.box1.delete(0, END)
            self.box2.delete(0, END)
            self.box3.delete(0, END)
            self.box4.delete(0, END)
            self.box5.delete(0, END)
            messagebox.showinfo("SUCESSO", "QUESTÃO ADICIONADA COM SUCESSO!", parent=janela)


# OPÇÃO DE JOGADOR
class ModoDeJogo:
    def __init__(self):
        self.fundo = PhotoImage(file='imagens/fundomodo.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        # ------------------------------------  BOTÃO DE PROFESSOR  ----------------------------------- #

        self.Professor = Button(janela, text="PROFESSOR",
                                padx=17, pady=19, width=20,
                                font=('BigNoodleTitling', 26),
                                bg='#e6ac00', fg='black',
                                activebackground='#006622',
                                activeforeground='white', command=criarTelaLogin)
        self.Professor.place(x=250, y=120)

        # -------------------------------------   BOTÃO DE ALUNO   ------------------------------------ #

        self.Aluno = Button(janela, text="ALUNO",
                            padx=17, pady=19, width=20,
                            font=('BigNoodleTitling', 26),
                            bg='#e6ac00', fg='black',
                            activebackground='#006622',
                            activeforeground='white', command=self.criarMenuAluno)
        self.Aluno.place(x=250, y=270)

        # ------------------------------------   BOTÃO DE VOLTAR   ------------------------------------- #

        self.Sair = Button(janela, text="Sair",
                           padx=17, pady=19, width=20,
                           font=('BigNoodleTitling', 26),
                           bg='#e6ac00', fg='black',
                           activebackground='#b30000',
                           activeforeground='white', command=quit)
        self.Sair.place(x=250, y=420)

        self.Professor.bind('<Enter>', self.hover7)
        self.Professor.bind('<Leave>', self.hover_leave7)

        self.Aluno.bind('<Enter>', self.hover8)
        self.Aluno.bind('<Leave>', self.hover_leave8)

        self.Sair.bind('<Enter>', self.hover9)
        self.Sair.bind('<Leave>', self.hover_leave9)

    def hover7(self, e):
        soundhover.play()
        self.Professor.configure(bg='white')

    def hover_leave7(self, e):
        self.Professor.configure(bg='#e6ac00')

    def hover8(self, e):
        soundhover.play()
        self.Aluno.configure(bg='white')

    def hover_leave8(self, e):
        self.Aluno.configure(bg='#e6ac00')

    def hover9(self, e):
        soundhover.play()
        self.Sair.configure(bg='white')

    def hover_leave9(self, e):
        self.Sair.configure(bg='#e6ac00')

    def criarMenuAluno(self):
        sound.play()
        m = Menu()

    def criarMenuProfessor(self):
        sound.play()
        m = Menu2()
        p = Personalizado()

    def quit(self):
        sound.play()
        janela.quit()


# LOGAR OU CADASTRAR NO JOGO
class Login:
    def __init__(self):

        self.fundo = PhotoImage(file='imagens/bglogin.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        self.entry_login = Entry(janela, width=36, font=('bahnschrift', 19))
        self.entry_login.place(x=270, y=120)

        self.entry_senha = Entry(janela, width=36, show='*', font=('bahnschrift', 19))
        self.entry_senha.place(x=270, y=190)

        # ----------------------------------------- BOTÃO DE LOGIN ---------------------------------------- #

        self.blogin = Button(janela, text="LOGIN",
                             padx=17, pady=19, width=20,
                             font=('BigNoodleTitling', 23),
                             bg='#e6ac00', fg='black',
                             activebackground='#660080',
                             activeforeground='white', command=self.login)
        self.blogin.place(x=270, y=285)

        # ----------------------------------------- BOTÃO DE CADASTRO ---------------------------------------- #

        self.bcadastro = Button(janela, text="FAÇA SEU CADASTRO",
                                padx=5, pady=5, width=20,
                                font=('BigNoodleTitling', 23),
                                bg='#e6ac00', fg='black',
                                activebackground='#660080',
                                activeforeground='white', command=self.cadastro)
        self.bcadastro.place(x=26, y=500)

        # ----------------------------------------- BOTÃO DE VOLTAR ---------------------------------------- #

        self.bvoltar = Button(janela, text="<------",
                              padx=2, pady=2, width=10,
                              font=('BigNoodleTitling', 10),
                              bg='#e6ac00', fg='black',
                              activebackground='#660080',
                              activeforeground='white', command=criarmododejogo)
        self.bvoltar.place(x=10, y=5)

        # ----------------------------------------- BOTÃO DE RECUPERAR SENHA ---------------------------------------- #

        self.brecuperar_senha = Button(janela, text="RECUPERAR SENHA",
                                       padx=5, pady=5, width=20,
                                       font=('BigNoodleTitling', 23),
                                       bg='#e6ac00', fg='black',
                                       activebackground='#660080',
                                       activeforeground='white', command=self.iniciarRecuperar_senha)
        self.brecuperar_senha.place(x=535, y=500)

        self.blogin.bind('<Enter>', self.hover10)
        self.blogin.bind('<Leave>', self.hover_leave10)
        self.bcadastro.bind('<Enter>', self.hover11)
        self.bcadastro.bind('<Leave>', self.hover_leave11)
        self.bvoltar.bind('<Enter>', self.hover12)
        self.bvoltar.bind('<Leave>', self.hover_leave12)
        self.brecuperar_senha.bind('<Enter>', self.hover13)
        self.brecuperar_senha.bind('<Leave>', self.hover_leave13)

    def hover10(self, e):
        soundhover.play()
        self.blogin.configure(bg='white')

    def hover_leave10(self, e):
        self.blogin.configure(bg='#e6ac00')

    def hover11(self, e):
        soundhover.play()
        self.bcadastro.configure(bg='white')

    def hover_leave11(self, e):
        self.bcadastro.configure(bg='#e6ac00')

    def hover12(self, e):
        soundhover.play()
        self.bvoltar.configure(bg='white')

    def hover_leave12(self, e):
        self.bvoltar.configure(bg='#e6ac00')

    def hover13(self, e):
        soundhover.play()
        self.brecuperar_senha.configure(bg='white')

    def hover_leave13(self, e):
        self.brecuperar_senha.configure(bg='#e6ac00')

    def iniciarRecuperar_senha(self):
        self.fundo3 = PhotoImage(file='imagens/bgrecuperarsenha2.png')
        Label(janela, image=self.fundo3).place(relwidth=1, relheight=1)

        self.bvoltar = Button(janela, text="<------",
                              padx=2, pady=2, width=10,
                              font=('BigNoodleTitling', 10),
                              bg='#e6ac00', fg='black',
                              activebackground='#660080',
                              activeforeground='white', command=criarTelaLogin)
        self.bvoltar.place(x=10, y=5)

        self.entry_usuarioRecuperar = Entry(janela, width=40, font=('bahnschrift', 20),
                                            justify='center')
        self.entry_usuarioRecuperar.place(x=105, y=150)

        self.bcadastro = Button(janela, text="OK",
                                padx=3, pady=3, width=20,
                                font=('BigNoodleTitling', 23),
                                bg='#e6ac00', fg='black',
                                activebackground='#660080',
                                activeforeground='white', command=self.conferirdados)
        self.bcadastro.place(x=280, y=220)

        self.bcadastro.bind('<Enter>', self.hover11)
        self.bcadastro.bind('<Leave>', self.hover_leave11)
        self.bvoltar.bind('<Enter>', self.hover12)
        self.bvoltar.bind('<Leave>', self.hover_leave12)

    def login(self):

        with sqlite3.connect('escrevabem.db') as dados:
            c = dados.cursor()

        find_user = 'SELECT * FROM cadastros WHERE email = ? and senha = ? or usuario = ? and senha = ?'
        c.execute(find_user, [(self.entry_login.get()), (self.entry_senha.get()), (self.entry_login.get()),
                              (self.entry_senha.get())])
        result = c.fetchall()

        if not result:
            messagebox.showerror('ALGO ERRADO!', 'CONFIRA SUAS INFORMAÇÕES NOVAMENTE!')

        elif self.entry_login.get() == '' or self.entry_senha.get() == '':
            messagebox.showerror('ERRO!', 'PREENCHA OS CAMPOS!')

        else:
            shownome = 'select nome from cadastros where usuario = ? or email = ?'
            c.execute(shownome, [self.entry_login.get(), self.entry_login.get()])
            mostrarnome = c.fetchall()

            messagebox.showinfo('TUDO CERTO!', f'BEM VINDO(A) {mostrarnome}!')
            voltarMenuProfessor()

    def conferirdados(self):
        with sqlite3.connect('escrevabem.db') as dados:
            c = dados.cursor()

        coletar = 'select usuario or email from cadastros where usuario = ? or email = ?'
        c.execute(coletar, [self.entry_usuarioRecuperar.get(), self.entry_usuarioRecuperar.get()])
        dados_corretos = c.fetchall()

        if self.entry_usuarioRecuperar.get() == '':
            messagebox.showerror('ERRO', 'PREENCHA O CAMPO!')

        elif not dados_corretos:
            messagebox.showerror('ERRO', 'ESTE USUÁRIO/EMAIL NÃO ESTÁ CADASTRADO')

            self.EntryPergunta.destroy()
            self.EntryResposta.destroy()
            self.Enviar.destroy()
            self.Fechar.destroy()

        else:

            with sqlite3.connect('escrevabem.db') as dados:
                c = dados.cursor()

            pegarpergunta = 'select pergunta from cadastros where usuario = ? or email = ?'
            c.execute(pegarpergunta, (self.entry_usuarioRecuperar.get(), self.entry_usuarioRecuperar.get()))
            showpergunta = c.fetchall()

            self.EntryPergunta = Entry(janela, font=('bignoodletitling', 30), bg='#f7ac00',
                                       fg='black', justify='center', width=53)
            self.EntryPergunta.place(x=0, y=313)
            self.EntryPergunta.insert(END, showpergunta)

            self.EntryResposta = Entry(janela, font=('bahnschrift', 20), justify='center', width=34)
            self.EntryResposta.place(x=260, y=420)

            self.Enviar = Button(janela, text="ENVIAR", width=20, height=1,
                                 font=('BigNoodleTitling', 25),
                                 bg='#003300', fg='white',
                                 activebackground='#006622',
                                 activeforeground='white', command=self.nova_senha)
            self.Enviar.place(x=130, y=520)

            self.Fechar = Button(janela, text="FECHAR", width=20, height=1,
                                 font=('BigNoodleTitling', 25),
                                 bg='#990000', fg='white',
                                 activebackground='#e60000',
                                 activeforeground='white', command=self.iniciarRecuperar_senha)
            self.Fechar.place(x=420, y=520)

            self.Enviar.bind('<Enter>', self.hover3)
            self.Enviar.bind('<Leave>', self.hover_leave3)
            self.Fechar.bind('<Enter>', self.hover4)
            self.Fechar.bind('<Leave>', self.hover_leave4)

    def hover3(self, e):
        soundhover.play()
        self.Enviar.configure(bg='green')

    def hover_leave3(self, e):
        self.Enviar.configure(bg='#003300')

    def hover4(self, e):
        soundhover.play()
        self.Fechar.configure(bg='red')

    def hover_leave4(self, e):
        self.Fechar.configure(bg='#990000')

    def nova_senha(self):
        with sqlite3.connect('escrevabem.db') as dados:
            c = dados.cursor()

        coletar = 'select resposta from cadastros where resposta = ? and usuario = ? or resposta = ? and email = ?'
        c.execute(coletar, [self.EntryResposta.get(), self.entry_usuarioRecuperar.get(), self.EntryResposta.get(),
                            self.entry_usuarioRecuperar.get()])
        dados_corretos = c.fetchall()

        if self.EntryResposta.get() == '':
            messagebox.showerror('ERRO', 'RESPONDA A PERGUNTA!')

        elif not dados_corretos:
            messagebox.showerror('ERRO', 'RESPOSTA INCORRETA!')

        else:

            messagebox.showinfo('TUDO CERTO', 'RESPOSTA CORRETA! REDEFINA SUA SENHA!')

            self.fundo3 = PhotoImage(file='imagens/bgnovasenha.png')
            Label(janela, image=self.fundo3).place(relwidth=1, relheight=1)

            self.entry_nova_senha = Entry(janela, width=40, font=('bahnschrift', 20),
                                          justify='center', show='*')
            self.entry_nova_senha.place(x=105, y=139)

            self.entry_nova_senha2 = Entry(janela, width=40, font=('bahnschrift', 20),
                                           justify='center', show='*')
            self.entry_nova_senha2.place(x=105, y=317)

            self.redefinir = Button(janela, text="ok", width=20, padx=12, pady=12,
                                    font=('BigNoodleTitling', 22),
                                    bg='#e6ac00', fg='black',
                                    activebackground='#006622',
                                    activeforeground='white', command=self.conferir_nova_senha)
            self.redefinir.place(x=260, y=390)

            self.botcancelar = Button(janela, text="cancelar",
                                      padx=12, pady=12, width=20,
                                      font=('BigNoodleTitling', 22),
                                      bg='#e6ac00', fg='black',
                                      activebackground='#b30000',
                                      activeforeground='white', command=self.iniciarRecuperar_senha)
            self.botcancelar.place(x=260, y=490)

            self.redefinir.bind('<Enter>', self.hover7)
            self.redefinir.bind('<Leave>', self.hover_leave7)
            self.botcancelar.bind('<Enter>', self.hover8)
            self.botcancelar.bind('<Leave>', self.hover_leave8)

    def hover7(self, e):
        soundhover.play()
        self.redefinir.configure(bg='green', fg='white')

    def hover_leave7(self, e):
        self.redefinir.configure(bg='#e6ac00', fg='black')

    def hover8(self, e):
        soundhover.play()
        self.botcancelar.configure(bg='red', fg='white')

    def hover_leave8(self, e):
        self.botcancelar.configure(bg='#e6ac00', fg='black')

    def conferir_nova_senha(self):
        with sqlite3.connect('escrevabem.db') as dados:
            c = dados.cursor()

        coletar = 'update cadastros set senha = ? where usuario = ? or email = ?'
        c.execute(coletar,
                  [self.entry_nova_senha.get(), self.entry_usuarioRecuperar.get(), self.entry_usuarioRecuperar.get()])
        c.fetchall()

        if self.entry_nova_senha.get() == '' or self.entry_nova_senha2.get() == '':
            messagebox.showerror('ERRO', 'PREENCHA OS CAMPOS DE SENHA!')

        elif self.entry_nova_senha.get() != self.entry_nova_senha2.get():
            messagebox.showerror('ERRO', 'AS SENHAS NÃO COINCIDEM!')

        else:
            messagebox.showinfo('SUCESSO', 'SUA SENHA FOI REDEFINIDA!')
            dados.commit()
            l = criarTelaLogin()

    def cadastro(self):

        self.fundo = PhotoImage(file='imagens/bgcadastro.png')
        Label(janela, image=self.fundo).place(relwidth=1, relheight=1)

        self.entry_nome = Entry(janela, width=39, font=('bahnschrift', 19))
        self.entry_nome.place(x=210, y=25)

        self.entry_usuario = Entry(janela, width=39, font=('bahnschrift', 19))
        self.entry_usuario.place(x=210, y=87)

        self.entry_email = Entry(janela, width=39, font=('bahnschrift', 19))
        self.entry_email.place(x=210, y=148)

        self.entry_senha = Entry(janela, width=39, font=('bahnschrift', 19), show='*')
        self.entry_senha.place(x=210, y=210)

        self.entry_pergunta = Entry(janela, width=39, font=('bahnschrift', 21), justify='center')
        self.entry_pergunta.place(x=100, y=345)

        self.entry_resposta = Entry(janela, width=39, font=('bahnschrift', 21), justify='center')
        self.entry_resposta.place(x=100, y=437)

        # ----------------------------------------- BOTÃO DE CADASTRAR ---------------------------------------- #

        self.bcadastrar = Button(janela, text="CADASTRAR",
                                 width=20, height=1,
                                 font=('BigNoodleTitling', 25),
                                 bg='#e6ac00', fg='black',
                                 activebackground='#660080',
                                 activeforeground='white', command=self.efetuarCadastro)
        self.bcadastrar.place(x=125, y=520)

        # ----------------------------------------- BOTÃO DE VOLTAR ---------------------------------------- #

        self.bvolte = Button(janela, text="VOLTAR",
                             width=20, height=1,
                             font=('BigNoodleTitling', 25),
                             bg='#e6ac00', fg='black',
                             activebackground='#660080',
                             activeforeground='white', command=criarTelaLogin)
        self.bvolte.place(x=420, y=520)

        self.bcadastrar.bind('<Enter>', self.hover5)
        self.bcadastrar.bind('<Leave>', self.hover_leave5)
        self.bvolte.bind('<Enter>', self.hover6)
        self.bvolte.bind('<Leave>', self.hover_leave6)

    def hover5(self, e):
        soundhover.play()
        self.bcadastrar.configure(bg='green')

    def hover_leave5(self, e):
        self.bcadastrar.configure(bg='#e6ac00')

    def hover6(self, e):
        soundhover.play()
        self.bvolte.configure(bg='red')

    def hover_leave6(self, e):
        self.bvolte.configure(bg='#e6ac00')

    def efetuarCadastro(self):
        with sqlite3.connect('escrevabem.db') as dados:
            c = dados.cursor()

        find_user = 'SELECT email FROM cadastros WHERE email = ?'
        c.execute(find_user, [(self.entry_email.get())])
        if c.fetchall():
            messagebox.showerror('ERRO', 'USUARIO/EMAIL JÁ CADASTRADO!')

        elif self.entry_email.get() == '' or self.entry_usuario.get() == '' or self.entry_senha.get() == '' or self.entry_pergunta.get() == '' or self.entry_resposta.get() == '':
            messagebox.showerror('ERRO', 'PREENCHA TODOS OS CAMPOS!')

        else:
            find_user2 = 'SELECT usuario FROM cadastros WHERE usuario = ?'
            c.execute(find_user2, [(self.entry_usuario.get())])

            if c.fetchall():
                messagebox.showerror('ERRO', 'USUARIO/EMAIL JÁ CADASTRADO!')
            else:
                messagebox.showinfo('SUCESSO', 'CONTA CRIADA!')
                insert = 'INSERT INTO cadastros(nome,usuario,email,senha, pergunta,resposta) VALUES(?,?,?,?,?,?)'
                c.execute(insert, [(self.entry_nome.get()), (self.entry_usuario.get()), (self.entry_email.get()),
                                   (self.entry_senha.get()), (self.entry_pergunta.get()), (self.entry_resposta.get())])
                dados.commit()
                l = Login()


def voltarMenuAluno():
    sound.play()
    m = Menu()


def voltarMenuProfessor():
    sound.play()
    musicaJogo()
    m = Menu2()
    p = Personalizado()


def criarmododejogo():
    m = ModoDeJogo()
    pygame.mixer.music.stop()


def voltarmododejogo():
    sound.play()
    pygame.mixer.music.stop()
    m = ModoDeJogo()


def confirma_retornar():
    m = messagebox.askyesno('ATENÇÃO', 'VOCÊ SERÁ DESLOGADO(A) SE CONTINUAR! DESEJA PROSSEGUIR?')
    if m:
        voltarmododejogo()


def criarTelaLogin():
    l = Login()


def sairTelaLogin():
    m = ModoDeJogo()


criarmododejogo()
janela.mainloop()
