# Aegis Treasury

Hybrid post-quantum cryptography application (Python + Java).

This repository contains the project skeleton, CI workflows, and project documentation to help you publish and maintain the Aegis Treasury application.

Goals
- Provide hybrid post-quantum cryptography primitives and integrations (Python and Java)
- CI for builds, tests and security scans on Windows
- Automate releases and publishing (PyPI, Maven, GitHub Releases) when credentials are configured

Quickstart

1. Clone the repository:

   git clone https://github.com/garthmoseczo-spec/aegis-treasury.git
   cd aegis-treasury

2. Add your existing project files (if your code is local):

   # from inside your local project directory
   git remote add origin https://github.com/garthmoseczo-spec/aegis-treasury.git
   git branch -M main
   git push -u origin main

   If your local history should be preserved, add the remote and push. If you want to replace the remote, you can force push (careful):

   git push -u origin main --force

3. Python: create a virtualenv and run tests

   python -m venv .venv
   source .venv/bin/activate   # or .venv\\Scripts\\activate on Windows
   pip install -r requirements.txt
   pytest

4. Java (Maven): build and test

   mvn -B test

Repository layout
- /src/backend/   # FastAPI backend core (auth, wallets, transactions, keys, admin)
- /src/licensing/ # License token utilities
- /src/webhook/   # GitHub Marketplace webhook handler
- /src/test/java/ # Java architecture tests
- /tests/

Files added by the initializer
- README.md (this file)
- LICENSE (dual-license reference)
- LICENSE-MIT
- LICENSE-APACHE-2.0
- .gitignore (Python + Java)
- .github/workflows/ci.yml (CI: tests, linters, security scans)
- .github/dependabot.yml
- SECURITY.md
- CONTRIBUTING.md
- tests/test_architecture.py (Python architecture test scaffold)
- src/test/java/com/aegistreasury/ArchUnitTest.java (Java ArchUnit scaffold)

Next steps
- Start the backend API locally:

  uvicorn src.backend.app:app --reload

- Add credentials as GitHub repository secrets if you want automated publishing (PYPI_API_TOKEN, MAVEN_CENTRAL credentials, GITHUB_TOKEN is provided by Actions).
- Extend the in-memory backend services with persistent storage and full cryptography integrations.

If you want I can:
- Add a Releases workflow that builds and attaches artifacts on tag
- Add publishing workflows for PyPI and Maven (you'll need to add repository secrets)
- Add branch protection rules and CODEOWNERS

Contact me with any requests and I'll adjust the repo or CI accordingly.
