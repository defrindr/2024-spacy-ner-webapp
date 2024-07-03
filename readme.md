# Instalasi

## Requirements
- Python 3.8+
- MySql

# Steps
1. clone repository
```sh
git clone https://github.com/defrindr/2024-spacy-ner-webapp.git
```
2. Install requirements
```sh
pip install -r requirements.txt
```
3. Sesuaikan database pada file ```.flaskenv```
4. Buka phpmyadmin, import file ```db_spacy.sql```
5. Jalankan program
```sh
flask run
```
6. Login dengan akun

```
> username: admin
> password: admin
```