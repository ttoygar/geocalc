# geocalc

*geocalc* is a program based on Flask framework designed to calculate the closest distance to "MKAD" of any address given as http query.


## Installation

clone this repository and set into environment variables
```bash
$ FLASK_APP=fgeocoder
```

register the blueprint
```python
from .geocalc.geocalc import geocalc

app.register_blueprint(geocalc)
```

run from main directory
```
...\geocalc>flask run
```

## Usage

Reads the address from query and saves the distance to geoc.log and geoc.csv on root directory. Also prints the result on html page.
```python

# returns 1776.8430545711326 km
http://localhost:5000/?address=Ankara

# returns 2485.7898310323476 km
http://localhost:5000/?address=London
```
