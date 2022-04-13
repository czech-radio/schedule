# Contributing

Thank you for any and all contributions! Following these guidelines will help streamline the process of contributing and make sure that we're all on the same page. While we ask that you read this guide and follow it to the best of your abilities, we welcome contributions from all, regardless of your level of experience.

## Setup

-  Clone the project and move to the folder.
-  Create and activate the virtual environment.
-  Install the package in virtual environment.
-  Write, test and lint the code.

## Test

To run a tests use following commands.

```
pytest -sv                   # Run all tests.
pytest -sv -m domain         # Run domain tests.
pytest -sv -m client         # Run client tests.
pytest -sv -m "not client"   # Run all tests except client.
```

## Lint
```
black .  # Format the code.
isort .  # Sort the imports.
```

## Release

&hellip;
