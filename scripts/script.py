import argparse
import subprocess
from gh_cli import GitHubCli, PrState
from az_cli import AzCli

class _Const(object):
    def ADO_TAGGING_COMMAND() -> str:
        return 'az boards work-item update --id {work_item_id} --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags={deploy_env}" --output json'
    
CONST = _Const()

def parseArguments():
    parser = argparse.ArgumentParser(description="Utility to tag ADO workitem with deployment environemnt", exit_on_error=False)
    parser.add_argument('--commit-sha', type=str, required=True, dest='commit_sha')
    parser.add_argument('--deploy_env', type=str, required=True, dest='deploy_env')
    return parser.parse_args()

def tagAdoWorkItem(workItemId: str, deploymentEnv: str):
    adoTaggingCommand = CONST.ADO_TAGGING_COMMAND.format(work_item_id = workItemId, deploy_env = deploymentEnv)
    
    adoTaggingSubprocessResponse = subprocess.run(adoTaggingCommand, capture_output=True, shell=True, text=True)
    if adoTaggingSubprocessResponse.returncode != 0:
        raise Exception('Failed to tag ADO work item identified by id [{}] with deployment env [{}]! Reason: {}'.format(workItemId, deploymentEnv, adoTaggingSubprocessResponse.stderr))
    print('Successfully tagged work item identified by id [{}] with deployment env [{}].'.format(workItemId, deploymentEnv))
    
def main():
    args = parseArguments()
    gh_cli = GitHubCli()
    az_cli = AzCli()
    commitSha = args.commit_sha
    deploymentEnv = args.deploy_env
    # tagAdoWorkItem(extractWorkItemIdFromPR(commitSha), deploymentEnv)
    workItemsIds = gh_cli.extract_data_by_pattern_from_pr_body(commitSha, PrState.MERGED, r'AB#(\d+)')
    az_cli.tag_work_items(workItemsIds, deploymentEnv)
    
if __name__ == '__main__':
    try:
        main()
        exit(0)
    except Exception as e:
        print(f'An error occured: {e}')
        exit(1)
