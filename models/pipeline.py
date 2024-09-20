import pickle

class Pipeline:

    def carrega_pipeline(path):
        """Carregamos o pipeline construindo durante a fase de treinamento """
        with open(path, 'rb') as file:
             pipeline = pickle.load(file)
        return pipeline

    def preditor(pipeline, X_input):
        """Realiza a predição de um paciente com base no modelo treinado"""
        diagnosis = pipeline.predict(X_input)
        return diagnosis