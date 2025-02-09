# Download Frames API

Este é um projeto de aplicação desenvolvido em Python 3.12. 

## Objetivo

Esta aplicação tem como objetivo realizar o download dos frames processados pelo serviço de extração de frames.

Para que o usuario possa realizar o download dos frames, é necessário que o mesmo tenha o file name salvo dentro do S3, mas caso não tenha em mãos, é possivel realizar uma consulta em nosso banco de dados para buscar essas informações.

Swagger da aplicação:
![Logo da Aplicação](img/swagger.png)

Exemplo de Busca de dados de um determinado cliente:
![Logo da Aplicação](img/rota de busca.png)

Exemplo de Download de Frames:
![Logo da Aplicação](img/download de frames.png)

##  Executando a Aplicação
#### Requisitos

- Python 3.12
- pip

#### Instalação
Para instalar as dependências necessárias, execute o seguinte comando apontando para o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
````    
OBS: Caso alguma alteração no projeto seja feita, é de estrema importancia atualizar as dependencias do projeto, e para isso pode usar o seguinte comando
````
pip freeze > requirements.txt
````

####  Execução
Para executar a aplicação, utilize o comando:
```bash
python src/app.py
````
##  Testes Unitários
Está aplicação também conta com testes unitarios, que estão localizados na pasta tests. Vale ressaltar que os testes unitarios estão utilizando o pytest e pytest-cov para analisar a cobertura de codigo, e por conta disso, para rodar os testes unitarios é necessario instalar as dependencias abaixo:
````    
pip install pytest
pip install pytest-cov
````

Para Analisar o codigo local e verificar a porcentagem de cobertura em cada arquivo, pode rodar o comando abaixo:
````
coverage3 run -m pytest -v --cov=. 
````

Caso queria verificar os testes dentro do sonnar, basta rodar os comandos do covarage e da geracao do arquivo covarerage.xml e depois rodar o sonnar-scanner
````
coverage3 run -m pytest -v --cov=. --cov-report xml:coverage.xml
sonar-scanner
````

##  Integração e Deploy
Para realizar o deploy desta aplicação, foi utilizado  a integração do GitHub Actions, permitindo fazer o deploy diretamente na AWS, utilizando os arquivos Kubernetes presentes na pasta K8S. Para subir a imagem em ambiente produtivo, estamos utilizando o AWS ECR.
Git Actions:
![Logo da Aplicação](images/git_action.png)

AWS ECR:
![Logo da Aplicação](images/ecr.png)

