import re
import subprocess

class GitHubCli:
    
    def extract_data_from_pr_body(self, commit_sha: str, pattern: re.Pattern):
        prBody = None
        try:
            prBody = subprocess.check_output(f'gh pr list --json body --state merged --search {commit_sha}', text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f'Failed to retrieve PR body! {e.stderr}')
        print(prBody)
        