import ray

ray.init()
print(ray.available_resources())
print(ray.cluster_resources())