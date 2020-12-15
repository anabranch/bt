import time
import ray
ray.init(ignore_reinit_error=True)

@ray.remote(resources={'num_cpus': 4})
def func():
    time.sleep(10)
    print("resultz: Scaling!")

r = ray.get([func.remote() for i in range(100000)])

