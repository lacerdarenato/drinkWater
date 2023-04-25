# api-web-scraping
Esta API destina-se a controlar o consumo de água das pessoas cadastradas
## Montar o app

1. Para executar o projeto é necessário clonar o repositório `git clone https://github.com/lacerdarenato/drinkWater.git` dentro do diretório em deseja instalá-lo.
2. Instale as dependências contidas no arquivo requirements.txt através do comando `pip install -r requirements.txt`
3. Iniciar a aplicação executando o comando `python app.py` no diretório onde o projeto foi clonado
4. Crie um arquivo .env com as variáveis conforme o arquivo .env.example existente no projeto
5. Para conferir se a API está executando e tambem montar o banco, execute uma requisição na API que roda na rota principal. Caso esteja tudo ok aparecerá a mensagem: `API Funcionando` e a estrutura do banco estará montada