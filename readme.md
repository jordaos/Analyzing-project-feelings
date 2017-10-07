# Analyzing project feelings

## Pegar informações do repositório
Baixe o repositório https://gitlab.com/rodrigorgs/msr17-challenge/tree/master

Execute o passo `Get information from repository`*, em https://gitlab.com/rodrigorgs/msr17-challenge/tree/master#get-information-from-repository.

Nomeie os bancos de dados gerados com o nome da branch que será analisada. Ex.: se a branch se chamar `branch-0.1`, o arquivo SQLite deve se chamar `branch-0.1.sqlite`

Mova o(s) arquivos SQLite com os dados do projeto para `data/PROJECTNAME_messages/BRANCHNAME`. Substitua `PROJECTNAME` e `BRANCHNAME`.

*Use `git clone -b my-branch --single-branch https://git@github.com/username/myproject.git` para clonar apenas uma branch.

## Análise

### Usando Naive Bayes

#### Extrair as mensagens do SQLITE para um arquivo TXT
Execute `src/extract-commit-to-file.py BRANCH_NAME`

#### Realizar classificação
Execute `src/classify-with-naive-bayes-and-nltk.py BRANCH_NAME`. Não se esqueça de antes alterar a variável `model_dir`, na linha 50 (aproximadamente) para o modelo da sua análise (no meu caso, será a primeira release).

### Usando SentiStrength's

#### Classificação
Primeiro, baixe os dados de sentistrength: http://sentistrength.wlv.ac.uk/

Depois baixe a ferramenta Java do sentistrength: http://gateway.path.berkeley.edu:8080/artifactory/list/release-local/com/sentistrength/sentistrength/0.1/sentistrength-0.1.jar

Extraia os dados de sentistrength para `data/sentistrength/sentistrength_data/`. E mova a ferramenta Java sentistrength para `data/sentistrength/`.

Renomear `data/sentistrength/sentistrength_data/EmotionLookupTable.txt` para `data/sentistrength/sentistrength_data/EmotionLookupTable-old.txt`.

Execute `src/filter-wordlist.py`.

No nosso estudo, detectamos a palavra `Fix` ligada a um sentimento positivo, já que é uma palavra usada quando se corrige um bug. E a palavra `Contributed` também como um sentimento positivo, dado que a presença de um contribuidor melhora o esforço e empenho do desenvolvedor no tal problema.
Logo, precisamos "ensinar" isso ao SentiStrength. Adicionaremos em `data/sentistrength/sentistrength_data/EmotionLookupTable.txt` a linha (seguindo a órdem alfabetica) `fix	3	` e `contributed	2	`.

Para que o sentistrength possa analisar as mensagens, é necessário que todas as mensagens estejam em um único arquivo, um por linha. Iremos fazer esse passo, e junto dele já iremos aproveitar para filtrar a mensagem (removendo dados desnecessários para esse contexto). Para fazer isso, vamos executar `src/from-sqlite-to-file-ss.py BRANCH_NAME`

Para computar o sentimento de cada commit, vá até `data/sentistrength` e execute:

```
java -jar sentistrength-0.1.jar sentidata sentistrength_data/ input FILE_LOCATION explain
```
e substitua `FILE_LOCATION` pela localização do arquivo gerado no passo anterior. Isso irá gerar um arquivo em `FILE_LOCATION` chamado `FILENAME0_out.txt`, que é onde SentiStrength guarda a pontuação de cada mensagem.

Agora precisamos converter esse arquivo em um banco de dados SQLite, para ser melhor analisado. Para isso, execute `src/convert-in-sqlite.py BRANCHNAME`.

O ultimo passo é classificar as mensagens em "positivo", negativo ou "neutro". Para fazer isso, execute `sort-commits-sentistrength.py BRANCH_NAME`

## Verificando similaridade com a classificação manual
Execute `src/verify-similarity.py MANUAL_CLASSIFICATION MODEL_CLASSIFICATION FILE_NAME`