# Contribution checks

For every change to Python code, do not consider the task complete until both
commands pass from the repository root:

```sh
pylint $(git ls-files 'bink/*.py')
python -m unittest discover -v
```

Fix pylint findings in the code; do not silence them with broad disables or
configuration changes unless the warning is demonstrably inapplicable.

Do not create, update, or publish a release while either check fails. Run the
same checks again immediately before committing or handing off a release.
