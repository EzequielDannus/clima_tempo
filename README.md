<h1> Passo a Passo: </h1>


 - Clone o repositório na sua máquina local.

 - Verifique se você possui a versão atual do Python.

 - Abra o terminal de sua preferência

 - Entre na pasta que você clonou o repositório, pelo terminal, utilizando o comando 'cd'

 - Instale as bibliotecas necessárias à utilização do programa.

 - Primeira Biblioteca: Pipenv. Ao terminar a instalação, copie
   o comando `pipenv shell` para criação do ambiente virtual
 
 - Após criado o ambiente, utilize os seguintes comandos para instalar as dependências restantes:
   `pipenv install pyramid`
   `pipenv install cookiecutter`
   
 - Copie o seguinte comando: `python setup.py develop`

 - E após o carregamento do anterior, copie este `pserve development.ini --reload`

 - Ao concluir as etapas anteriores, serão criados dois links localhost:
  <img src ="./clima_tempo/static/localhosts.png "alt= "imagem"></img>