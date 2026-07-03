# Contributing

Merci de votre intérêt pour **Start Time** !

## Signaler un bug

Utilisez le [modèle de bug report](.github/ISSUE_TEMPLATE/bug_report.yml).

## Proposer une fonctionnalité

Utilisez le [modèle de feature request](.github/ISSUE_TEMPLATE/feature_request.yml).

## Setup local

```bash
pip install -r requirements_dev.txt
pipx install prek   # ou : brew install j178/prek/prek
prek install
```

> `prek` est un drop-in Rust de `pre-commit`, nettement plus rapide. Si vous
> préférez la version Python : `pipx install pre-commit && pre-commit install`.
> Le fichier `.pre-commit-config.yaml` est identique pour les deux runners.

## Pull requests

1. Créez une branche dédiée : `git checkout -b feat/ma-fonctionnalite`.
2. Développez, puis lancez les hooks : `prek run --all-files`.
3. Lint : `ruff check . && ruff format --check .`.
4. Tests : `pytest`.
5. Committez en [Conventional Commits](https://www.conventionalcommits.org/) :
   `feat: …`, `fix: …`, `docs: …`. Le changelog et les versions sont générés
   automatiquement par `release-please` à partir de ces préfixes.
6. Poussez et ouvrez une PR vers `main`.

## Gestion des dépendances

Ce repo utilise **Renovate** (pas Dependabot). Les PR de mise à jour sont
ouvertes par `@renovate[bot]` et suivies dans le
[Dependency Dashboard](../../issues?q=is%3Aissue+author%3Aapp%2Frenovate).
