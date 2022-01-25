import pickle 

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from logger import get_logger 

# Logger
logger = get_logger(__name__)

def train(X_train,y_train,cv=5,filename='regLinear.sav'):
    """Essa fuunção executa o treino do modelo e obtem o score do mesmo utilizando validação cruzada com 'cv' pastas

    Parameters
    ----------
    X_train : numpy.array
        Características utilizadas no treinamento do modelo
    y_train : numpy.array
        Target do modelo
    cv : int, optional
        Número de pastas do Cross Validation, by default 5
    filename : str, optional
        Caminho onde será salvo o modelo, by default 'regLinear.sav'

    Returns
    -------
    sklearn.linear_model.LinearRegression,numpy.array
        Modelo treinado
        Array com os valore do erro médio absoluto percentual obtidos durante o processo de validação cruzada
    """
    
    try:
        regLinear = LinearRegression()

        logger.info(f"Avaliando o modelo - Cross-Validation com {cv} pastas")
        
        # Realizando o cross validation com a métrica definida do erro médio absoluto percentual
        score = cross_val_score(estimator=regLinear, X=X_train, y=y_train, cv=cv, scoring='neg_mean_absolute_percentage_error')

        logger.info(f"Média: {-score.mean()}")
        logger.info(f"Desvio: {score.std()}")

        regLinear.fit(X_train, y_train)

        logger.info(f"Salvando modelo como {filename}")
        pickle.dump(regLinear, open(filename, 'wb'))

    except Exception as e:
        logger.critical(f'Não foi possível treinar o modelo',exc_info=True)

    return regLinear,score

