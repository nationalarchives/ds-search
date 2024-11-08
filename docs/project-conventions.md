# Project conventions

At TNA we follow a set of conventions for our projects to ensure consistency and quality across our codebases. These can be found in our [Engineering handbook](https://nationalarchives.github.io/engineering-handbook/) and should be followed when contributing to the project, as well as the guidance below.

## Python

This project uses a few tools to improve the consistency and quality of Python code:

- [`Black`](https://black.readthedocs.io/en/stable/): An opinionated Python formatter that takes care of code formatting (so we don't have to think about it).
- [`isort`](https://pycqa.github.io/isort/): Ensures that import statements are ordered in a consistant way accross the project.
- [`flake8`](https://flake8.pycqa.org/en/stable/): Catches things like unused parameters, unused imports and other non-formatting related things.

The easiest way to ensure the code you're contributing adheres to these standards is to find and install plugins for your code editor of choice, that will check and transparently reformat your code whenever you save changes. Standard configuration files are included in the root of the repository, which _should_ be picked up and respected by such plugins.

Another option is to run the `format` command from your console to apply `isort` and `Black` formatting to Python code:

```console
docker compose exec dev format
```

`flake8` will just flag things in the terminal, it will not update any code for you like `isort` or `Black`.

This will be checked by CI on every commit, so it's a good idea to run this locally before pushing your changes.

Useful links

- <https://nationalarchives.github.io/engineering-handbook/technology/backend/python/>

## Git/Github conventions

### Branching

- Changes are developed in feature branches and submitted as pull requests via Github
- Feature branches should always be based on: `main`
- Create a new branch if the branch for that ticket has been merged.

### Naming branches

- Use only alphanumeric characters and hyphens where possible and avoid special characters.
- Branch names for ticketed new features should follow: `feature/JIRA-TICKET-NUMBER-with-short-description`
- Branch names for ticketed bug fixes should follow: `fix/JIRA-TICKET-NUMBER-with-short-description`
- Branch names for housekeeping tasks or other unticketed work should follow: `chore/short-description`

For example:

- `feature/UN-123-extra-squiggles`
- `fix/DF-999-image-view-error`
- `chore/update-documentation`

### Naming pull requests

- Pull requests for features and bug fixes should be titled: `JIRA-TICKET-NUMBER: short-description`
- Pull requests for housekeeping tasks or other unticketed work should be titled: `CHORE: short-description`

For example:

- `UN-123: Add extra squiggles`
- `DF-999: Fix image view error`
- `CHORE: Update documentation`

### Merging branches

**NOTE:** Where possible, a feature branch should be kept up-to-date with `main` by regularly merging `main` into the feature branch. This will help to prevent conflicts when merging the feature branch back into `main`, and ensure there are no inconsistencies.

- When merging a feature branch into `main`, use the `Squash and merge` option to keep the commit history clean
