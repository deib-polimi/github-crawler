# iac-crawler

### Setup
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Queries
- The resulting files are stored in the ```results``` folder.
- There are 4 available queries

#### Query 1
```query_1.py```

The first query retrieved repositories with keywords ```microservice``` and ```docker``` in their metadata

#### Query 2
```query_2.py```

The second query retrieved repositories with keywords ```microservice``` and ```container``` in their metadata

#### Query 3
```query_3.py```

The third query retrieved repositories with a ```Dockerfile``` that contains keyword ```microservice```

#### Query 4
```query_4.py```

The fourth query retrieved repositories with ```docker-compose``` files that contain keyword ```microservice```


### Filtering
The filtering is performed with ```filter.py``` after the execution of one query.

Parameters:

- ```-s```: Minimum number of stars (default is 10)
- ```-c```: Latest commit after this date, Y-m-d format (default is 2021-10-01)
- ```-i```: Input file
- ```-o```: Output file

Example:
```python filter.py -s 10 -c 2021-10-01 -i results/q1.csv -o results/q1-filtered.csv```


### Filtered query
The ```query_filtered.py``` allows to run the first and second query with filtering

#### Query filtered
The ```-q``` is executed filtering results with more than ```-s``` stars (default is 10) and with the latest commit
after ```-c``` date (default is 2021-10-01).

Example:
```python query_filtered.py -q 1 -s 10 -c 2021-10-01```
