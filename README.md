# Pdf Splitter

Automação criada para permitir automações locais em arquivos do tipo PDF

## Executando

Dentro do diretório raiz do projeto, execute os comandos abaixo para configuração de dependências

```shell
$ poetry init
$ poetry shell
$ python main.py --help
$ python main.py [NOME DO MÉTODO ESCOLHIDO] --help
```

em seguida, basta executar o último comando passando os parâmetros necessários

### To-do

- [ ] Permitir que chunks sejam gerados tanto por qt de páginas quanto por intervalos
- [ ] Criar interface para coletar pdf
- [ ] Permitir passar um link para baixar arquivo
- [ ] Criar automação para envio de arquivos para onedrive/google drive
- [ ] Criar comando via terminal
- [x] Verificar questão de caminhos no python
- [x] Automatizar coleta de páginas para formação de chunks
