curl -X POST \
  http://localhost:3000/api/rels/ \
  -H 'Content-Type: application/json' \
  -d '{
    "node1": "11",
    "node2": "22",
    "relationship_name": "RELATIONSHIP_NAME"
}'
