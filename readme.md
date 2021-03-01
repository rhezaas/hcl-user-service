# HCl:Service - User-Service
This Service build to manage user activities

## Tech used
1. Python
2. PostgreSQL
3. Flask
4. SQLAlchemy

## Installation
1. Run initial setup

```bash
> ./setup
```

2. Enter Python virtual environment

```bash
> source venv/bin/activate
```

3. Install dependencies
```
> pip3 install -r requirements.txt
```

4. Add your dotenv files, to put any credentials
```
#=====================================
# API
#=====================================
API_SECRET=
ENV=
DEBUG=
PORT=

#=====================================
# DATABASE
#=====================================
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=
DB_NAME=
```

4. Run it
```
> start
``` 