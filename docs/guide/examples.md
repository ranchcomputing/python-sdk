# Examples

### - Submit project with 3ds max

Here is a little simple script with python submit a job to the ranchcomputing render farm with 3ds max and Corona renderer 

```python
import os
from ranch.connection import Connect

RANCH_API_KEY = os.getenv("RANCH_API_KEY")

conn = Connect(RANCH_API_KEY)

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
