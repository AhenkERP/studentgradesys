#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# When postgres is ready, we can run database operations
python manage.py makemigrations
python manage.py makemigrations accounts
python manage.py makemigrations lesson
python manage.py makemigrations grade


# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Change permissions of static files added by collectstatic
chmod -R 755 /app/static

# Create a superuser from environment variables
python manage.py create_super_user_from_env


exec "$@"