import re
import subprocess
import json

class GitHubCli:
    
    def extract_pr_body(self, commit_sha: str) -> str:
        prDetails = None
        try:
            prDetails = subprocess.check_output(f'gh pr list --json body --state merged --search {commit_sha}', shell=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f'Failed to retrieve PR body! {e.stderr}')
        prDetailsJson = json.loads(prDetails, strict=False)
        print(prDetailsJson)
        return prDetailsJson[0]['body'] if len(prDetailsJson) != 0 else ''
    
    def extract_data_from_pr_body(self, commit_sha: str, pattern: re.Pattern) -> list[str]:
        print(self.extract_pr_body(commit_sha))
        return re.findall(pattern, self.extract_pr_body(commit_sha))
        
        
        
        
        