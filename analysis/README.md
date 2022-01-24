# Analysis of collected data

Tn this directory is a jupyter notebook, which performs an analysis of some of the data Pepper collected.
It includes visualizations, linear regression and also tensorflow is used here.

The `Client` class in the `Client` module is used to easily access the data in the database. This requires a running instance of the node application.

To use the data, an API key is needed, which is stored in the web application. this key should be stored in a file named .env `API_KEY` (see .example.env).

There is also a script which should be run weekly to generate weekly reports of peppers collected data.

# Install required modules

```bash
analysis~$ bash install.sh
```

# TODO

- add real data
- improve tf model
