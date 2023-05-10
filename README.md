# edulynx

A python FastApi Application to manage courses.

## Setting up the project

1. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

2. Initialize poetry and install `pre-commit` hooks:

```bash
make install
make pre-commit-install
```

3. Run the codestyle:

```bash
make codestyle
```

4. Run the application:

```bash
poetry run edulynx
```

## Run Tests

``` bash
make test
```
