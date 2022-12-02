#### The project hosted by following address: https://iban-validator-v.herokuapp.com/

## Create and activate virtual environment:
```bash
python3 -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Linux)
```


## Install dependensies for backend:
```bash
pip install -r requirements.txt
```

## Run server:
```bash
flask --app app --debug run
```

## Init DB:
```bash
flask db init
flask db migrate
flask db upgrade
```


