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

## Preparar e testar um anúncio

1. Clique em **Preparar anúncio**. O título e a descrição sugeridos usam somente os dados do catálogo e são editáveis.
2. Informe SKU, estoque, preço confirmado e medidas da embalagem. Salve o rascunho.
3. O checklist considera apenas os campos salvos. Estoque zero mantém a pendência para primeiras vendas.
4. Feche, recarregue a página e abra o mesmo produto: os dados devem permanecer.
5. O cartão mostra o preço confirmado quando informado; caso contrário, mostra o preço sugerido do catálogo.
6. Mesmo com o cadastro básico completo, fotos, categoria, atributos, GTIN/isenção e conexão precisam ser validados para publicação.

Teste automatizado: `python -m unittest discover -s tests -v`.

## Atualizar no Windows sem perder rascunhos

Pare o servidor com Ctrl+C. Se baixou o projeto como ZIP, baixe a versão atual no GitHub e substitua `app.py` e `static/index.html` nos mesmos locais. Preserve a pasta `.local` no seu projeto atual: ela contém os rascunhos. Reinicie com `python app.py` e atualize o navegador com Ctrl+F5. Se clonou com Git e não editou os arquivos do código, use `git pull origin main` antes de reiniciar.
