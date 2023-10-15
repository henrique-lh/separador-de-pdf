# Pdf Splitter

Automação criada para permitir automações locais em arquivos do tipo PDF

## Executando

Antes de iniciar, crie um arquivo .end dentro do diretório pdf_splitter, contendo as seguintes variáveis de ambiente:

```txt
PATH_TO_SECRET_JSON = <SEU_CAMINHO_PARA_O_TOKEN>
PATH_TO_CREDENTIALS_JSON = <SEU_CAMINHO_PARA_A_CREDENCIAL>
PARENT_ID = <ID DO DIRETÓRIO RAIZ>
URL = <URL DE ESCOPO>
```

Caso não tenha essas informações, olhe a seção [links úteis](#links-úteis)

Dentro do diretório raiz do projeto, execute os comandos abaixo para configuração de dependências

```shell
$ poetry init
$ poetry shell
$ cd pdf_splitter
$ python main.py --help
```

em seguida, basta executar o último comando passando os parâmetros necessários. Exemplo abaixo de como obter os parâmetros da função:

```shell
$ python main.py batch --help
$ python main.py cut --help 
```

## Links Úteis

- [Google Cloud Console](https://console.cloud.google.com/welcome?hl=pt-br&project=pdf-automation-402014)
- [Criar e preencher pastas](https://developers.google.com/drive/api/guides/folder?hl=pt-br)
- [Escolher os escopos da Google Drive API](https://developers.google.com/drive/api/guides/api-specific-auth?hl=pt-br)

### To-do

- [x] Criar automação para envio de arquivos para google drive
- [x] Criar comando via terminal
- [x] Verificar questão de caminhos no python
- [x] Automatizar coleta de páginas para formação de chunks
