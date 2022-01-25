import pandas as pd
import numpy as np

from logger import get_logger
from sklearn.metrics import mean_absolute_percentage_error
import seaborn as sns
import matplotlib.pyplot as plt

# Logger
logger = get_logger(__name__)

def generate_report(modelo,X_test,y_test,score):
    """Essa função gera um relatório de performance do modelo de regressão em formato csv e salva no diretório local.
    Além disso essa função gera um gráfico de predições versus valores reais e salva no diretório local.

    Parameters
    ----------
    modelo : object
        Modelo já treinado
    X_test : numpy.array
        Features do conjunto de teste
    y_test : numpy.array
        Target do conjunto de teste
    score : numpy.array
        Array com os valore do erro médio absoluto percentual obtidos durante o processo de validação cruzada
    """
    try:
        logger.info("Criando relatório de Performance:")
        y_pred = modelo.predict(X_test)
        # Vamos calcular o MSE (Mean Squared Error)
        mse = np.mean((y_test - y_pred) ** 2)
        rmse = np.sqrt(mse)
        mape= mean_absolute_percentage_error(y_test, y_pred)

        res= pd.DataFrame({'CV Média':[-score.mean()],
                        'CV Std':[score.std()],
                        'Testset-MSE':mse,
                        'Testset-RMSE':rmse,
                        'Testset-MAPE':mape,
                            })
    
        
        logger.info("Relatório de Performance:")
        logger.info('\n \t'+ res.to_string().replace('\n', '\n\t'))


        res.to_csv("./results.csv",index=False)

        logger.info('Gerando gráficos de Predições vs Target')
        dados = pd.DataFrame({'y_test':y_test,'Predições':y_pred})
        plt.figure(figsize=(18,10))
        sns.lineplot(data=dados, markers=True)
        plt.savefig('./pred_vs_real.png')
    
    except Exception as e:
        logger.critical(f'Não foi possível gerar o relatório de performance',exc_info=True)

