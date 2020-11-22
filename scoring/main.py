from data_acquisition import get_data,get_cnx_str,get_odbc_connection,get_query,get_data,check_data


if __name__ == "__main__":
    # Carrega chave de conexão
    cnx_str = get_cnx_str()

    # Estabelce conexão com banco
    cnx_odbc = get_odbc_connection(cnx_str)

    # Carrega Query
    query =get_query(tini='2020-10-01',tfim='2020-11-22')

    # Extrai dados
    df= get_data(query,cnx_odbc)

    # Checa qualidade dos dados
    df = check_data(df)
    print(df.head())

    