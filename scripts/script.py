import argparse
import subprocess
import json
import re

def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class _Const(object):
    @constant
    def GET_PR_DETAILS_CLI_COMMAND() -> str:
        return 'gh pr list --json body --state merged --search {commit_sha}'
    @constant
    def ADO_TAG_PATTERN() -> re.Pattern:
        return r"AB#\d{6}"
    @constant
    def ADO_TAGGING_COMMAND() -> str:
        return 'az boards work-item update --id {work_item_id} --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags={deploy_env}" --output json'
    
CONST = _Const()

def parseArguments():
    parser = argparse.ArgumentParser(description="Utility to tag ADO workitem with deployment environemnt", exit_on_error=False)
    parser.add_argument('--commit-sha', type=str, required=True, dest='commit_sha')
    parser.add_argument('--deploy_env', type=str, required=True, dest='deploy_env')
    return parser.parse_args()

def extractWorkItemIdFromPR(commitSha):
    extractPrBodyCommand = CONST.GET_PR_DETAILS_CLI_COMMAND.format(commit_sha = commitSha)
    
    prBodySubprocessResponse = subprocess.run(extractPrBodyCommand, capture_output=True, shell=True, text=True)
    if prBodySubprocessResponse.returncode != 0:
        raise Exception('Failed to retrieve PR body for commit identified by {} SHA! Reason: {}'.format(commitSha, prBodySubprocessResponse.stderr))
    adoTagsFromPrBody = re.findall(CONST.ADO_TAG_PATTERN, json.loads(prBodySubprocessResponse.stdout)[0]['body'])
    if len(adoTagsFromPrBody) != 1:
        raise Exception('Could not retrieve ADO tag from PR body or there is more than one!')
    
    return adoTagsFromPrBody[0].split('#')[1]

def tagAdoWorkItem(workItemId: str, deploymentEnv: str):
    adoTaggingCommand = CONST.ADO_TAGGING_COMMAND.format(work_item_id = workItemId, deploy_env = deploymentEnv)
    
    adoTaggingSubprocessResponse = subprocess.run(adoTaggingCommand, capture_output=True, shell=True, text=True)
    if adoTaggingSubprocessResponse.returncode != 0:
        raise Exception('Failed to tag ADO work item identified by id [{}] with deployment env [{}]! Reason: {}'.format(workItemId, deploymentEnv, adoTaggingSubprocessResponse.stderr))
    print('Successfully tagged work item identified by id [{}] with deployment env [{}].'.format(workItemId, deploymentEnv))
    
def main():
    args = parseArguments()
    commitSha = args.commit_sha
    deploymentEnv = args.deploy_env
    tagAdoWorkItem(extractWorkItemIdFromPR(commitSha), deploymentEnv)

if __name__ == '__main__':
    try:
        main()
        exit(0)
    except Exception as e:
        print(f'An error occured: {e}')
        exit(1)
