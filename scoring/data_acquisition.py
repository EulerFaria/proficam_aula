import pyodbc
import time
import pandas as pd
import os
from logger import get_logger

# Logger
logger = get_logger(__name__)

def get_cnx_str(cnx_name='CNX_STR_PROFICAM'):
    """Essa função é responsável por obter a chave de conexão cnx_name armazenada como variável de ambiente

    Parameters
    ----------
    cnx_name : str
        Nome da variável de ambiente 

    Returns
    -------
    str
        Chave de conexão ODBC contendo DRIVER, SERVER, UID, PWD.
        ex: 'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=xxx; DATABASE=xxx; UID=xxx; PWD=xxx'
    """
    try:
        cnx_str = os.environ.get('CNX_STR_PROFICAM')
        logger.info(f"Chave de conexão {cnx_name} capturada com sucesso")
        logger.debug(f"***{cnx_str}")
        return cnx_str
    except Exception as e:
        logger.critical(f'Não foi possível obter a chave de conexão {cnx_name}',exc_info=True)
    
def get_odbc_connection(cnx_str,attempts=6,time_sleep=30):
    """Esta função é responsável por estabelecer conexão ODBC a partir da chave de conexão fornecida. 

    Parameters
    ----------
    cnx_str : string
        Chave de conexão ODBC contendo DRIVER, SERVER, UID, PWD.
        ex: 'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=xxx; DATABASE=xxx; UID=xxx; PWD=xxx'
    attempts : int, optional
        Número de tentativas para estabelecer conexões, by default 6

    Returns
    -------
    pyodb.connect Object
        Objeto de conexão pyodbc

    Raises
    ------
    Exception
        [description]
    """

    for i in range(1,attempts):
        try:
            cnx_odbc = pyodbc.connect(cnx_str)
            logger.info(f'Conexão estabelecida com sucesso')
            return cnx_odbc

        except Exception as e:
            logger.warning(f'Falha na tentativa {i} de conexão ODBC')
            time.sleep(time_sleep)
            if i == 5:
                logger.critical('Não foi possível obter a conexão ODBC',exc_info=True)
                raise Exception(f'Não foi possível obter a conexão ODBC {type(e)} , {e.args}')
    
def get_query(tini, tfim):
    """Essa função é responsável por construir a query com clausula where filtrando datas entre tini e tfim

    Parameters
    ----------
    tini : str
        Tempo início para filtro de data, dd/mm/yy
    tfim : str
        Tempo fim para filtro de data, dd/mm/yy
        
    Returns
    -------
    str
        Query com fitro de data
    """
    with open("../query_odbc.txt", "r") as f:
        query = f.read()
    query+= f"WHERE [data] >='{tini}' and [data] <='{tfim}'"   
    return query

def get_data(query,cnx):
    """Essa função executa a extração dos dados

    Parameters
    ----------
    query : str
        Query SELECT para extração dos dados
    cnx : Object
        Objeto de conexao pyodbc.connect

    Returns
    -------
    Object
        Pandas DataFrame object
    """
    try:
        df = pd.read_sql(query, cnx)
        return df
    except Exception as e:
        logger.critical(f"Erro na extração dos dados",exc_info=True)

def check_data(df):
    """Essa função checa a qualidade dos dados

    Parameters
    ----------
    df : Object
        Pandas DataFrame object

    Returns
    -------
    None or Object
        Retorna None in caso de linhas nulas encontrados ou o próprio DataFrame caso esteja ok.
    """
    # Checa qualidade dos dados
    if df.isnull().sum().sum()>0:
        print("Dados nulos encontrados")
        return None
    else: return df