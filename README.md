# FLASK RESTFUL API BOILERPLATE

## Flask command line
### List all commands
```
flask
```
### Start api application
```
flask run
```

## Config environment variables in `.env` file

- Generate a good secret key: 
```
python -c 'import os; print(os.urandom(24))'
```
More detail at: https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions

- Create `.env` at project root folder with following content:
```
SECRET_KEY={generated secret}
DATABASE_URL=mysql+pymysql://user:password@host:port/database
TEST_DATABASE_URL=mysql+pymysql://user:password@host:port/database
ORIGIN_ALLOW_DOMAIN=*
DEPLOYMENT_ENV=dev
```

- Available environments for `DEPLOYMENT_ENV`: `dev` | `test` | `prod`

## Database migration

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

## Viewing the app

Open the following url on your browser to view swagger documentation
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)


## Contributing
If you want to contribute to this boilerplate, clone the repository and just start making pull requests.
