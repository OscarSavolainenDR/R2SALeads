#!/bin/bash

<<<<<<< HEAD
# Number of times to run the command
num_iterations=50

for ((i = 1; i <= num_iterations; i++)); do

    # Check if the file exists before removing it
    if [ -e backend_v3/.env ]; then
        rm backend_v3/.env
    fi
    git add .
    git commit --amend --no-edit
    git rebase --continue

    # Wait for some time (you can adjust the sleep duration as needed)
    sleep 2
done
=======
# Your command goes here
your_command="rm To_dos.txt; find . -type f -name '__pycache__' -delete; git add . ; git commit --amend --no-edit ; git rebase --continue"

# Number of times to run the command
num_iterations=50

# Loop to run the command 100 times
for ((i = 1; i <= num_iterations; i++)); do
    # Run the command
    $your_command

    # Wait for some time (you can adjust the sleep duration as needed)
    sleep 2
done
>>>>>>> 4251e54 (Trying a celery/redis combo to do asycn tasks, in this case send confirmaiton email)
