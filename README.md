# CSCI-635
This project contains all artifacts (with the exception of trajectories) generated as part of the replication study for [Live-SWE-Agent: Can Software engineering Agent self-evolve on the Fly?](https://arxiv.org/abs/2511.13646). The contents of this repo are broken down as follows:

- custom_configs - Contains the custom configuration files we created to replicate the ablation study and to enable prompt evolution for the enhancement.

- live-swe-agent - Contains the original source code and artifacts for live-swe-agent.

- mini-swe-agent-v1 - Contains the source code for the original mini-swe-agent v1 implementation which we have modified in a few places to enable prompt evolution.

- results - Contains all results and related data (with the except of the trajectories) for all experiments conducted during this study.

- scripts - Contains several helpful python and shell script we created to automate some of the process for running the experiments. 

- subsets - Contains csv files that list the instance names for the particular subset of problems from SWE-bench-verified we used in our experiments.

## Running Live-SWE-agent on SWE-bench
TODO: outline the steps to run our evals using the scripts

## Evaluating the SWE-bench Predictions
TODO: Outline the steps to evaluate the results 

## Additional Documentation
This project spans multiple different existing repo including mini-swe-agent, live-swe-agent, and swe-bench. Below is a summary of all documentation links we found useful in replicating this work.

- [Live-SWE-agent Repo](https://github.com/OpenAutoCoder/live-swe-agent) - This link is for the live-swe-agent repo which contains documentation on how to run live-swe-agent.

- [Mini-SWE-agent Documentation](https://mini-swe-agent.com/v1/usage/swebench/) - This link contains detailed info on working with mini-swe-agent v1 and v2.

- [Mini-SWE-agent Repo](https://github.com/SWE-agent/mini-swe-agent) - This link is for the mini-swe-agent repo which contains documentation on how to run mini-swe-agent.

- [SWE-bench Documentation](https://www.swebench.com/SWE-bench/) - This link is for the SWE-bench site which contains documentation for SWE-bench as well as leaderboard stats.

- [SWE-bench](https://github.com/SWE-bench/SWE-bench) - This is the link to the SWE-bench repo which contains the testing harness to evaluate the predictions made by the agent. 