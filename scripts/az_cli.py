from subprocess import check_call

class AzCliException(Exception):
    def __init__(self, error):
        super().__init__(f'Failed to execute AZ CLI command! Error: {error}')

def tag_work_items(work_items_ids: list[str], tag: str) -> None:
    for work_item_id in work_items_ids:
        check_call(f'az boards work-item update --id {work_item_id} --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags={tag}"', shell=True)
        print(f'Successfully updated work item {work_item_id} with tag {tag}')
            