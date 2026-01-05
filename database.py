import pyodbc
import os
import requests
import time
from bs4 import BeautifulSoup
import psycopg2
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()
# Variaveis padrao do sistema
cnpj = []
DIR = os.getcwd()
File = f"{DIR}\\database.accdb;"
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

print('iniciando sistema')
print('por favor aguarde')
try:
    GREEN = "\033[0;32m"
    # Solicita e tenta conectar com o servidor postgreSQL
    conn_post = psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB")
    )
    conx_post = conn_post.cursor()
    print('Conexão bem sucedida ao banco loja')
except psycopg2.OperationalError as e:
    messagebox.showerror('Tempo de conexão excedido', f'{e}')
except Exception as e:
    messagebox.showerror(f'ERROR', {e})
time.sleep(5)

# Solicita e tenta fazer uma conexão com o banco Microsoft Access
try:
    conn = pyodbc.connect("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + File + "unicode_results=True;")
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')
    conx = conn.cursor()
    print('Conexão bem sucedida ao banco Access')
except pyodbc.IntegrityError as e:
    messagebox.showerror('ERROR', 'Dados ja existentes \n' + str(e))
except pyodbc.DataError as e:
    messagebox.showerror('ERRO', str(e))
    print("Database Error:", str(e))
finally:
    print('Redirecionando para o menu principal...')
    time.sleep(3)

def atualiza_banco():
    global conx_post
    print(RESET + 'Buscando por fornecedores')
    time.sleep(2)
    try:
        # pegando dados do banco loja
        sql = "SELECT  id, cnpj, razaosocial, id_tipoempresa FROM fornecedor ORDER BY id"
        conx_post.execute(sql)
        result_post = conx_post.fetchall()
        print(RESET + 'Fornecedores localizados')
        print(RESET + 'Adicionando ao banco Access')
        time.sleep(2)
        os.system('cls')
        for row in result_post:
            try:
                # Convertendo o valor Decimal para um número inteiro
                id = int(row[0])
                cnpj_post = int(row[1])
                razaosocial_post = row[2]
                id_tipoempresa_post = int(row[3])
                # adicionando dados ao bando Access
                query = f"INSERT INTO fornecedor (id, cnpj, razaosocial, id_tipoempresa) VALUES ({id}, {cnpj_post}, '{razaosocial_post}', '{id_tipoempresa_post}')"
                print(RESET + f'Verificando Fornecedor :{razaosocial_post}')
                conx.execute(query)
                print(GREEN + '======================================================================================================================')
                print(GREEN + f'O Fornecedor :{id}, CNPJ:{cnpj_post}, {razaosocial_post}, {id_tipoempresa_post} foi adicionado !')
                print(GREEN + '======================================================================================================================')
                time.sleep(0.1)
                os.system('cls')
            except pyodbc.DatabaseError as e:
                # print(RED + f'{e}')
                print(RED + '======================================================================================================================')
                print(RED + f'O Fornecedor :{id}, CNPJ:{cnpj_post}, {razaosocial_post}, {id_tipoempresa_post} ja existe!' + GREEN + ' Fazendo atualização.')
                print(RED + '======================================================================================================================')
                update = f"UPDATE fornecedor SET cnpj = {cnpj_post}, razaosocial='{razaosocial_post}', id_tipoempresa = {id_tipoempresa_post} WHERE id = {id}"
                conx.execute(update)
                time.sleep(0.1)
                os.system('cls')
            except Exception as e:
                print("Um erro foi encontrado", str(e))
            finally:
                conx.commit()
    except Exception as e:
        print("Erro na conexão com o PostgreSQL",e)
    print(RESET + 'Fornecedores adicionados ao banco !!!')

def buscaweb(query):
    global conx, conn
    print(RESET + 'Iniciando a raspagem')
    print(RESET + '======================================================================================================================')
    try:
        conx.execute(query)
        result = conx.fetchall()
        time.sleep(0.5)
        os.system('cls')
        try:
            for i in result:
                print(RESET + f'Pesquisando o fornecedor {i[0]} CNPJ : {i[1]} \n')
                url = f"https://consultapublica.sefaz.ce.gov.br/sintegra/consultar?tipdocumento=2&numcnpjcgf={i[1]}"
                r = requests.get(url)
                r.raise_for_status()  # Check for HTTP request errors
                pesquisa = BeautifulSoup(r.text, 'html.parser')
                # Modify the next line to match your XPath expression
                result = pesquisa.select('#enderecosintegara > thead > tr:nth-child(2) > td > span:nth-child(1)')
                simples_html = pesquisa.select('#enderecosintegara > thead > tr:nth-child(12) > td')
                if result:
                    CNAE = result[0].text  # Extract the text from the first matching element
                    simples = simples_html[0].text
                    print(RESET + '======================================================================================================================')
                    print(RESET + f'FOI ENCONTRADO FORNECEDOR {i[0]} CNPJ: {i[1]} CNAE:' + GREEN + f' {CNAE}')
                    print(RESET + '======================================================================================================================')
                    try:
                        # update = f'UPDATE fornecedor SET CNAE = {CNAE} WHERE cnpj = {i}'
                        update = f"UPDATE fornecedor SET CNAE = '{CNAE}', Simples_Nacional = '{simples}' WHERE cnpj = '{i[1]}'"
                        conx.execute(update)
                        conn.commit()
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                    os.system('cls')
                else:
                    print(RED + '======================================================================================================================')
                    print(RED + f'NAO FOI ENCONTRADO CNPJ: {i[1]} DO FORNECEDOR {i[0]}')
                    print(RED + '======================================================================================================================')
                    time.sleep(1)
                    
                    try:
                        # update = f'UPDATE fornecedor SET CNAE = {CNAE} WHERE cnpj = {i}'
                        update = f"UPDATE fornecedor SET CNAE = 'Fornecedor não encontrado' , Simples_Nacional = 'Fornecedor não encontrado' WHERE cnpj = '{i[1]}'"
                        conx.execute(update)
                        conn.commit()
                    except Exception as e:
                        print(e)
                    os.system('cls')
        except requests.exceptions.RequestException as e:
            messagebox.showerror("HTTP Request Error:", str(e))
        except Exception as e:
            messagebox.showerror("Other Error:", str(e))
            print(("Other Error:", str(e)))
    except pyodbc.Error as e:
    # Trate o erro do pyodbc de acordo com o tipo específico de erro
        if "Illegal encoding" in str(e):
            # Exibir uma mensagem de erro personalizada
            messagebox.showerror('Illegal encoding', str(e))
            print("Erro de codificação ao acessar o banco Access\n" + str(e))
        else:
            messagebox.showerror('Erro conexão', str(e))
            print("Erro ao acessar o banco Access:", str(e))

def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():

    while True:
        limpar_tela()
        print(RESET + "1. Atualizar banco de dados")
        print(RESET + "2. Buscar dados na web (Todos os fornecedores)")
        print(RESET + "3. Buscar dados na web (Apenas não encontrados)")
        print(RESET + "4. Buscar dados na web (Apenas novos fornecedores)")
        print(RESET + "5. Sair")
        print('\n')
        print("Escolha uma opção: ")
        escolha = input()

        if escolha == '1':
            limpar_tela()
            atualiza_banco()
            print(RESET + "Pressione Enter para continuar...")
            input()
        elif escolha == '2':
            limpar_tela()
            buscaweb('SELECT razaosocial, cnpj FROM fornecedor')
            print(RESET + "Pressione Enter para continuar...")
            input()
        elif escolha == '3':
            limpar_tela()
            buscaweb('''SELECT razaosocial, cnpj FROM fornecedor WHERE cnae = 'Fornecedor não encontrado';''')
            print(RESET + "Pressione Enter para continuar...")
            input()
        elif escolha == '4':
            limpar_tela()
            buscaweb('''SELECT razaosocial, cnpj FROM fornecedor WHERE cnae is null;''')
            print(RESET + "Pressione Enter para continuar...")
            input()
        elif escolha == '5':
            break
        else:
            print("Opção " + RED + "inválida." + RESET + " Tente novamente.")
            time.sleep(1)
            limpar_tela()

if __name__ == "__main__":
    main()
