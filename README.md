# MVP Vinhos — Classificação da Qualidade de Vinhos

Este projeto tem como objetivo prever a qualidade de um vinho a partir das suas medidas químicas, classificando-a como **baixa**, **média** ou **alta**.
O modelo de *machine learning* foi construído em um notebook no Google Colab e é servido de forma embarcada por uma API Flask, consumida por um front-end em HTML, CSS e JavaScript puro.

O MVP reúne o conteúdo da sprint Qualidade de Software, Segurança e Sistemas Inteligentes.

---

## Vídeo de apresentação

O vídeo, de até 3 minutos, mostra a aplicação rodando e chamando o modelo. Ele está no arquivo `video/apresentacao.mp4` e também pode ser assistido pelo [Google Drive](COLOCAR_O_LINK_AQUI).

---

## Dataset

*Wine Quality*, do [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/186/wine+quality), com 6.497 amostras de vinhos tintos e brancos da denominação de origem Vinho Verde, no norte de Portugal.

Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). *Modeling wine preferences by data mining from physicochemical properties*. Decision Support Systems, 47(4), 547-553. Licença CC BY 4.0.

A nota original, de 0 a 10, foi agrupada em três classes:

| Classe | Nota original |
|---|---|
| baixa | 5 ou menos |
| média | 6 |
| alta | 7 ou mais |

---

## Estrutura do repositório

```
MVP_VINHOS/
├── api/
│   ├── app.py                  rotas da API
│   ├── config.py               caminhos, hash do modelo e atributos
│   ├── logger.py               configuração dos logs
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── model/                  carga do modelo, predição e avaliação
│   ├── schemas/                contratos de entrada e saída (Pydantic)
│   ├── tests/                  testes automatizados com PyTest
│   └── MachineLearning/
│       ├── data/               CSVs originais e conjunto de teste
│       ├── notebooks/          notebook do Colab
│       └── pipelines/          modelo exportado (.pkl)
├── front/
│   ├── index.html
│   ├── styles.css
│   └── scripts.js
├── video/
│   ├── apresentacao.mp4        vídeo de apresentação
│   └── link_drive.txt          link do vídeo no Google Drive
└── README.md
```

---

## Notebook de *machine learning*

O notebook `api/MachineLearning/notebooks/MVP_Vinhos.ipynb` documenta todo o processo: carga dos dados por URL, limpeza, separação em treino e teste, padronização e normalização, comparação de KNN, Árvore de Classificação, Naive Bayes e SVM com validação cruzada e *pipelines*, otimização de hiperparâmetros, avaliação final e exportação do modelo.

[Abrir o notebook no Google Colab](https://colab.research.google.com/github/Mariana-Lealdini/MVP_VINHOS/blob/main/api/MachineLearning/notebooks/MVP_Vinhos.ipynb)

O notebook roda do início ao fim sem nenhuma configuração. A busca de hiperparâmetros da seção 11 leva cerca de 9 minutos.

**Modelo escolhido:** KNN com 21 vizinhos, distância manhattan, votos com peso pela distância e dados padronizados.

| Métrica | Validação cruzada | Teste | Linha de base |
|---|---|---|---|
| Acurácia | 0,609 | 0,608 | 0,437 |
| F1 macro | 0,595 | 0,586 | 0,203 |

A linha de base corresponde a um modelo que sempre responde a classe mais comum.

---

## Como executar a API

Será necessário ter o Python 3.10, 3.11, 3.12 ou 3.13 instalado, já que o modelo foi gerado com o scikit-learn 1.6.1, que não oferece suporte ao Python 3.14.
Após clonar o repositório, é necessário ir ao diretório `api`, pelo terminal, para executar os comandos descritos abaixo.

```
$ git clone https://github.com/Mariana-Lealdini/MVP_VINHOS.git
$ cd MVP_VINHOS/api
```

> É fortemente indicado o uso de ambientes virtuais do tipo [venv](https://docs.python.org/pt-br/3/library/venv.html).

**1. Crie e ative o ambiente virtual:**

No Windows, pelo Prompt de Comando:

```
> python -m venv env
> env\Scripts\activate
```

No PowerShell, a execução de scripts pode estar bloqueada. Nesse caso, basta digitar `cmd` antes, para abrir o Prompt de Comando no mesmo terminal.

No Linux ou Mac:

```
$ python3 -m venv env
$ source env/bin/activate
```

Com o ambiente ativado, `(env)` aparece no começo da linha do terminal.

**2. Instale as dependências:**
Este comando instala as bibliotecas descritas no arquivo `requirements.txt`, com as versões fixadas.

```
(env)$ pip install -r requirements.txt
```

**3. Execute os testes automatizados:**

```
(env)$ pytest -v
```

**4. Execute a API:**

```
(env)$ python app.py
```

Ao iniciar, a API confere o hash SHA-256 do arquivo do modelo e só então o carrega. A mensagem "Modelo carregado após a conferência do hash SHA-256" indica que o modelo passou na conferência, e a linha "Running on http://127.0.0.1:5000" indica que a API está pronta.

---

## Como executar o front-end

Não há dependências ou instalação necessária. Com a API rodando, basta abrir o arquivo `front/index.html` diretamente no navegador (duplo clique ou arrastar para o browser).

> O front-end consome a API em `http://127.0.0.1:5000`. Certifique-se de que o back-end está rodando antes de usar.

### Funcionalidades

| Funcionalidade | Descrição |
|---------------|-----------|
| Preencher com um exemplo | Carrega os quatro vinhos fictícios usados na seção 14 do notebook |
| Prever qualidade | Envia as medidas à API e exibe a classe prevista |
| Probabilidades | Mostra uma barra com a probabilidade de cada classe |
| Mensagens de erro | Avisa sobre campos vazios, valores fora das faixas e API desligada |
| Limpar | Apaga os campos e o resultado |

---

## Acesso à documentação

Com a API rodando, abra o endereço abaixo no navegador para acessar a documentação interativa (Swagger):

http://127.0.0.1:5000

---

## Rota disponível

| Método | Rota | Descrição |
|---|---|---|
| POST | `/predicao` | Recebe as 12 medidas de um vinho e retorna a classe prevista e as probabilidades |

**Exemplo de requisição:**

```json
{
  "acidez_fixa": 7.8,
  "acidez_volatil": 0.70,
  "acido_citrico": 0.05,
  "acucar_residual": 2.0,
  "cloretos": 0.090,
  "dioxido_enxofre_livre": 12.0,
  "dioxido_enxofre_total": 45.0,
  "densidade": 0.9975,
  "ph": 3.40,
  "sulfatos": 0.55,
  "alcool": 9.3,
  "tipo_branco": 0
}
```

**Exemplo de resposta:**

```json
{
  "classe": "baixa",
  "probabilidades": {
    "baixa": 0.8275,
    "media": 0.1324,
    "alta": 0.0402
  }
}
```

**Faixas aceitas:** os valores fora das faixas abaixo são recusados com o código 422 e uma mensagem que indica o campo e a faixa permitida.

| Campo | Unidade | Faixa |
|---|---|---|
| `acidez_fixa` | g/dm³ de ácido tartárico | 2 a 20 |
| `acidez_volatil` | g/dm³ de ácido acético | 0 a 2 |
| `acido_citrico` | g/dm³ | 0 a 2 |
| `acucar_residual` | g/dm³ | 0 a 70 |
| `cloretos` | g/dm³ de cloreto de sódio | 0 a 1 |
| `dioxido_enxofre_livre` | mg/dm³ | 0 a 300 |
| `dioxido_enxofre_total` | mg/dm³ | 0 a 500 |
| `densidade` | g/cm³ | 0,98 a 1,05 |
| `ph` | | 2 a 5 |
| `sulfatos` | g/dm³ de sulfato de potássio | 0 a 2,5 |
| `alcool` | % do volume | 5 a 20 |
| `tipo_branco` | | 0 para tinto ou 1 para branco |

---

## Testes automatizados

Os testes ficam na pasta `api/tests` e são executados com `pytest -v`, a partir da pasta `api`.

**`test_modelo.py`:** garante que o modelo atenda aos requisitos de desempenho no conjunto de teste exportado pelo notebook, formado por 1.064 vinhos que o modelo nunca viu. Se o modelo for substituído por um com desempenho inferior, o teste falha e impede a implantação.

| Métrica | Limite mínimo | Resultado do modelo atual |
|---|---|---|
| Acurácia | 0,58 | 0,608 |
| F1 macro | 0,55 | 0,586 |

O F1 macro é a métrica principal porque dá o mesmo peso às três classes, e a classe alta é a mais rara do dataset. Os limites ficam um pouco abaixo do resultado atual e bem acima da linha de base. O mesmo arquivo também verifica que um modelo com o arquivo alterado não é carregado.

**`test_api.py`:** verifica a rota de predição, incluindo a resposta igual à do notebook para o vinho 1 da seção 14 e a recusa de valores fora das faixas, campos ausentes, campos desconhecidos e textos no lugar de números.

---

## Segurança

As práticas da disciplina Desenvolvimento de Software Seguro aplicadas na aplicação, discutidas na seção 16 do notebook:

- **Integridade do modelo:** o hash SHA-256 do `.pkl` é conferido antes da carga, já que carregar um arquivo adulterado com `pickle` poderia executar código malicioso.
- **Validação das entradas:** o back-end aceita apenas números dentro de faixas plausíveis e recusa campos desconhecidos.
- **Logs sem dados do usuário:** os registros indicam se a predição ocorreu ou quais campos foram recusados, sem os valores enviados.
- **Sem banco de dados:** as consultas não são armazenadas.
- **Versões fixadas:** o `requirements.txt` fixa a versão de cada biblioteca, o que permite verificar vulnerabilidades conhecidas.

Para trocar o modelo, é preciso gerar o novo `.pkl` pelo notebook, atualizar o valor de `HASH_MODELO` em `api/config.py` e executar os testes antes de colocá-lo em uso.

---

## Arquitetura

O modelo é servido de forma embarcada: o próprio back-end carrega o arquivo `.pkl` e realiza as predições. O código da API segue o princípio da responsabilidade única:

- **`model/`** — classes `Modelo` (carga e predição), `PreProcessador` (preparação da entrada), `Carregador` (leitura do conjunto de teste), `Avaliador` (cálculo das métricas) e funções de integridade
- **`schemas/`** — contratos de entrada e saída da API usando Pydantic, responsáveis pela validação dos dados
- **`app.py`** — rotas que recebem as requisições HTTP e retornam as respostas

---

## Tecnologias utilizadas

- [Python](https://www.python.org/)
- [scikit-learn](https://scikit-learn.org/) — modelo de *machine learning*
- [pandas](https://pandas.pydata.org/) — manipulação dos dados
- [Flask](https://flask.palletsprojects.com/)
- [Flask-OpenAPI3](https://luolingchun.github.io/flask-openapi3/) — documentação Swagger automática
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [PyTest](https://docs.pytest.org/) — testes automatizados
- HTML5, CSS3 e JavaScript puro (Fetch API) no front-end