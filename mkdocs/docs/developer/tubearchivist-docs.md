# Contributing to tubearchivist-docs as a developer

## Developement Environment
As outlined in the [README](README.md), you can run a local development server with:

```bash
pip install -r requirements.txt
mkdocs serve -f mkdocs/mkdocs.yml
```

If you have a port conflict, you can change the port with:

```bash
mkdocs serve -f mkdocs/mkdocs.yml -a "0.0.0.0:8001"
```

## Outline
This project makes use of the [MkDocs](https://www.mkdocs.org/) framework.

- There's a single configuration file named mkdocs.yml, and a folder named docs that will contain your documentation source files.

## Contributing
Fork the repo, make your changes, and open a Pull Request.