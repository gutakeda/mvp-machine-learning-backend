from sklearn.metrics import accuracy_score
from models.pipeline import Pipeline

class Avaliador:

    def avaliar(model, X_test, Y_test):
        """ Faz uma predição e avalia o modelo. """
        predicoes = Pipeline.preditor(model, X_test)

        return accuracy_score(Y_test, predicoes)