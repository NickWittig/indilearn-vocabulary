# Development

### Linting and Code Style

This project uses `black`, `flake8`, and `pylint` for code style and linting. You can run them with the following commands:

```bash
black .
flake8 .
pylint **/*.py
```

## Testing

This project uses `pytest` for testing. To run the tests, use the following command:

```bash
pytest
```

### Continuous Integration

The project includes a file for setting up CI/CD with GitHub. The pipeline runs linting.

