# iac-crawler

## Execution Flow
1. Setup
2. Run queries
3. Filter results

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

The first query retrieved repositories with keywords ```microservice``` and ```docker``` in their metadata.

#### Query 2
```query_2.py```

The second query retrieved repositories with keywords ```microservice``` and ```container``` in their metadata.

#### Query 3
```query_3.py```

The third query retrieved repositories with a ```Dockerfile``` that contains ```microservice``` keyword.

#### Query 4
```query_4.py```

The fourth query retrieved repositories with ```docker-compose``` files that contain ```microservice``` keyword.


### Filtering
All the files in the ``results`` folder can be filtered using ``filter_all.sh``
(default stars = 10 and date = 2021-10-01). The results will be stored in the ``results-filtered`` folder.

Otherwise, the filtering can be performed with ```filter.py``` after the execution of one query.

Parameters:

- ```-s```: Minimum number of stars (default stars = 10)
- ```-c```: Latest commit after this date, Y-m-d format (default date = 2021-10-01)
- ```-i```: Input file
- ```-o```: Output file

Example:
```python filter.py -s 10 -c 2021-10-01 -i results/q1.csv -o results/q1-filtered.csv```


### Filtered query
The ```query_filtered.py``` allows to run the **first and second query** with filtering

The query ```-q``` is executed filtering results with more than ```-s``` stars (default stars = 10) and with
the latest commit  after ```-c``` date (default date = 2021-10-01).

Example:
```python query_filtered.py -q 1 -s 10 -c 2021-10-01```
