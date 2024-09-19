from subprocess import check_output, CalledProcessError, STDOUT

class AzCli:
    
    def tag_work_items(self, work_items_ids: list[str], tag: str) -> None:
        update_result = {}
        for work_item_id in work_items_ids:
            print(f'Trying to tag {work_item_id} with tag {tag}')
            try:
                check_output(f'az boards work-item update --id {work_item_id} --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags={tag}"', shell=True, stderr=STDOUT)
                update_result.update({work_item_id: 'Success'})
            except CalledProcessError as e:
                print(f"Update process failed for {work_item_id}, error: {e}")
                update_result.update({work_item_id: e.output})
        print(update_result)