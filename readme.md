### Tech-Stack

-   python
-   fastAPI
-   postGRES
-   SQLAlchemy

### Steps

-   Create venv

    -   py -3 -m venv \<name>
    -   select python interpretor for this venv from view->command palette-> select py interp

-   pip install fastapi[all]
-   create http requests

### Code Snippets

```python
@app.get("/") #decorator
```

-   app is the instance of fastapi
-   get is the http request
-   "/" root path
