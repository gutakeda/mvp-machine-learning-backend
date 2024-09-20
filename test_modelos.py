from models.avaliador import Avaliador
from models.carregador import Carregador
from models.pipeline import Pipeline


# Para rodar: pytest -v test_modelos.py -s
# Para rodar na versão do python do venv: python -m pytest -v test_modelos.py -s

# Instanciação das Classes
carregador = Carregador()
avaliador = Avaliador()
pipeline = Pipeline()

# Parâmetros
# troque url_dados para test_dataset_heart_disease.csv caso queira rodar os testes
# com o mesmo conjunto de dados usado para treinar o modelo
# url_dados = "./machine-learning/data/test_dataset_heart_disease.csv"
url_dados = "./machine-learning/data/val_dataset_heart_disease.csv"
colunas = ['age', 'sex', 'chest', 'rest', 'cholesterol', 'fasting', 'resting', 'max', 'exercise', 'oldpeak', 'stslope']

# Carga dos dados
dataset = Carregador.carregar_dados(url_dados)
array = dataset.values
X = array[:,0:-1]
y = array[:,-1]

# Método para testar o modelo de KNN normalizado a partir do arquivo correspondente
def test_pipeline_knn_norm():
    # Importando o pipeline de KNN normalizado
    path = './machine-learning/pipelines/knn_norm.pkl'
    pipeline = Pipeline.carrega_pipeline(path)

    # Obtendo as métricas do KNN
    acuracia = Avaliador.avaliar(pipeline, X, y)
    print(acuracia, "knn-norm")

    assert acuracia >= 0.78

# Método para testar modelo KNN padronizado a partir do arquivo correspondente
def test_pipeline_knn_padr():
    # Importando pipeline de KNN padronizado
    path = './machine-learning/pipelines/knn_padr.pkl'
    pipeline = Pipeline.carrega_pipeline(path)

    # Obtendo as métricas do KNN
    acuracia = Avaliador.avaliar(pipeline, X, y)
    print(acuracia, "knn-padr")

    assert acuracia >= 0.78

# Método para testar pipeline NB padronizado a partir do arquivo correspondente
def test_pipeline_nb_padr():
    # Importando pipeline de SVM padronizado
    path = './machine-learning/pipelines/svm_padr.pkl'

    pipeline = Pipeline.carrega_pipeline(path)

    # Obtendo as métricas do SVM
    acuracia = Avaliador.avaliar(pipeline, X, y)
    print(acuracia, "svm-padr")

    assert acuracia >= 0.78