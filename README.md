# PADB Mindemeet P2

## Running DB

```
docker run --name padb-database -e POSTGRES_PASSWORD=postgres -d postgres
```

## Commands

```
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "Your Room Name",
  "description": "Your Room Description",
  "enable": true,
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}' http://localhost:5000/api/v1/rooms
```
