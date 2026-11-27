const URL_PREDICAO = 'http://127.0.0.1:5000/predicao';

const CAMPOS = [
  'acidez_fixa', 'acidez_volatil', 'acido_citrico', 'acucar_residual',
  'cloretos', 'dioxido_enxofre_livre', 'dioxido_enxofre_total',
  'densidade', 'ph', 'sulfatos', 'alcool', 'tipo_branco',
];

const NOMES_CLASSES = { baixa: 'Baixa', media: 'Média', alta: 'Alta' };

// Vinhos fictícios da seção 14 do notebook, na mesma ordem de CAMPOS.
const EXEMPLOS = [
  [7.8, 0.70, 0.05, 2.0, 0.090, 12.0, 45.0, 0.9975, 3.40, 0.55, 9.3, 0],
  [7.2, 0.30, 0.35, 2.2, 0.065, 15.0, 40.0, 0.9960, 3.30, 0.70, 11.0, 0],
  [6.8, 0.25, 0.32, 6.0, 0.045, 35.0, 135.0, 0.9940, 3.20, 0.48, 10.5, 1],
  [6.5, 0.25, 0.35, 2.0, 0.030, 35.0, 110.0, 0.9905, 3.25, 0.50, 12.8, 1],
];

const formulario = document.getElementById('formulario');
const seletorExemplo = document.getElementById('exemplo');
const botaoPrever = document.getElementById('prever');
const areaResultado = document.getElementById('resultado');
const areaErro = document.getElementById('erro');

/**
 * Preenche o formulário com o vinho de exemplo escolhido.
 */
const preencherExemplo = () => {
  const exemplo = EXEMPLOS[seletorExemplo.value];
  if (!exemplo) {
    return;
  }
  CAMPOS.forEach((campo, posicao) => {
    document.getElementById(campo).value = exemplo[posicao];
  });
  esconderMensagens();
};

/**
 * Lê os campos do formulário. Retorna null se algum campo estiver vazio.
 */
const lerFormulario = () => {
  const vinho = {};
  for (const campo of CAMPOS) {
    const valor = document.getElementById(campo).value.trim();
    if (valor === '') {
      return null;
    }
    vinho[campo] = Number(valor);
  }
  return vinho;
};

const MENSAGEM_FALHA_PREDICAO = 'Não foi possível realizar a predição.';

/**
 * Envia as medidas do vinho para a API e devolve a resposta em JSON.
 */
const enviarPredicao = async (vinho) => {
  const resposta = await fetch(URL_PREDICAO, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(vinho),
  });
  const dados = await resposta.json().catch(() => null);
  if (!resposta.ok || dados === null) {
    throw new Error(dados?.message || MENSAGEM_FALHA_PREDICAO);
  }
  return dados;
};

/**
 * Cria a barra horizontal com a probabilidade de uma classe.
 */
const criarBarra = (classe, probabilidade) => {
  const percentual = `${Math.round(probabilidade * 100)}%`;

  const barra = document.createElement('div');
  barra.className = 'barra';

  const nome = document.createElement('span');
  nome.textContent = NOMES_CLASSES[classe];

  const trilho = document.createElement('div');
  trilho.className = 'barra-trilho';
  const preenchimento = document.createElement('div');
  preenchimento.className = `barra-preenchimento classe-${classe}`;
  preenchimento.style.width = percentual;
  trilho.appendChild(preenchimento);

  const valor = document.createElement('span');
  valor.className = 'barra-valor';
  valor.textContent = percentual;

  barra.append(nome, trilho, valor);
  return barra;
};

/**
 * Exibe a classe prevista e as probabilidades de baixa, média e alta.
 */
const mostrarResultado = ({ classe, probabilidades }) => {
  const destaque = document.getElementById('classe');
  destaque.textContent = NOMES_CLASSES[classe];
  destaque.className = `classe-${classe}`;

  const listaBarras = document.getElementById('probabilidades');
  listaBarras.replaceChildren(
    ...Object.keys(NOMES_CLASSES).map((nome) => criarBarra(nome, probabilidades[nome])),
  );

  areaErro.hidden = true;
  areaResultado.hidden = false;
};

const mostrarErro = (mensagem) => {
  areaErro.textContent = mensagem;
  areaResultado.hidden = true;
  areaErro.hidden = false;
};

const esconderMensagens = () => {
  areaResultado.hidden = true;
  areaErro.hidden = true;
};

/**
 * Valida o preenchimento, chama a API e mostra o resultado ou o erro.
 */
const preverQualidade = async (evento) => {
  evento.preventDefault();

  const vinho = lerFormulario();
  if (vinho === null) {
    mostrarErro('Preencha todas as medidas com números antes de prever.');
    return;
  }

  botaoPrever.disabled = true;
  try {
    mostrarResultado(await enviarPredicao(vinho));
  } catch (erro) {
    const semConexao = erro instanceof TypeError;
    mostrarErro(semConexao
      ? 'Não foi possível conectar à API. Verifique se ela está rodando em 127.0.0.1:5000.'
      : erro.message);
  } finally {
    botaoPrever.disabled = false;
  }
};

seletorExemplo.addEventListener('change', preencherExemplo);
formulario.addEventListener('submit', preverQualidade);
formulario.addEventListener('reset', () => {
  seletorExemplo.value = '';
  esconderMensagens();
});
