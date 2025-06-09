import ply.lex as lex
import ply.yacc as yacc
import pandas as pd
import matplotlib.pyplot as plt
import os

dataframes = {}

# PALAVRAS RESERVADAS ADAPTADAS PARA PANDAS / ANÁLISE DE DADOS
reserved = {
    'carregar': 'CARREGAR',       # Para ler arquivos
    'arquivo': 'ARQUIVO',         # Representa arquivos como CSV, Excel
    'como': 'COMO',               # Alias (equivalente a "as")

    'juntar': 'JUNTAR',           # concat ou merge
    'com': 'COM',                 # para juntar com base em colunas
    'filtrar': 'FILTRAR',         # operações com filtros
    'onde': 'ONDE',               # cláusulas de condição

    'soma': 'SOMA',
    'media': 'MEDIA',
    'minimo': 'MINIMO',
    'maximo': 'MAXIMO',
    'contagem': 'CONTAGEM',
    'descricao': 'DESCRICAO',     # describe()
    'shape': 'SHAPE',

    'selecione': 'SELECIONE',
    'de': 'DE',
    'para': 'PARA',
    'função': 'FUNCAO',
    'classe': 'CLASSE',
    'comando' : 'COMANDO',
    
    'grafico': 'GRAFICO',
    'pizza': 'PIZZA',
    'barras': 'BARRAS'
}

tokens = (
    # LITERAIS
    'ID',
    'NUMINT', 
    'NUMDEC',
    'STRING',

    # OPERADORES MATEMÁTICOS
    'MAIS',
    'MENOS',
    'VEZES',
    'DIVIDIR',

    # OPERADORES DE COMPARAÇÃO
    'MAIORQ',
    'MENOQ',
    'MAIORGUAL',
    'MENORIGUAL',
    'IGUAL',
    'DIFERENTE',
    'AND',
    'OR',
    'NOT',

    # ATRIBUIÇÃO
    'RECEBE',

    # DELIMITADORES
    'PARENESQ',
    'PARENDIR',
    'DOISPONTOS',
    'COLCHETEESQ',
    'COLCHETEDIR',  
    'CHAVEESQ', 
    'CHAVEDIR', 
    'VIRGULA',
    'PONTO',
    'PONTOVIRGULA',
    
    #GRAFICO
    'GRAFICO',
    'PIZZA',
) + tuple(reserved.values())

# EXPRESSÕES REGULARES

t_MAIS    = r'\+'
t_MENOS   = r'-'
t_VEZES   = r'\*'
t_DIVIDIR  = r'/'

t_MAIORQ = r'>'
t_MENOQ = r'<'
t_MAIORGUAL = r'>='
t_MENORIGUAL = r'<='
t_IGUAL = r'=='
t_DIFERENTE = r'!='

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

t_RECEBE = r'='

t_PARENESQ  = r'\('
t_PARENDIR  = r'\)'
t_DOISPONTOS = r':'
t_COLCHETEESQ = r'\['
t_COLCHETEDIR = r'\]'
t_CHAVEESQ = r'\{'
t_CHAVEDIR = r'\}'
t_VIRGULA = r','
t_PONTO = r'\.'
t_PONTOVIRGULA = r';'

# LITERAIS

t_NUMINT = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
t_NUMDEC = r'((\d+)(\.\d+)(e(\+|-)?(\d+))?|(\d+)e(\+|-)?(\d+))([lL]|[fF])?'
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# IDENTIFICADOR + VERIFICAÇÃO DE PALAVRA RESERVADA
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # usa minúsculas para casar com reserved
    return t

# NOVA LINHA
def t_novalinha(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# COMENTÁRIOS
def t_COMENTARIO(t):
    r'\#.*'
    pass  # ignora comentários

# IGNORA ESPAÇOS E TABULAÇÕES
t_ignore = ' \t'

# ERROS
def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# CONSTRUIR O LEXER
lexer = lex.lex()

########################################################################################################################################

saidas = []

def p_program(p):
    '''program : program expression
               | expression'''
    pass


def p_comando_carregar(p):
    '''expression : CARREGAR STRING COMO ID'''
    global dataframes

    caminho_arquivo = p[2].strip('"')  # Remove as aspas
    diretorio_atual = os.path.dirname(__file__)
    caminho_arquivo = os.path.join(diretorio_atual, caminho_arquivo)

    df = pd.read_excel(caminho_arquivo)
    dataframes[p[4]] = df
    print(f"Arquivo '{caminho_arquivo}' carregado como '{p[4]}'.")

def p_comando_media(p):
    '''expression : MEDIA DE ID PARA ID'''
    global dataframes

    df_name = p[3]
    coluna = p[5]
    if df_name in dataframes:
        media = dataframes[df_name][coluna].mean()
        saidas.append(f"Média da coluna '{coluna}' em {df_name}: {media}")
    else:
        saidas.append(f"DataFrame '{df_name}' não encontrado.")

def p_comando_soma(p):
    '''expression : SOMA DE ID PARA ID'''
    global dataframes

    df_name = p[3]
    coluna = p[5]
    if df_name in dataframes:
        soma = dataframes[df_name][coluna].sum()
        saidas.append(f"Soma da coluna '{coluna}' em {df_name}: {soma}")
    else:
        saidas.append(f"DataFrame '{df_name}' não encontrado.")

def p_comando_descricao(p):
    '''expression : DESCRICAO DE ID'''
    global dataframes

    df_name = p[3]
    if df_name in dataframes:
        txt = f"Descrição do DataFrame '{df_name}':\n {dataframes[df_name].describe()}"
        saidas.append(txt)
    else:
        saidas.append(f"DataFrame '{df_name}' não encontrado.")

def p_comando_descricao(p):
    '''expression : SHAPE DE ID'''
    global dataframes

    df_name = p[3]
    if df_name in dataframes:
        txt = f"Shape do DataFrame '{df_name}':\n {dataframes[df_name].shape}"
        saidas.append(txt)
    else:
        saidas.append(f"DataFrame '{df_name}' não encontrado.")

def p_comando_filtrar(p):
    '''expression : FILTRAR ID ONDE ID MAIORQ NUMINT'''
    global dataframes

    df_name = p[2]
    coluna = p[4]
    valor = int(p[6])
    if df_name in dataframes:
        resultado = dataframes[df_name][dataframes[df_name][coluna] > valor]
        txt = f"Filtrando '{df_name}' onde {coluna} > {valor}:\n{resultado}"
        saidas.append(txt)
    else:
        saidas.append(f"DataFrame '{df_name}' não encontrado.")

def p_comando_selecione_colunas(p):
    'expression : SELECIONE lista_colunas DE ID'
    global dataframes
    colunas = p[2]
    nome = p[4]
    if nome in dataframes:
        saidas.append(dataframes[nome][colunas])
    else:
        saidas.append(f"DataFrame '{nome}' não encontrado.")

def p_lista_colunas(p):
    '''lista_colunas : lista_colunas VIRGULA ID
                     | ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_error(p):
    print("Erro de sintaxe.")

############################################################################################################################3
#plotar graficos

def p_comando_grafico(p):
    '''expression : GRAFICO DE BARRAS DE ID PARA ID'''
    global dataframes
    df_name = p[5]
    coluna = p[7]
    if df_name in dataframes:
        df = dataframes[df_name]
        if coluna in df.columns:
            df[coluna].plot(kind='bar', title=f"Gráfico de {coluna} - {df_name}")
            plt.xlabel("Índice")
            plt.ylabel(coluna)
            plt.tight_layout()
            plt.show()
        else:
            print(f"Coluna '{coluna}' não encontrada em {df_name}.")
    else:
        print(f"DataFrame '{df_name}' não encontrado.")
        
def p_comando_grafico_pizza(p):
    '''expression : GRAFICO DE PIZZA DE ID PARA ID VIRGULA ID'''
    global dataframes
    df_name = p[5]
    label_col = p[7]
    value_col = p[9]
    if df_name in dataframes:
        df = dataframes[df_name]
        if label_col in df.columns and value_col in df.columns:
            labels = df[label_col].astype(str)
            sizes = df[value_col]
            plt.figure(figsize=(6, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title(f"Gráfico de Pizza: {value_col} por {label_col}")
            plt.axis('equal')
            plt.show()
        else:
            print(f"Colunas '{label_col}' ou '{value_col}' não encontradas em {df_name}.")
    else:
        print(f"DataFrame '{df_name}' não encontrado.")


parser = yacc.yacc()


