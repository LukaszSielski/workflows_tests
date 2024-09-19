from subprocess import check_output, CalledProcessError, STDOUT

def tag_work_items(self, work_items_ids: list[str], tag: str) -> None:
    for work_item_id in work_items_ids:
        print(f'Trying to tag {work_item_id} with tag {tag}')
        try:
            check_output(f'az boards work-item update --id {work_item_id} --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags={tag}"', shell=True, stderr=STDOUT)
            print(f'Successfully updated work item {work_item_id} with tag {tag}')
        except CalledProcessError as e:
            print(f"Update process failed for {work_item_id}, error: {e.output}")