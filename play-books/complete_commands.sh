#!/bin/bash

# Echo message and wait for input to continue
echo "Running prereq.yml playbook. Press Enter to continue."
read
# Run ansible playbook to download audit tool
ansible-playbook prereq.yml

# Echo message and wait for input to continue
echo "Running run_test.yml playbook. Press Enter to continue."
read

# Run ansible playbook to run run_test.yml
ansible-playbook run_test.yml
