session_name=test-session-snapshot
date
anyscale up --config=minimal.yaml --cloud-name=anyscale_default_cloud $session_name
date
for i in {1..2}; do anyscale exec -n $session_name 'echo "hello" >> something.txt'; sleep 3; done
date
anyscale down $session_name
date
echo "Starting ..."
anyscale up --cloud-name=anyscale_default_cloud $session_name
date
anyscale exec -n $session_name 'cat something.txt'
date
anyscale down --terminate $session_name