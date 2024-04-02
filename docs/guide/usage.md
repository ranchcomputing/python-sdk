# Basic usage

## Configuration file


A basic usage of the Ranch require a configuration file (eg: `ranch.conf`).
Here is a basic one, check `ranch.connection.` for details.

```bash
[client]
token=token
```

### Python Script


And here is a little sample Python script to start a job in ranch rander farm.

```python
import os
from ranch.connection import Connect
from ranch import ranchecker

RANCH_API_KEY = os.getenv("RANCH_API_KEY")
Username = os.environ.get("g_licenseUsername")
Password = os.environ.get("g_licensePassword")
# Replace the scene variable with the destination of your scene.
scene = "C:\\Users\\username\\jobs\\cinema4d\\sdk.c4d"
c4d_commandline = "C:\\Maxon\\C4D2023\\Commandline.exe"

conn = Connect(RANCH_API_KEY)
ranch_rc = ranchecker.Ranchecker()
vuc_archive_path = ranch_rc.create_archive(software_commandline=c4d_commandline, 
            g_licenseUsername=Username, 
            g_licensePassword=Password, 
            scene_destination=scene)
job = self.conn.create_job(
            archive_path=vuc_archive_path,
            job_name="sdk_job",
            priority="cpu-low",
            software="cinema4d",
            software_version="R23",
            renderer_name="Arnold",
        )
res = self.conn.submit(job)
```