# Getting started

## Dockerization

### Build Docker image locally and run code inside a container
```
docker-compose up --build -d    
```

### Stop and remove containers
```
docker-compose down
```


## Preview

### UI
`http://localhost:8000/`
![alt text](files/app.png)

### Swagger Documentation
`http://localhost:8000/docs#/`
![alt text](files/swagger.png)

### Logs
`http://localhost:8000/logs`
![alt text](files/logs.png)

## Database schema

* Table `config`
- **id**: SERIAL, PRIMARY KEY
- **status_value**: INTEGER, NOT NULL
- **is_update_enabled**: BOOLEAN, NOT NULL, DEFAULT TRUE
- **Description**: This table stores the configuration settings for the application. It does not have direct relationships with other tables.

* Table `phrases`
- **id**: SERIAL, PRIMARY KEY
- **ru_text**: TEXT
- **en_text**: TEXT
- **Description**: This table contains phrases in RU/EN languages. 

* Table `language_config`
- **id**: SERIAL, PRIMARY KEY
- **language**: VARCHAR(2), NOT NULL
- **Description**: This table represents the language configuration. The table has no database relationship with the phrase table, but the backend code depends on this table and its language column to determine which RU/EN phrases should be retrieved in the UI. This means that if the language column of this table currently has the value EN, then the backend code will only retrieve English text from the phrase table.