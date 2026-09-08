from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass
@dataclass
class Job: job_id:str; future:Future; description:str
class JobScheduler:
    def __init__(self,max_workers=4): self.pool=ThreadPoolExecutor(max_workers=max_workers); self.jobs={}
    def submit(self,job_id,fn,*args,description=""): 
        f=self.pool.submit(fn,*args); self.jobs[job_id]=Job(job_id,f,description); return self.jobs[job_id]
    def cancel(self,job_id): return self.jobs[job_id].future.cancel() if job_id in self.jobs else False
    def shutdown(self): self.pool.shutdown(wait=True,cancel_futures=True)
