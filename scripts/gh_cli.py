import re
import json
from enum import Enum
from subprocess import check_output, CalledProcessError, STDOUT

class PrState(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    MERGED = 'merged'
    ALL = 'all'
    
class GhCliException(Exception):
    def __init__(self, error):
        super().__init__(f'Failed to execute GH CLI command! Error: {error}')

class PrNotFoundException(Exception):
    def __init__(self, commit_sha: str):
        super().__init__(f"Could not find pull request for commit identitifed by {commit_sha} SHA")

def extract_pr_body(commit_sha: str, pr_state: PrState) -> str:
    prDetails = None
    try:
        prDetails = check_output(f'gh pr list --json body --state {pr_state.value} --search {commit_sha}', shell=True, text=True, stderr=STDOUT)
    except CalledProcessError as e:
        raise GhCliException(e.output)
    
    prDetailsJson = json.loads(prDetails)
    if len(prDetailsJson) == 0:
        raise PrNotFoundException(commit_sha)
    return prDetailsJson[0]['body']

def extract_data_by_pattern_from_pr_body(commit_sha: str, pr_state: PrState, pattern: re.Pattern) -> list[str]:
    return re.findall(pattern, extract_pr_body(commit_sha, pr_state))