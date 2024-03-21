# Basic usage

## Configuration file


A basic usage of the Ranch require a configuration file (eg: `ranch.conf`).
Here is a basic one, check `ranch.connection.` for details.

```bash
[client]
token=token
```

### Python Script


And here is a little sample to start a task running your `myscript.py` Python script.

```python
import os  
from ranch import connection
from ranch import ranchecker

RANCH_API_KEY = os.getenv("RANCH_API_KEY")
Username = os.environ.get("g_licenseUsername")
Password = os.environ.get("g_licensePassword")
scene = "C:\\Users\\mohbakh\\Pictures\\car\\sdk.c4d"
c4d_commandline = "C:\\Maxon\\C4D2023\\Commandline.exe"

conn = connection.Connect(RANCH_API_KEY)
ranch_rc = ranchecker.Ranchecker()
vuc = ranch_rc.create_archive(software_commandline=c4d_commandline, g_licenseUsername=Username, g_licensePassword=Password, scene_destination=scene)
conn.submit(archive_path=vuc, job_name="sdk", renderer_id=598, priority_id=13)
```