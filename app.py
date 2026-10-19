"""Catálogo local de preparação de anúncios. Não publica em marketplaces."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parent
STORE = ROOT / '.local' / 'drafts.json'
PRODUCTS = json.loads((ROOT / 'data/catalogo.json').read_text(encoding="utf-8"))
FIELDS = {'sku', 'stock', 'price', 'ean', 'height', 'width', 'length', 'shipping_weight', 'title', 'description'}

REQUIRED = {
    'title': 'Título', 'description': 'Descrição', 'sku': 'SKU',
    'stock': 'Estoque maior que zero', 'price': 'Preço de venda',
    'height': 'Altura', 'width': 'Largura', 'length': 'Comprimento',
    'shipping_weight': 'Peso para envio',
}

def preparation(draft):
    missing = [label for key, label in REQUIRED.items()
               if not draft.get(key, '').strip() or (key == 'stock' and float(draft[key]) <= 0)]
    return {'missing': missing, 'completed': len(REQUIRED) - len(missing),
            'total': len(REQUIRED),
            'status': 'Cadastro básico completo' if not missing else 'Dados pendentes',
            'publication_blockers': ['Fotos individuais', 'Categoria e atributos do canal',
                                     'Validação de GTIN ou isenção', 'Conexão com Mercado Livre']}

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, payload, content_type='application/json; charset=utf-8'):
        body = payload.encode() if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/api/products':
            drafts = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
            return self.respond(200, [{**p, 'draft': drafts.get(p['id'], {}), 'preparation': preparation(drafts.get(p['id'], {}))} for p in PRODUCTS])
        if self.path == '/':
            return self.respond(200, (ROOT / 'static/index.html').read_text(encoding="utf-8"), 'text/html; charset=utf-8')
        self.respond(404, {'error': 'Não encontrado'})

    def do_POST(self):
        if self.path != '/api/drafts':
            return self.respond(404, {'error': 'Não encontrado'})
        # Accept only same-origin browser writes; this service is for local development.
        origin = self.headers.get('Origin')
        if origin and origin != 'http://' + self.headers.get('Host', ''):
            return self.respond(403, {'error': 'Origem inválida'})
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length < 1 or length > 64000:
                raise ValueError('Tamanho inválido')
            body = json.loads(self.rfile.read(length))
            if body.get('id') not in {p['id'] for p in PRODUCTS}:
                raise ValueError('Produto inválido')
            draft = body['draft']
            if not isinstance(draft, dict) or set(draft) - FIELDS:
                raise ValueError('Campos inválidos')
            for key, value in draft.items():
                if not isinstance(value, str) or len(value) > (5000 if key == 'description' else 150 if key == 'title' else 100):
                    raise ValueError('Valor inválido')
                if value and key not in {'sku', 'ean', 'title', 'description'}:
                    import math
                    number = float(value)
                    if not math.isfinite(number) or number < 0 or (key != 'stock' and number == 0):
                        raise ValueError('Valor numérico inválido')
                    if key == 'stock' and not number.is_integer():
                        raise ValueError('Estoque deve ser inteiro')
            drafts = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
            drafts[body['id']] = draft
            STORE.parent.mkdir(exist_ok=True)
            temp = STORE.with_suffix('.tmp')
            temp.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
            temp.replace(STORE)
            self.respond(200, {'saved': True})
        except (ValueError, KeyError, TypeError):
            self.respond(400, {'error': 'Revise os campos: estoque inteiro e medidas/preço positivos.'})

if __name__ == '__main__':
    print(f"Central de cafés: http://127.0.0.1:{os.environ.get('PORT', '8000')}/ — Ctrl+C para encerrar", flush=True)
    HTTPServer(('127.0.0.1', int(os.environ.get('PORT', '8000'))), Handler).serve_forever()
