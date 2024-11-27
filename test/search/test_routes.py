from django.test import TestCase


class SearchTestCase(TestCase):
    def test_start_page(self):
        rv = self.client.get("/search/")
        self.assertContains(
            rv,
            '<h1 class="tna-heading-xl">Search</h1>',
            status_code=200,
        )

    def test_catalogue(self):
        rv = self.client.get("/search/catalogue/")
        self.assertContains(
            rv, '<h1 class="tna-heading-xl">Catalogue search results</h1>', status_code=200
        )
