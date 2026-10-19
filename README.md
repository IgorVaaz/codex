# Central de anúncios de cafés

Primeira versão local para preparar os oito produtos do catálogo enviado. Sem dependências externas: Python 3.12 ou posterior.

## Executar

```sh
cd /workspace/codex
python app.py
```

Servidor local na porta 8000 (configure `PORT` se necessário). Interface com busca, filtro por marca, edição de rascunhos persistidos e exportação JSON. Os dados editados ficam em `.local/drafts.json`, ignorado pelo Git. O catálogo de referência fica em `data/catalogo.json` e não é sobrescrito pela edição.

## Limites

Não há integração, autenticação ou publicação real. Serviço restrito ao loopback para desenvolvimento; não expor em produção. Preços são sugestões do catálogo, não preços aprovados. Peso do produto não substitui peso de envio. Fotos não foram extraídas ou aprovadas. Estoque, GTIN, medidas, categoria e atributos devem ser verificados. Não há alegação de prontidão para publicação.

Próxima etapa: conexão OAuth oficial com Mercado Livre, credenciais seguras, consulta das regras de categoria e revisão explícita do anúncio antes de envio. Outros canais entram depois. A aplicação não altera preços ou estoque em contas externas.
