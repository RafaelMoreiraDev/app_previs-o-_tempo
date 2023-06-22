# Rodar o script abaixo no terminal
# pip install -r requirements.txt

from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk

# Importações
import requests
from datetime import datetime
import pytz
import pycountry_convert as pc

from translate import Translator
#### Cores ####
co0 = "#444466" #Preto
co1 = "#feffff" # Branco
co2 = "#6f9fbd" # Azul

fundo_dia = "#6cc4cc" 
fundo_noite = "#484f60"
fundo_tarde = "#bfb86d"
fundo = fundo_dia

janela = Tk()
janela.title("")
janela.geometry("320x350")
janela.configure(bg=fundo)
ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

# Criando frames
frame_top = Frame(janela, width=320, height=50, bg=co1, pady=0,padx=0)
frame_top.grid(row=1, column=0 )

frame_corpo = Frame(janela, width=320, height=300, bg=fundo, pady=12,padx=0)
frame_corpo.grid(row=2, column=0 , sticky=NW)

estilo = ttk.Style(janela)
estilo.theme_use("clam")

# Função que retorna as informações
def informacao():
    
    # Api que não funciona
    chave = "78303bb5e0b8d95715a10d27ec644eac"
    cidade = e_local.get()
    api_link = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(cidade,chave)

    # Fazendo a chamada da API usando request
    r = requests.get(api_link)

    # Convertendo os dados presentes na variavel r em dicionario
    dados = r.json()

    print(dados)
    # Obtendo zona, país, horas:
    pais_codido = dados["sys"]["country"]
    
    # --- Zona ---
    zona_fuso = pytz.country_timezones[pais_codido]
    
    # --- Pais ---
    pais = pytz.country_names[pais_codido]

    #  --- data ---
    zona = pytz.timezone(zona_fuso[0])

    zona_horas = datetime.now().strftime("%d/%m/%y | %I:%M %p")

 

    # --- Tempo ---
    tempo = dados["main"]["temp"]
    pressao = dados["main"]["pressure"]
    umidade = dados["main"]["humidity"]
    velocidade = dados["wind"]["speed"]
    descricao = dados["weather"][0]["description"]
    tradutor = Translator(to_lang="pt")
    descricao = tradutor.translate(descricao)

    # Mudando informações
        
    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continent_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continent_codigo)
        
        return pais_continente_nome

    continente = pais_para_continente(pais)
    
    

    # Passando informações nas Labels
    #cidade
    l_cidade["text"]= cidade +" - "+ pais + " / " + continente
    # Data
    l_data["text"] = zona_horas
    # umidade do ar
    l_umidade["text"]= umidade
    # Pressão
    l_pressao["text"] = (f"Pressão: {pressao}")
    #velovidade do vento
    l_velocidade_v["text"] = (f"Vel. Vento: {velocidade}")
    # Descrição
    l_tempo_agora["text"] = descricao
    # temperatura
    l_temper["text"] = ((f"Temperatura: {int(tempo-273.15)}"))
    
    l_umid_simb["text"] ="%"
    
    l_umid_nome["text"] = "Umidade:"
    
    
    # Logica para trocar o BG
    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime("%H")
    
    global imagem
    
    zona_periodo = int(zona_periodo)
    if zona_periodo <=5:
        
        imagem = Image.open("img/lua.png")
        fundo = fundo_noite
        
    elif zona_periodo <=11:
        imagem = Image.open("img/sol_manha.png")
        fundo = fundo_dia
        
    elif zona_periodo <=18:
        imagem = Image.open("img/sol_tarde.png")
        fundo = fundo_tarde
        
    elif zona_periodo <=23:
        imagem = Image.open("img/lua.png")
        fundo = fundo_noite
    else:
        pass
        
    imagem = imagem.resize((130,130))
    imagem = ImageTk.PhotoImage(imagem)

    l_icone = Label(frame_corpo, image=imagem, bg=fundo)
    l_icone.place(x=162, y=50)
    
    
        # Passando informações nas Labels
        
    janela.configure(bg=fundo)
    frame_top.configure(bg=fundo)
    frame_corpo.configure(bg=fundo)
    #cidade
    l_cidade["bg"]= fundo   
    # Data
    l_data["bg"] = fundo
    # umidade do ar
    l_umidade["bg"]= fundo    
    # Pressão
    l_pressao["bg"] = fundo
    #velovidade do vento
    l_velocidade_v["bg"] = fundo
    # Descrição
    l_tempo_agora["bg"] = fundo
    # temperatura
    l_temper["bg"] = fundo
    l_umid_nome["bg"] = fundo
    l_umid_simb["bg"] = fundo
    
    
    
#configurando o frame top

# caixa de pesquisa
e_local = Entry(frame_top, width=20, justify="left", font=("", 14), highlightthickness=1, relief="solid")
e_local.place(x=15, y=10)

# botão de pesquisa
b_ver = Button(frame_top,command=informacao,text="Ver Clima", bg=co1, fg=co2, font=("Ivy 9 bold"), relief="raised", overrelief=RIDGE )
b_ver.place(x=250, y=10)

#configurando o frame corpo
# nome da cidade - pais- continente
l_cidade = Label(frame_corpo, anchor="center",  bg=fundo, fg=co1, font=("Arial 14"))
l_cidade.place(x=10, y=4)\

# Data hora 
l_data = Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 10"))
l_data.place(x=10, y=54)

# Umidade do ar
l_umidade = Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 40"))
l_umidade.place(x=10, y=90)

l_umid_simb = Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 10 bold"))
l_umid_simb.place(x=85, y=95)

l_umid_nome = Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 8"))
l_umid_nome.place(x=85, y=125)
# Pressão
l_pressao= Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 10"))
l_pressao.place(x=10, y=164)
#velovidade do vento
l_velocidade_v= Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 10"))
l_velocidade_v.place(x=10, y=192)
# Tempo agora
l_temper= Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 10"))
l_temper.place(x=10, y=230)



l_tempo_agora= Label(frame_corpo,text="", anchor="center",  bg=fundo, fg=co1, font=("Arial 10"))
l_tempo_agora.place(x=170, y=190)

janela.mainloop()