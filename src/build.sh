set -o errexit

pip install -r src/requirements.txt

python src/manage.py collectstatic --noinput    

python src/manage.py migrate