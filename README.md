### BD2-projekt
## Spis treści
* [Opis](#opis)
* [Technologie](#technologie)
* [Uruchomienie](#uruchomienie)
* [Autorzy](#autorzy)

 ## Opis
Projekt na kurs Bazy danych 2 u Dr Łopuszyńskiego
Aplikacja z użyciem FLASK ala Netflix z logowaniem i bazą dancyh w PostgreSQL.

 ## Technologie
Projekt ten został napisany w języku Python z wykorzystanie frameworka Flask oraz systemem PostgreSQL.

## Uruchomienie
Aby lokalnie uruchomić projekt, najpierw należy sklonować repozytorium

``` bash
git clone https://github.com/Szymon1905/BD2-projekt.git
```
Następnie zainstalować wymagane biblioteki

```bash
pip install -r requirements.txt
```
Aby aplikacja mogła poprawnie łączyć się z bazą danych, w folderze projektu należy stworzyć plik `.env` i uzupełnić go o poniższe zmienne

```python
    DEV_DATABASE_URL = 'postgresql://user:password@host:5432/dev-database'
    SECRET_KEY = 'SECRET_KEY'

    DATABASE_USER = 'user'
    DATABASE_PASSWORD = 'password'
    DATABASE_NAME = 'dev-database'
    DATABASE_HOST = 'host'
    DATABASE_PORT = 5432
```
Aby uruchomić aplikację, w folderze projektu wystarczy wpisać

```bash
flask run
```

Aplikacja uruchomiona jest pod adresem http://127.0.0.1:5000 .

## Autorzy
Autorami projektu są Szymon Borzdyński i Katarzyna Matuszek