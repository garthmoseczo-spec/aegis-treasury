Releases and Publishing (GitHub Packages)

Workflows added:
- .github/workflows/release.yml — builds Python and Java artifacts on tag (v*) and creates a GitHub Release with attached artifacts.
- .github/workflows/publish-pypi.yml — publishes Python package to PyPI on tag (v*). Requires a repository secret named PYPI_API_TOKEN.
- .github/workflows/publish-maven-gpr.yml — deploys Java artifacts to GitHub Packages (Maven) on tag (v*). This uses the automatically provided GITHUB_TOKEN; no extra secrets required for basic publishing to GitHub Packages.

Secrets to add (if you want PyPI publishing):
- PYPI_API_TOKEN

Branch protection

I cannot apply branch protection rules directly from here. To enable recommended protection for the main branch, run the GitHub CLI command below (you must have admin rights on the repository and gh installed and authenticated).

Recommended rules for branch: main
- Require status checks to pass before merging: the CI checks "Python tests (Windows)", "Java (Maven) build (Windows)", and "CodeQL analysis".
- Require pull request reviews before merging: 1 approval required.
- Dismiss stale pull request approvals when new commits are pushed.
- Enforce for administrators: yes.

Run this command locally to apply the protection (replace OWNER and REPO if needed):

OWNER="garthmoseczo-spec"
REPO="aegis-treasury"

gh api --method PUT /repos/$OWNER/$REPO/branches/main/protection -f required_status_checks='{"strict":true,"contexts":["Python tests (Windows)","Java (Maven) build (Windows)","CodeQL analysis"]}' -f enforce_admins=true -f required_pull_request_reviews='{"dismiss_stale_reviews":true,"required_approving_review_count":1}' -f restrictions='null'

Alternatively enable protection via: Settings → Branches → Add rule → protect main.
