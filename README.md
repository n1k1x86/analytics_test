# analytics_test

#first
run django application:

1) clone repo
2) install requirements (exec: pip install -r requirements.txt)
3) go to my_sql/
4) exec: docker-compose run --service-ports database
5) run django app on port 7000 (exec: python manage.py runserver 0.0.0.0:7000)

#second
run matomo

1) exec: docker run -d -p 80:80 --link {my_sql_container_name}:matomo_db -v matomo:/var/www/html matomo
