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
```
