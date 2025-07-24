import io
from .connection import Connection
from .models import Backup, BackupTarget, BackupRecycleCriteria, BackupRecycleAction, BackupType

class BackupchanAPIError(Exception):
    pass

def check_success(response: tuple[dict, int]) -> dict:
    data, status = response
    if not data.get("success", False):
        raise BackupchanAPIError(f"Server returned error: {data} (code {status})")
    return data

class API:
    def __init__(self, host: str, port: int, api_key: str):
        self.connection = Connection(host, port, api_key)

    # TODO error handling

    def list_targets(self) -> list[BackupTarget]:
        response = self.connection.get("target")
        targets = response[0]["targets"]
        return [BackupTarget.from_dict(target) for target in targets]

    def new_target(self, name: str, backup_type: BackupType, recycle_criteria: BackupRecycleCriteria, recycle_value: int, recycle_action: BackupRecycleAction, location: str, name_template: str, deduplicate: bool) -> str:
        """
        Returns ID of new target.
        """
        data = {
            "name": name,
            "backup_type": backup_type,
            "recycle_criteria": recycle_criteria,
            "recycle_value": recycle_value,
            "recycle_action": recycle_action,
            "location": location,
            "name_template": name_template,
            "deduplicate": deduplicate
        }
        resp_json, _ = self.connection.post("target", data)
        return resp_json["id"]

    def upload_backup(self, target_id: str, file: io.IOBase, filename: str, manual: bool) -> str:
        """
        Returns ID of new backup.
        """
        data = {
            "manual": int(manual)
        }

        files = {
            "backup_file": (filename, file)
        }

        response = self.connection.post_form(f"target/{target_id}/upload", data=data, files=files)
        resp_json = check_success(response)
        return resp_json["id"]

    def get_target(self, id: str) -> tuple[BackupTarget, list[Backup]]:
        response = self.connection.get(f"target/{id}")
        resp_json = check_success(response)
        return BackupTarget.from_dict(resp_json["target"]), [Backup.from_dict(backup) for backup in resp_json["backups"]]

    def edit_target(self, id: str, name: str, recycle_criteria: BackupRecycleCriteria, recycle_value: int, recycle_action: BackupRecycleAction, location: str, name_template: str, deduplicate: bool):
        data = {
            "name": name,
            "recycle_criteria": recycle_criteria,
            "recycle_value": recycle_value,
            "recycle_action": recycle_action,
            "location": location,
            "name_template": name_template,
            "deduplicate": deduplicate
        }
        response = self.connection.patch(f"target/{id}", data=data)
        check_success(response)

    def delete_target(self, id: str, delete_files: bool):
        data = {
            "delete_files": delete_files
        }
        response = self.connection.delete(f"target/{id}", data=data)
        check_success(response)

    def delete_target_backups(self, id: str, delete_files: bool):
        data = {
            "delete_files": delete_files
        }
        response = self.connection.delete(f"target/{id}/all", data=data)
        check_success(response)

    def delete_backup(self, id: str, delete_files: bool):
        data = {
            "delete_files": delete_files
        }
        response = self.connection.delete(f"backup/{id}", data=data)
        check_success(response)

    def recycle_backup(self, id: str, is_recycled: bool):
        data = {
            "is_recycled": is_recycled
        }
        response = self.connection.patch(f"backup/{id}", data=data)
        check_success(response)

    def list_recycled_backups(self) -> list[Backup]:
        response = self.connection.get("recycle_bin")
        resp_json = check_success(response)
        return [Backup.from_dict(backup) for backup in resp_json["backups"]]

    def clear_recycle_bin(self, delete_files: bool):
        data = {
            "delete_files": delete_files
        }
        response = self.connection.delete("recycle_bin", data=data)
        check_success(response)
