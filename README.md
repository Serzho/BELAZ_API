# BELAZ_API
Backend application for parse belaz lineup
Using BeautifulSoup, SQLAlchemy, Alembic, FastAPI, PyTest, Requests, Docker  

## Install requirements  
`$pip install -r requirements.txt`  
Or run `setup.bat`  

## Starting
Application without docker starting by `setup.bat` or `uvicorn core.endpoints.endpoints:app`  
Database with lineup information saving in file `belaz.db`  
Logging info saving in file `log.txt`  

## Docker
Application prepared for using in docker image.  
Building docker image by command `docker-compose build`  
Starting by command `docker-compose up -d`  
Getting output of application by command `docker-compose logs -f`  
