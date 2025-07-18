# curly-octo-guacamole (who doesn't love guacamole?)
Testing Accelerators for fptmark

## To Set up repositories similar to this one
If you don't already have pdm:
```
brew install pdm
```

You can init your repository with:
```
pdm init
```

This repository also uses make to automate setup. You can install it on mac with:
```
brew install make
```

For your own repos, you might add dependencies using pdm once initialized:
```
pdm add requests  # Example dependency
pdm add beautifulsoup4 # Example dependency
```

Then you would install with all dependencies with:
```
pdm install
```

## Installing Playwright
```
pdm add pytest-playwright
pdm run python -m playwright install
```

# Run all tests
pdm run pytest -s

# Run just the entity navigation tests
pdm run pytest tests/ui/test_entity_navigation.py

# Run with verbose output
pdm run pytest -v

# Generate Playwright Code
```
pdm run playwright codegen localhost:4200
```