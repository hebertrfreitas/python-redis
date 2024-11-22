curl -X POST "http://localhost:8000/item" \
-H "Content-Type: application/json" \
-H "tenant_id: tenant-1" \
-d '{"name": "example_item_name", "price": 60.00, "active": true}'