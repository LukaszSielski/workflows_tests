import subprocess
from subprocess import check_output, CalledProcessError

class AzCli:
    
    def tag_work_items(self, work_items_ids: list[str], tag: str):
        update_result = {}
        for work_item_id in work_items_ids:
            print(f'Trying to tag {work_item_id}')
            output = None
            try:
                output = check_output(f'az boards work-item update --id {work_item_id} --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags={tag}"', shell=True, stderr=subprocess.STDOUT)
                update_result.update({work_item_id: output})
            except CalledProcessError as e:
                print(f"Update process failed for {work_item_id}, error: {e}")
                print(f"{e.output}/{e.returncode}/{e.stdout}/{e.stderr}")
                update_result.update({work_item_id: e.output})
        print(update_result)