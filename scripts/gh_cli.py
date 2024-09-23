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
    def __init__(self, message):
        super().__init__(message)

def extract_pr_body(commit_sha: str, pr_state: PrState) -> str:
    prDetails = None
    try:
        prDetails = check_output(f'gh pr list --json body --state {pr_state.value} --search {commit_sha}', shell=True, text=True, stderr=STDOUT)
    except CalledProcessError as e:
        raise GhCliException(f'Failed to execute GH CLI command! Error: {e.output}')
    prDetailsJson = json.loads(prDetails)
    print(prDetails)
    print(prDetailsJson)
    return prDetailsJson[0]['body'] if len(prDetailsJson) != 0 else ''

def extract_data_by_pattern_from_pr_body(commit_sha: str, pr_state: PrState, pattern: re.Pattern) -> list[str]:
    return re.findall(pattern, extract_pr_body(commit_sha, pr_state))