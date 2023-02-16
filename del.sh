#!/bin/bash

# Number of times to run the command
num_iterations=10

for ((i = 1; i <= num_iterations; i++)); do
    # Check if the file exists before removing it
    if [ -e .env ]; then
        rm .env
    fi

    git add .
    git commit --amend --no-edit
    git rebase --continue

    # Wait for some time (you can adjust the sleep duration as needed)
    sleep 1
done
