session_name=test-session-6-normal
date
anyscale up --config=../yamls/minimal-ray-static.yaml --cloud-name=anyscale_default_cloud $session_name
date
anyscale exec -n $session_name 'python tuning/mnist.py"'