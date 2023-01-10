## Rifas Server

> Backend server for the Rifas web application

### Installation

### Local Development

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
