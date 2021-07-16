# Date Calculator

This is a dedicated date calculator made for a scientific experiment.

## Usage

### Shell Version

Use docker to run the shell version, please ensure you have docker installed and started.

Firstly, build the image:

```shell
make build_shell
```

and then you can run the shell interface for the calculator:

```shell
make run_shell
```

now you can start to play with the calculator. Input the following command and you will see the result:

```shell
/code/examples/shell # python calculator.py "2/3/2020" "5/3/2020"
2/3/2020 - 5/3/2020 = 2 days
```

the default format is `%d/%m/%Y`, you can also specify a date format by using `--fmt` to use a different format.

### API Version

We also use docker to run the API version, please ensure you have docker installed and started.

Firstly, build the image:

```shell
make build_api
```

and then you can run the api server for the calculator:

```shell
make run_api
```

now you can start to play with the API version calculator by accessing http://localhost:8089 in your browser.

## Tests

### Test the `scidate` library

You can run the docker to test the scidate library:

```shell
make test_scidate
```

It will show test result together with coverage.

### Test the command-line tool

You can go into the `examples/shell` directory, you can find a `requirements_test.txt` file. In order to run the unit tests, you can do:

```shell
python -m venv venv
. venv/bin/activate
pip install -r requirements_test.txt
python -m unittest
```

### Test the API version of the calculator

Similar to the command-line tool, you can go into the `examples/shell` directory, and you can find a `requirements_test.txt` file. Execute the following command to run the unit tests:

```shell
python -m venv venv
. venv/bin/activate
pip install -r requirements_test.txt
pytest
```
