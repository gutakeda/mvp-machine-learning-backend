# HeartDisease Predictor Backend

HeartDisease Predictor Backend é a parte do servidor do aplicativo, responsável por fornecer as APIs necessárias para gerenciar transações, bem como para calcular e fornecer dados para as tabelas e dashboard.

## Funcionalidades

1. **Documentação da API**:
   - A documentação completa das APIs pode ser acessada via Swagger em: [http://localhost:5000/apidocs/#/](http://localhost:5000/apidocs/#/)

## Requisitos

- Python 3.x
- Virtualenv

## Instruções de Execução

### Mac/Linux

1. Clone este repositório:

   ```bash
   git clone https://github.com/gutakeda/mvp-machine-learning-backend
   cd mvp-machine-learning-backend
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   python run.py
   ```

### Windows

1. Clone este repositório:

   ```bash
   git clone https://github.com/gutakeda/mvp-machine-learning-backend
   cd mvp-machine-learning-backend
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   python run.py
   ```

## Swagger

1. Para ter acesso aos detalhes das APIs, basta seguir os passos anteriores para rodar a aplicação e em seguida acessar o swagger pela rota:
   ```
   http://localhost:5000/apidocs/
   ```

## Testes

1. Para rodar os testes com informação da acurácia:
   ```
   pytest -v test_modelos.py -s
   ```

   Para rodar os testes na versão do python do venv com informação da acurácia:
   ```
   python -m pytest -v test_modelos.py -s
   ```

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

---

Esperamos que você aproveite o uso do HeartDisease Predictor para testar o modelo de predição de doenças cardiacas.
