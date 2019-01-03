## FLASK RESTFUL API BOILERPLATE

### Console commands

- To run application: `flask run`

### Database migration

1. Initiate a migration folder (once only)

```bash
flask db init
```

2. Create migration script from detected changes in the model
```bash
flask db migrate --message 'initial database migration'
```

3. Apply the migration script to the database
```bash
flask db upgrade
``` 

### Viewing the app ###

Open the following url on your browser to view swagger documentation
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)


### Contributing
If you want to contribute to this boilerplate, clone the repository and just start making pull requests.
