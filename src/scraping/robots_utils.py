import urllib.robotparser
from urllib.parse import urljoin

USER_AGENT = "ResearchBot/1.0"

def is_allowed(base_url: str, target_url: str) -> bool:
    robots_url = urljoin(base_url, "/robots.txt")
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
        return rp.can_fetch(USER_AGENT, target_url)
    except Exception:
        return False