@echo off
@curl -s .
@IF %errorlevel% == 9009 echo "Curl needs to be installed. Check the Readme" else (
mkdir pr

curl https://get.enterprisedb.com/postgresql/postgresql-16.1-1-windows-x64.exe  -o .\pr\postgressinstaller.exe

.\pr\postgressinstaller.exe

curl https://ftp.postgresql.org/pub/pgadmin/pgadmin4/v8.0/windows/pgadmin4-8.0-x64.exe -o .\pr\pgadmin.exe

.\pr\pgadmin.exe

curl https://www.python.org/ftp/python/3.11.0/python-3.11.0rc2-amd64.exe -o .\pr\python311.exe

.\pr\python311.exe

)

