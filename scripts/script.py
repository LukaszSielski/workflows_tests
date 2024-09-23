import argparse
from gh_cli import extract_data_by_pattern_from_pr_body, PrState
from az_cli import tag_work_items
from envs_mapping import get_tag

def parseArguments():
    parser = argparse.ArgumentParser(description="Utility to tag ADO workitem with deployment environemnt", exit_on_error=False)
    parser.add_argument('--commit-sha', type=str, required=True, dest='commit_sha')
    parser.add_argument('--deploy-env', type=str, required=True, dest='deploy_env')
    return parser.parse_args()

def main():
    args = parseArguments()
    workItemsIds = extract_data_by_pattern_from_pr_body(args.commit_sha, PrState.MERGED, r'AB#(\d+)')
    tag_work_items(workItemsIds, get_tag(args.deploy_env))
    
if __name__ == '__main__':
    try:
        main()
        exit(0)
    except Exception as e:
        print(f'An error occured: {e}')
        exit(1)
