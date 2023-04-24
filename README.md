## Rifas Server

> Backend server for the Rifas web application

### Installation

Install dependencies from `requirements.txt`

- `make install`

### DB Setup

Install [PostgreSQL](https://www.postgresql.org/) and configure:

- CREATE DATABASE rifas;
- CREATE ROLE postgres;
- ALTER USER postgres WITH LOGIN;

Create the database tables using [peewee's suggested method](https://docs.peewee-orm.com/en/latest/peewee/example.html#creating-tables):

```
$ python
>>> from config.init import create_tables
>>> create_tables()
```

### Local Development

Local development is done using [uvicorn](https://www.uvicorn.org/).

- `make start`

### Testing

Testing is done using [pytest](https://docs.pytest.org/en/latest/).

- `make test`

### Model Schema

_users_

```
{
    id: String,
    name: String,
    email: String,
    createdAt: Date,
    updatedAt: Date
}
```

_raffle_

```
{
    id: String,
    user_id: String
    title: String,
    product: String,
    description: String,
    tickets: Number,
    url: String,
    created_at: Date,
    updated_at: Date
}
```
