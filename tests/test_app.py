import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import HTTPServer
import app


class DraftWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_store = app.STORE
        app.STORE = Path(self.temp.name) / 'drafts.json'
        self.server = HTTPServer(('127.0.0.1', 0), app.Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        app.STORE = self.old_store
        self.temp.cleanup()

    def save(self, draft):
        request = Request(self.base + '/api/drafts',
                          data=json.dumps({'id': app.PRODUCTS[0]['id'], 'draft': draft}).encode(),
                          headers={'Content-Type': 'application/json'})
        with urlopen(request) as response:
            return json.load(response)

    def products(self):
        with urlopen(self.base + '/api/products') as response:
            return json.load(response)

    def test_partial_old_draft_and_accented_copy_survive_reload(self):
        self.save({'sku': 'CAFÉ-01', 'stock': '0'})
        product = self.products()[0]
        self.assertIn('Estoque maior que zero', product['preparation']['missing'])
        self.assertEqual(product['draft']['sku'], 'CAFÉ-01')
        self.assertIn('Título', product['preparation']['missing'])

    def test_complete_basic_fields_still_require_marketplace_steps(self):
        draft = {key: '10' for key in app.REQUIRED}
        draft.update(title='Café em grãos', description='Descrição com acentos.\n' * 30)
        self.save(draft)
        product = self.products()[0]
        self.assertEqual(product['draft'], draft)
        self.assertEqual(product['preparation']['missing'], [])
        self.assertIn('Conexão com Mercado Livre', product['preparation']['publication_blockers'])
        self.assertEqual(json.loads(app.STORE.read_text(encoding='utf-8'))[product['id']], draft)

    def test_invalid_save_preserves_existing_draft(self):
        self.save({'sku': 'Original'})
        for bad in [{'stock': '-1'}, {'stock': '1.5'}, {'price': 'NaN'}, {'description': 'x' * 5001}]:
            with self.assertRaises(HTTPError) as error:
                self.save(bad)
            self.assertEqual(error.exception.code, 400)
            self.assertEqual(self.products()[0]['draft'], {'sku': 'Original'})

if __name__ == '__main__':
    unittest.main()
