# CSCI-635
This project contains all artifacts (wiht the exception of trajectories) gerneated as part  a replication study of [Live-SWE-Agent: Can Software engineering Agent self evolove on the Fly](). The contents of this repo are broken down as follows:

- custom_configs - contains the custom configuration we created to replicate the ablation study and to enable prompt evolution for the enhancment.

- live-swe-agent - contains the orignal source code and artifacts for live-swe-agent.

- mini-swe-agent-v1 - contains the source code for mini-swe-bench which we have modified in a few places to anble prompt evolution.

- results - contains all results and related data (with the except of the trajectories) for all experiemnts conducted during this study.

- scripts - contains serveral helpful python and shell script we created to automate some of the process for running the experiments. 

- subsets - contains csv files for that list the instance names of the a paticular subset of problems from swe-bench-verified that you wish to use to test the agent.

## Replication Steps

## Running Live-SWE-agent on SWE-bench

## Evaluating the SWE-bench Predictions

## Additional Documentation
This project spans multiple different existing repo including mini-swe-agent, live-swe-agent, and swe-bench. Below is a summary of links to documentation we found useful in replicate this work.

- [Live-SWE-agent Repo](https://github.com/OpenAutoCoder/live-swe-agent) - This link is for the Live-swe-agent repo which contains documentation on how to run live-swe-agent.

- [Mini-SWE-agent Documentation](https://mini-swe-agent.com/v1/usage/swebench/) - This link contains detailed info on workign mini-swe-agent v1 and v2.

- [Mini-SWE-agent Repo](https://github.com/SWE-agent/mini-swe-agent) - This link is for the mini-swe-agent repo which contains documentation on how to run live-swe-agent.

- [SWE-bench Documentation](https://www.swebench.com/SWE-bench/) - This link is for the SWE-bench site whihc contains documation fo rswe-bench as wellsas leaderboard stats.

- [SWE-bench](https://github.com/SWE-bench/SWE-bench) - This is the link to the SWE-bench repo which continas the testing harness to evaluate the predictions madew by the agent. 