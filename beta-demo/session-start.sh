session_name=test-session-2
date
anyscale up --config=minimal.yaml --cloud-name=anyscale_default_cloud $session_name
date
for i in {1..10}; do anyscale exec -n $session_name 'python -c "import ray; ray.init();print(ray.available_resources())" \n'; date ; sleep 30; done
date
anyscale down --terminate $session_name
date