# leapfrog_leave_assessment
A leave analysis platform built for Growth Assessment Program

**Project Structure**

1. Backend - Bakend Module
2. Db - Database Module 
3. Utils - Utility function used in overall project
4. Visuaization - Module for dashboard

## How to setup the project?

### Requirements

`pip install -r requirements.txt`
```
black
fastapi 
plotly
psycopg2-binary
requests
sqlfluff
streamlit
matplotlib
python-dotenv
uvicorn
httpx
asyncpg
asyncio
argparse
```

### Database Setup

Inside the db folder we have a `docker-compose` file to pull the docker image for our postgres database.

```
docker compose pull postgres
```

Once, the postgres image is pulled, you can create your own credentials to access the database:
```
docker run --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=adminpassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
```

You can even create user by going to the command line:
```
docker exec -it my-postgres psql -U admin -d mydatabase

CREATE USER newuser WITH PASSWORD 'newpassword';

GRANT ALL PRIVILEGES ON DATABASE mydatabase TO newuser;
```

### Backend Setup
The backend API is based on fastapi. You can run this command in backend folder.
```
uvicorn main:app --reload
```
### Database Migration
Inside db folder, we have a python file `db_migrate` which helps to create required tables in the database.

Migration Up
```
python db_migrate --up
```

Migration Down
```
python db_migrate --down
```
### Dashboard Setup

Streamlit is used to build dashboard. We can run this command to setup the streamlit application.

```
streamlit run --server.allowRunOnSave=True Home.py 
```

Additionally, we have `.env.example` wherever required.

# Note: The detailed documentation can be found inside the documentation folder