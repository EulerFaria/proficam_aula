import pyodbc
import pandas as pd

def get_data():

    # Carrega chave de conexão
    with open('../cnx_str.txt','r') as f:
        cnx_str = f.read()

    # Estabelce conexão com banco
    cnx_odbc = pyodbc.connect(cnx_str)
    
    # Carrega Query
    with open('../query_odbc.txt','r') as f:
        query = f.read()
    
    # Extrai dados
    df = pd.read_sql(query, cnx_odbc)

    # Checa qualidade dos dados
    if df.isnull().sum().sum()>0:
        print("Dados nulos encontrados")

    return df
    
