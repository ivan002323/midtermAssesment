#!/bin/bash
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp midterm_app_login.py tempdir/.
cp accounts.db tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" >> tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile
echo "COPY ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY midterm_app_login.py /home/myapp/" >> tempdir/Dockerfile
echo "COPY accounts.db /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 8080" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/midterm_app_login.py" >> tempdir/Dockerfile

cd tempdir
docker build -t midtermapp .

docker run -t -d -p 8080:8080 --name apprunning midtermapp

docker ps -a
