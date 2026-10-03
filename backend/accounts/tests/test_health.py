from django.test import TestCase
from django.urls import reverse


class HealthEndpointTests(TestCase):
    def test_health_endpoint_checks_database(self):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})

    def test_api_schema_and_docs_are_available(self):
        schema_response = self.client.get(reverse("schema"))
        docs_response = self.client.get(reverse("api-docs"))

        self.assertEqual(schema_response.status_code, 200)
        self.assertEqual(docs_response.status_code, 200)