import unittest
import requests
from concurrent.futures import ThreadPoolExecutor


class MyTestCase(unittest.TestCase):

    def send_request(self):
        url = "http://localhost:8000/item"
        headers = {
            "Content-Type": "application/json",
            "tenant_id": "tenant-1"
        }
        data = {
            "name": "example_item_name",
            "price": 60.00,
            "active": True
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code

    def test_something(self):
        num_requests = 20
        response_codes = []
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(self.send_request) for _ in range(num_requests)]
            for future in futures:
                status_code = future.result()
                print(f"Status Code: {status_code}")
                response_codes.append(status_code)

        code_counts = {code: response_codes.count(code) for code in set(response_codes)}
        self.assertEqual(10, code_counts[200])
        self.assertEqual(10, code_counts[429])


if __name__ == '__main__':
    unittest.main()
