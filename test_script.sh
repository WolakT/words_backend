curl -X POST \
  http://localhost:3000/api/rels/ \
  -H 'Content-Type: application/json' \
  -d '{
    "node1": "test1",
    "node2": "test2",
    "relationship_name": "RELATES"
}'
