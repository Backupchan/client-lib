# Backup-chan client library

This is the Python library for interfacing with a Backup-chan server.

## Installing

```bash
pip install .
```

For instructions on setting up the server, refer to Backup-chan server's README.

## Testing

```
pytest
```

## Example 

```python
from backupchan import *

api = API("http://192.168.1.43", 5000, "your api key")

targets = api.list_targets()
for target in targets:
    print(target)

target_id = api.new_target(
    "the waifu collection",
    BackupType.MULTI,
    BackupRecycleCriteria.AGE,
    10,
    BackupRecycleAction.RECYCLE,
    "/var/backups/waifu",
    "wf-$I_$D"
)
target = api.get_target(target_id)
print(f"Created new target: {target}")
```
