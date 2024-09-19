import re
import subprocess
import json

class GitHubCli:
    
    def extract_data_from_pr_body(self, commit_sha: str, pattern: re.Pattern) -> list[str]:
        prDetails = None
        try:
            prDetails = subprocess.check_output(f'gh pr list --json body --state merged --search {commit_sha}', shell=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f'Failed to retrieve PR body! {e.stderr}')
        prDetailsJson = json.loads(prDetails)
        print(prDetailsJson)
        if len(prDetailsJson) == 0:
            return ''
        finds = re.findall(pattern, prDetailsJson[0]['body'])
        a = list(map(lambda e: e.split('#')[1], finds))
        print(a)
        return a
        
        
        
        
        