echo "BUILD START"
python 3.11.3 -m pip install -r requirements.txt
python 3.11.3 manage.py collectstatic --noinput --clear
echo  "BUILD END"