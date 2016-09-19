from unittest import main
from knimin.tests.tornado_test_base import TestHandlerBase
from knimin import db


class TestAgSearch(TestHandlerBase):
    def test_get_not_authed(self):
        response = self.get('/ag_search/')
        self.assertEqual(response.code, 200)
        self.assertTrue(
            response.effective_url.endswith('?next=%2Fag_search%2F'))

    def test_get(self):
        self.mock_login_admin()
        response = self.get('/ag_search/')
        self.assertEqual(response.code, 200)
        self.assertIn('Find stuff.', response.body)

    def test_post(self):
        self.mock_login_admin()
        details = db.getAGBarcodeDetails('000004216')
        payload = {'barcode': '000004216',
                   'ag_kit_id': details['ag_kit_id'],
                   'site_sampled': details['site_sampled'],
                   'sample_date': details['sample_date'],
                   'sample_time': details['sample_time'],
                   'participant_name': details['participant_name'],
                   'notes': details['notes'],
                   'environment_sampled': details['environment_sampled']}

        if details['refunded'] is None:
            payload['refunded'] = 'N'
        else:
            payload['refunded'] = details['refunded']
        if details['withdrawn'] is None:
            payload['withdrawn'] = 'N'
        else:
            payload['withdrawn'] = details['withdrawn']

        payload['search_term'] = 'test'
        response = self.post('/ag_search/', payload)
        self.assertIn('TESTDUDE', response.body)
        self.assertIn('TESTOTHER', response.body)
        self.assertIn('United Kingdom', response.body)
if __name__ == "__main__":
    main()
