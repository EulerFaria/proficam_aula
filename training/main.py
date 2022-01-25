
from data_preparation import read_data,remove_outliers,get_dummies,split_data
from train_model import train
from logger import get_logger
from generate_report import generate_report

# Logger
logger = get_logger(__name__)

if __name__ == "__main__":
    
    # Lendo dados
    df = read_data()

    # Removendo Outliers
    df = remove_outliers(df)

    # Get Dummies
    df = get_dummies(df)

    # Divindo dados
    X_train, X_test, y_train, y_test = split_data(df)

    # Treinando Modelo
    regLinear,score = train(X_train,y_train)

    # Avaliando Modelo 
    generate_report(regLinear,X_test,y_test,score)
