import subprocess
from subprocess import check_output, CalledProcessError

class AzCli:
    
    def tag_work_items(self, work_items_ids: list[str], tag: str):
        update_result = {}
        for work_item_id in work_items_ids:
            output = None
            try:
                output = check_output(f'az boards work-item update --id {work_item_id} --fields "System.Tags={tag}', shell=True, stderr=subprocess.STDOUT)
            except CalledProcessError as e:
                update_result.update({work_item_id: e.stderr})
            update_result.update({work_item_id: output})
        print(update_result)