echo date
anyscale up --config=minimal_no_gpu.yaml --disable-sync test-session
echo date
for i in {1..20}; do anyscale exec -n test-session 'python -c "import ray; ray.init();print(ray.available_resources())" \n'; date ; sleep 30; done
echo date
anyscale down --terminate test-session
echo date