import re
import json
from enum import Enum
from subprocess import check_output, CalledProcessError, STDOUT

class PrState(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    MERGED = 'merged'
    ALL = 'all'

def extract_pr_body(commit_sha: str, pr_state: PrState) -> str:
    prDetails = None
    try:
        prDetails = check_output(f'gh pr list --json body --state {pr_state.value} --search {commit_sha}', shell=True, text=True, stderr=STDOUT)
    except CalledProcessError as e:
        raise Exception(f'Failed to retrieve PR body! {e.output}')
    prDetailsJson = json.loads(prDetails)
    return prDetailsJson[0]['body'] if len(prDetailsJson) != 0 else ''

def extract_data_by_pattern_from_pr_body(commit_sha: str, pr_state: PrState, pattern: re.Pattern) -> list[str]:
    return re.findall(pattern, extract_pr_body(commit_sha, pr_state))