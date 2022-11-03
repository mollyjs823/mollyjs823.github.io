# Resourceful

## Resource
**Food truck**

Attributes: 
* truck name (string)
* menu item (string)
* rating (integer)
* review (string)
* location (string)

## Schema
```sql
CREATE TABLE trucks (
id INTEGER PRIMARY KEY,
name TEXT,
type TEXT,
rating INTEGER,
review TEXT,
location TEXT);
```

## REST Endpoints

Name                       | Method       | Path
---------------------------|--------------|------------------
Retrieve truck collection  | GET          | /trucks
Retrieve truck member      | GET          | /trucks/*\<id\>*
Create truck member        | POST         | /trucks
Update truck member        | PUT          | /trucks/*\<id\>*
Delete truck member        | DELETE       | /trucks/*\<id\>*

