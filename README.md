# Resourceful

## Resources
**Food truck**

Attributes: 
* truck name (string)
* menu item (string)
* rating (integer)
* review (string)
* location (string)

**User**
Attributes: 
* email (string)
* fname (string)
* lname (integer)
* enc_password (string)


## Trucks Schema
```sql
CREATE TABLE trucks (
id INTEGER PRIMARY KEY,
name TEXT,
type TEXT,
rating INTEGER,
review TEXT,
location TEXT);
```

```sql
CREATE TABLE truck_metadata (
id INTEGER PRIMARY KEY, 
slug TEXT, 
name TEXT, 
cuisine TEXT);
```


## Users Schema
```sql
CREATE TABLE users (
id INTEGER PRIMARY KEY, 
email TEXT, 
fname TEXT, 
lname TEXT, 
enc_password TEXT);
```

## REST Endpoints

Name                        | Method       | Path
----------------------------|--------------|------------------
Retrieve truck collection   | GET          | /trucks
Retrieve truck member       | GET          | /trucks/*\<id\>*
Create truck member         | POST         | /trucks
Update truck member         | PUT          | /trucks/*\<id\>*
Delete truck member         | DELETE       | /trucks/*\<id\>*
Retrieve user collection    | GET          | /users
Retrieve single user        | GET          | /users/*<id\>*
Create single user          | POST         | /users
Log user in/ Create session | POST         | /sessions
Log user out/ Delete session| POST         | /logout

## Password hashing method
Bcrypt hashing