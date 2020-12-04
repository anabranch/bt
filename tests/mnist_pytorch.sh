session_name=pytorch-$(echo $RANDOM)
date
echo $session_name
anyscale up --config=yamls/tune_test.yaml --cloud-name=anyscale_default_cloud $session_name
date
anyscale exec -n $session_name 'python mnist_pytorch.py --use-gpu'
date
for i in {1..10}; do ; date ; sleep 30; done
date
anyscale down --terminate $session_name
date