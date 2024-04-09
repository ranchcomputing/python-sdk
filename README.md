# Ranch python SDK
This Python-based API SDK Designed with future production in mind, its goal is to unify the development of the Ranchecker application and facilitate external customers in integrating their pipelines with our render farm. This SDK stands as a bridge between external pipelines and our rendering services, potentially opening new avenues for collaboration and efficiency in rendering workflows.

## Example python script

### - Submit project with 3ds max

Here is a little simple script with python submit a job to the ranchcomputing render farm with 3ds max and Corona renderer 

```python
import os
from ranch.connection import Connect
from ranch import ranchecker

RANCH_API_KEY = os.getenv("RANCH_API_KEY")

conn = Connect(RANCH_API_KEY)
ranch_rc = ranchecker.Ranchecker()

job = conn.create_job(
            archive_path="C:\\Users\\sdk_job.vu3",
            job_name="sdk_job",
            priority="cpu-low",
            software="3dsmax",
            software_version="2023",
            renderer_name="Corona",
        )
res = conn.submit(job)
```

### - Submit project with cinema 4d

Here is a little simple script with python submit a job to the ranchcomputing render farm with cinema 4d R23 and Arnold renderer 

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
job = conn.create_job(
            archive_path=vuc_archive_path,
            job_name="sdk_job",
            priority="cpu-low",
            software="cinema4d",
            software_version="R23",
            renderer_name="Arnold",
        )
res = conn.submit(job)

```

