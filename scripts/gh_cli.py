import re
import json
from enum import Enum
from subprocess import check_output

class PrState(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    MERGED = 'merged'
    ALL = 'all'

class PrNotFoundException(Exception):
    def __init__(self, commit_sha: str):
        super().__init__(f"Could not find pull request for commit identitifed by {commit_sha} SHA")

def extract_pr_body(commit_sha: str, pr_state: PrState) -> str:
    prDetails = check_output(f'gh pr list --json body --state {pr_state.value} --search {commit_sha}', shell=True, text=True)
    prDetailsJson = json.loads(prDetails)
    if len(prDetailsJson) == 0:
        raise PrNotFoundException(commit_sha)
    return prDetailsJson[0]['body']

def extract_data_by_pattern_from_pr_body(commit_sha: str, pr_state: PrState, pattern: re.Pattern) -> list[str]:
    return re.findall(pattern, extract_pr_body(commit_sha, pr_state))