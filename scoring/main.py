from data_acquisition import get_data,get_cnx_str,get_odbc_connection,get_query,get_data,check_data
from logger import get_logger

if __name__ == "__main__":

    # Logger
    logger = get_logger(__name__)
    logger.info("Logger criado com sucesso")
    
    # Carrega chave de conexão
    logger.info("Carregando chave de conexão")
    cnx_str = get_cnx_str()

    # Estabelce conexão com banco
    logger.info("Estabelecendo conexão com banco de dados")
    cnx_odbc = get_odbc_connection(cnx_str)

    # Carrega Query
    logger.info("Parametrizando query para extração de dados")
    query =get_query(tini='2020-10-01',tfim='2020-11-22')

    # Extrai dados
    logger.info("Extraindo dados")
    df= get_data(query,cnx_odbc)

    # Checa qualidade dos dados
    logger.info("Checando qualidade de dados")
    df = check_data(df)
    logger.info("Dataset extraído:")
    logger.info('\n \t'+ df.head().to_string().replace('\n', '\n\t'))

    