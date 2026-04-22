# CSCI-635
This project contains all artifacts (wiht the exception of trajectories) gerneated as part  a replication study of [Live-SWE-Agent: Can Software engineering Agent self evolove on the Fly](). The contents of this repo are broken down as follows:

- custom_configs - contains the custom configuration we created to replicate the ablation study and to enable prompt evolution for the enhancment.

- live-swe-agent - contains the orignal source code and artifacts for live-swe-agent.

- mini-swe-agent-v1 - contains the source code for mini-swe-bench which we have modified in a few places to anble prompt evolution.

- results - contains all results and related data (with the except of the trajectories) for all experiemnts conducted during this study.

- scripts - contains serveral helpful python and shell script we created to automate some of the process for running the experiments. 

- subsets - contains csv files for that list the instance names of the a paticular subset of problems from swe-bench-verified that you wish to use to test the agent.

## Usage