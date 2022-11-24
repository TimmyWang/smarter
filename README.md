# Project: Smarter

### Tech stack

- fastapi
- mysql
- docker

### Command

To start the service

```sh
docker compose up
```

To shut down the service

```sh
docker compose down
```

### API usage

To review an order (GET)

```sh
http://localhost:8000/order/{order_id}
```

To add an order (POST)

```sh
http://localhost:8000/order/add
body:
{
  "customer_name": "string",
  "customer_id": "string",
    "items": [
    {
      "product_name": "string",
      "product_id": "string",
      "amount": integer, # must be greater than 0
      "price": integer, # must be greater than 0
    }
  ]
}
```

To modify an order (PUT)

```sh
http://localhost:8000/order/modify/{order_id}
body:
{
  "customer_name": "string",
  "customer_id": "string",
  "items": [
    {
      "product_name": "string",
      "product_id": "string",
      "amount": 0,
      "price": 0,
      "id": 0, # see NOTE
      "delete": false # see NOTE
    }
  ]
}
```

NOTE
"id" and "delete" are optional
| | id not provided | id provided and in the original order| id provided and NOT in the original order|
| ------ | ------ | ------ | ------ |
| delete: true | item will be added to the order | item will be removed from the order | cause error |
| delete: flase or not provided | item will be added to the order | item will be modified | cause error |
