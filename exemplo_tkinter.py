# importando o módulo tkinter (biblioteca padrão do Python para criar interfaces gráficas)
from tkinter import * 
# importando o módulo ttk (submódulo do tkinter, necessário pra usar temas, por exemplo)
from tkinter import ttk

def Calcular(*args): # função que converte Fahrenheit para Celsius
    fahrenheit = float(graus_fahrenheit.get()) # obtendo o valor em Fahrenheit
    celsius = (fahrenheit - 32) * 5/9 # convertendo Fahrenheit para Celsius
    graus_celsius.set(round(celsius, 2)) # exibindo o valor em Celsius com 2 casas decimais

root = Tk() # criando a janela principal do aplicativo
root.title("Conversor de Fahrenheit para Celsius") # título da janela

mainframe = ttk.Frame(root, padding="3 3 12 12") # criando um frame (container) para os widgets
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) # posicionando o frame na janela

# configurando a coluna e a linha do frame (serve pra redimensionar a janela)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

graus_fahrenheit = StringVar() # variável que armazena o valor em Fahrenheit
fahrenheit_entry = ttk.Entry(mainframe, width=7, textvariable=graus_fahrenheit) # campo de entrada para o valor em Fahrenheit
fahrenheit_entry.grid(column=2, row=1, sticky=(W, E)) # posicionando o campo de entrada

graus_celsius = StringVar() # variável que armazena o valor em Celsius
ttk.Label(mainframe, textvariable=graus_celsius).grid(column=2, row=2, sticky=(W, E)) # rótulo para o valor em Celsius

ttk.Button(mainframe, text="Calcular", command=Calcular).grid(column=3, row=3, sticky=W) # botão para calcular

ttk.Label(mainframe, text="°F").grid(column=3, row=1, sticky=W) # rótulo para o valor em Fahrenheit
ttk.Label(mainframe, text="é equivalente a").grid(column=1, row=2, sticky=E) # rótulo para a equivalência
ttk.Label(mainframe, text="°C").grid(column=3, row=2, sticky=W) # rótulo para o valor em Celsius

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5) # percorre todos os componentes e configura o espaçamento entre eles
fahrenheit_entry.focus() # foca no campo de entrada
root.bind("<Return>", Calcular) # atalho para o botão Calcular

root.mainloop() # loop principal do aplicativo, necessário pras coisas aparecerem na tela