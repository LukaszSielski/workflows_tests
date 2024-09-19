import re
import subprocess
import json
from typing import TypeVar, Callable

class GitHubCli:
    
    def extract_pr_body(self, commit_sha: str) -> str:
        prDetails = None
        try:
            prDetails = subprocess.check_output(f'gh pr list --json body --state merged --search {commit_sha}', shell=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f'Failed to retrieve PR body! {e.stderr}')
        prDetailsJson = json.loads(prDetails)
        return prDetailsJson[0]['body'] if len(prDetailsJson) == 0 else ''
    
    T = TypeVar('T')
    def extract_data_from_pr_body(self, commit_sha: str, pattern: re.Pattern, mapping: Callable[[str], T]) -> list[T]:
        finds = re.findall(pattern, self.extract_pr_body(commit_sha))
        a = list(map(mapping, finds))
        print(a)
        return a
        
        
        
        
        