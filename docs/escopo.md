# Plataforma de operações de marketplace

Base de requisitos: proposta de assessoria enviada pelo usuário. O documento é referência funcional; suas ofertas comerciais, marcas e promessas de prazo não são requisitos automaticamente aceitos.

## Primeira versão

- Painel por loja, canal e período: faturamento, pedidos, investimento em Ads, receita atribuída, ACOS, TACOS, ROAS e conversão.
- Produtos por SKU e canal, estoque, preço, custo e margem. Rentabilidade depende de taxas, frete, impostos, devoluções e custos informados.
- Plano de ação com responsável, prazo, resultado esperado e estado de execução.
- Alertas de estoque e desempenho convertidos em tarefas sem duplicação.
- Histórico de sincronização e identificação explícita da origem dos dados.

## Etapas seguintes

1. Integração autorizada com Mercado Livre; depois Amazon, Shopee e Bling. Cada conector depende das permissões e disponibilidade da API do provedor.
2. Relatórios semanais e mensais, comparação de períodos e curva ABC.
3. Assessoria: avaliação de 21 módulos em quatro blocos, pré-requisitos, trilha sugerida e reavaliação. Perguntas e critérios precisam ser definidos; não constam na proposta.
4. Agenda de reuniões, registros, recomendações e acompanhamento por consultor.
5. Resumos por IA com dados rastreáveis e revisão humana; extensão de navegador em projeto separado.

## Regras técnicas

- Demonstração não implica integração real. Dados fictícios devem estar identificados.
- Métricas sem denominador válido ficam indisponíveis, não viram zero artificialmente.
- Tokens ficam no servidor; nunca no navegador, repositório ou logs.
- Em operação com vários clientes, isolamento por organização e permissões devem ser implementados antes do uso real.
- Publicar anúncios e alterar preços/campanhas exige autorização explícita, validação e auditoria.

## Decisões pendentes

Uso para lojas próprias ou assessoria para clientes; prioridade funcional da primeira versão; acesso às contas e aplicações dos provedores.
