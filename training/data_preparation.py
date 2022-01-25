import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from logger import get_logger
from sklearn.model_selection import train_test_split

# Logger
logger = get_logger(__name__)

def read_data(path= '../data/precos-imoveis-vitoria-2020.csv'):
    """Essa função lê os dados contidos no arquivo do caminho path

    Parameters
    ----------
    path : str, optional
        Diretório do arquivo de dados, by default '../data/precos-imoveis-vitoria-2020.csv'

    Returns
    -------
    pandas.DataFrame object
        Pandas DataFrame
    """
    try:

        logger.info("Lendo dados")
        # Carregando o CSV em um DataFrame
        df = pd.read_csv(path, encoding='windows-1252')
        logger.info('\n \t'+ df.head(5).to_string().replace('\n', '\n\t'))
    
    except Exception as e:
        logger.critical(f'Não foi ler o arquivo de dados',exc_info=True)
    
    return df 

def remove_outliers(df,k=1.5):
    """Essa função é responsável pela remoção dos outliers. Para detectar os outliers para uma determinada coluna, 
    o primeiro e o terceiro quartil (Q1 , Q3) são calculados. Uma observação é sinalizada como discrepante se estiver
    fora do intervalo **R = [Q1 - k(IQR), Q3 + k(IQR)]** com IQR = Q3 - Q1 e k >= 0. 

    Parameters
    ----------
    df : pandas.DataFrame object
        Pandas dataframe contendo os dados que serão utilizados para treino e validação do modelo
    k : float, optional
        Multiplicador do IQR para detecção de valores discrepantes, by default 1.5

    Returns
    -------
    pandas.DataFrame object
        DataFrame com outliers removidos
    """
    try:
        logger.info('Removendo outliers')
        # Calculando o Q1
        Q1 = df.quantile(0.25)

        #Calculando o Q3
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        logger.debug(f'IQR = {IQR}')

        # Contador de outliers
        outliers = 0

        # Loop para excluir os outliers da tabela
        for x in IQR.index:
            for y in df.index:
                # Comparação lógica para verificar se o valor está dentro do intervalo R
                if (df.loc[y, x] < Q1[x] - IQR[x]*k) or (df.loc[y, x] > Q3[x] + IQR[x]*k):
                    df.drop(index=y, inplace=True)
                    outliers += 1

        logger.info(f'Foram encontrados e removidos {outliers} outliers')

    except Exception as e:
        logger.critical(f'Erro na remoção de valores descrepantes',exc_info=True)
    
    return df

def get_dummies(df,cols=['bairro','tipo de construção']):
    """Essa função aplica a transformação OneHotEncoding ou get_dummies para transformar 
    os dados de categóricos de texto um vetor de fictício que indica o tipo do dado.

    Parameters
    ----------
    df : pandas.DataFrame object
        Pandas dataframe contendo os dados que serão utilizados para treino e validação do modelo
    cols : list, optional
       Lista com colunas a serem transformadas, by default ['bairro','tipo de construção']

    Returns
    -------
    pandas.DataFrame object
        Pandas dataframe com dados categóricos tratados
    """
    try:
        logger.info("Tratando variáveis categóricas")
    
        for col in cols:
            df = pd.get_dummies(df, columns=[col], prefix=col)

        target = df.pop('valor')
        df = pd.concat([df, target], axis=1)    

        logger.info(f"Dimensões Dataframe:{df.shape}")
        logger.debug('\n \t'+ df.head(5).to_string().replace('\n', '\n\t'))   
    except Exception as e:
        logger.critical(f'Erro na transformação de dados categóricos',exc_info=True)

    return df 

def split_data(df,test_size=0.2):
    """Essa função reparte o cojnunto de dados em Treino e Teste de acordo com a proporção fornecida em *test_size*

    Parameters
    ----------
    df : pandas.DataFrame object
        Pandas dataframe contendo os dados que serão utilizados para treino e validação do modelo
    test_size : float, optional
        Proporção da repartição, by default 0.2

    Returns
    -------
    (numpy.array,numpy.array,numpy.array,numpy.array)
        X_train: Features do conjunto de Treino,
        X_test: Features do conjunto de Teste,
        y_train: Target do conjunto de Treino,
        y_test: Target do conjunto de Teste
    """
    try:
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=6)

        logger.info(f'Tamanho de X_train: {X_train.shape}')
        logger.info(f'Tamanho de X_test: {X_test.shape}')

        logger.info(f'Tamanho de y_train: {y_train.shape}')
        logger.info(f'Tamanho de y_test: {y_test.shape}')
    except Exception as e:
        logger.critical(f'Erro na separação dos conjuntos de treino e teste',exc_info=True)
        
    return X_train, X_test, y_train, y_test






