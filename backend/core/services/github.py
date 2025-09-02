import httpx
from typing import List, Dict
from backend.core.models.schemas import IssueOut


async def fetch_issues(owner: str, repo: str, state: str = "open") -> List[IssueOut]:
    """
    Holt Issues aus einem öffentlichen GitHub Repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {"state": state}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        issues = response.json()

    results = []
    for issue in issues:
        # Nur echte Issues (keine Pull Requests)
        if "pull_request" not in issue:
            results.append(IssueOut(
                id=issue["id"],
                number=issue["number"],
                title=issue["title"],
                body=issue.get("body", ""),
                state=issue["state"],
                url=issue["html_url"]
            ))
    return results


async def fetch_and_label_issues(owner: str, repo: str, state: str = "open"):
    """
    Erweiterte Funktion: Issues holen und mit einer Dummy-Label-Logik versehen.
    (Später kannst du hier dein ML-Modell einhängen.)
    """
    issues = await fetch_issues(owner, repo, state)
    labeled = []
    for issue in issues:
        labeled.append({
            "id": issue.id,
            "title": issue.title,
            "state": issue.state,
            "label": "bug" if "error" in issue.title.lower() else "enhancement"
        })
    return labeled
