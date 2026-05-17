# scikit-learn__scikit-learn-13779

**Exit status:** `Submitted`

## Model stats

- **Instance cost:** `0.010466650000000001`
- **API calls:** `12`

<details>
<summary><strong>Step 1</strong></summary>

## Prompt sent to LLM

````text
[user]
<pr_description>
Consider the following PR description:
Voting estimator will fail at fit if weights are passed and an estimator is None
Because we don't check for an estimator to be `None` in `sample_weight` support, `fit` is failing`.

```python
    X, y = load_iris(return_X_y=True)
    voter = VotingClassifier(
        estimators=[('lr', LogisticRegression()),
                    ('rf', RandomForestClassifier())]
    )
    voter.fit(X, y, sample_weight=np.ones(y.shape))
    voter.set_params(lr=None)
    voter.fit(X, y, sample_weight=np.ones(y.shape))
```

```
AttributeError: 'NoneType' object has no attribute 'fit'
```

</pr_description>

<instructions>
# Task Instructions

## Overview
You're a software engineer interacting continuously with a computer by submitting commands.
You'll be helping implement necessary changes to meet requirements in the PR description.
Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase.

IMPORTANT: This is an interactive process where you will think and issue ONE command, see its result, then think and issue your next command.

For each response:
1. Include a THOUGHT section explaining your reasoning and what you're trying to accomplish
2. Provide exactly ONE bash command to execute

## Important Boundaries
- MODIFY: Regular source code files in /testbed (this is the working directory for all your subsequent commands)
- DO NOT MODIFY: Tests, configuration files (pyproject.toml, setup.cfg, etc.)

## Recommended Workflow
1. Analyze the codebase by finding and reading relevant files
2. Create a script to reproduce the issue
3. Edit the source code to resolve the issue
4. Verify your fix works by running your script again
5. Test edge cases to ensure your fix is robust

## Command Execution Rules
You are operating in an environment where
1. You write a single command
2. The system executes that command in a subshell
3. You see the result
4. You write your next command

Each response should include:
1. A **THOUGHT** section where you explain your reasoning and plan
2. A single bash code block with your command

Format your responses like this:

<format_example>
THOUGHT: Here I explain my reasoning process, analysis of the current situation,
and what I'm trying to accomplish with the command below.

```bash
your_command_here
```
</format_example>

Commands must be specified in a single bash code block:

```bash
your_command_here
```

**CRITICAL REQUIREMENTS:**
- Your response SHOULD include a THOUGHT section explaining your reasoning
- Your response MUST include EXACTLY ONE bash code block
- This bash block MUST contain EXACTLY ONE command (or a set of commands connected with && or ||)
- If you include zero or multiple bash blocks, or no command at all, YOUR RESPONSE WILL FAIL
- Do NOT try to run multiple independent commands in separate blocks in one response
- Directory or environment variable changes are not persistent. Every action is executed in a new subshell.
- However, you can prefix any action with `MY_ENV_VAR=MY_VALUE cd /path/to/working/dir && ...` or write/load environment variables from files

Example of a CORRECT response:
<example_response>
THOUGHT: I need to understand the structure of the repository first. Let me check what files are in the current directory to get a better understanding of the codebase.

```bash
ls -la
```
</example_response>

Example of an INCORRECT response:
<example_response>
THOUGHT: I need to examine the codebase and then look at a specific file. I'll run multiple commands to do this.

```bash
ls -la
```

Now I'll read the file:

```bash
cat file.txt
```
</example_response>

If you need to run multiple commands, either:
1. Combine them in one block using && or ||
```bash
command1 && command2 || echo "Error occurred"
```

2. Wait for the first command to complete, see its output, then issue the next command in your following response.

## Environment Details
- You have a full Linux shell environment
- Always use non-interactive flags (-y, -f) for commands
- Avoid interactive tools like vi, nano, or any that require user input
- If a command isn't available, you can install it

## Useful Command Examples

### Create a new file:
```bash
cat <<'EOF' > newfile.py
import numpy as np
hello = "world"
print(hello)
EOF
```

### Edit files with sed:
```bash
# Replace all occurrences
sed -i 's/old_string/new_string/g' filename.py

# Replace only first occurrence
sed -i 's/old_string/new_string/' filename.py

# Replace first occurrence on line 1
sed -i '1s/old_string/new_string/' filename.py

# Replace all occurrences in lines 1-10
sed -i '1,10s/old_string/new_string/g' filename.py
```

### View file content:
```bash
# View specific lines with numbers
nl -ba filename.py | sed -n '10,20p'
```

### Any other command you want to run
```bash
anything
```

## Submission
When you've completed your work (reading, editing, testing), and cannot make further progress
issue exactly the following command:

```bash
echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && git add -A && git diff --cached
```

This command will submit your work.
You cannot continue working (reading, editing, testing) in any way on this task after submitting.
</instructions>
````

## LLM response

````text
THOUGHT: I will start by creating a reproduction script to confirm the issue.

```bash
cat <<'EOF' > reproduce_issue.py
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)
voter = VotingClassifier(
    estimators=[('lr', LogisticRegression()),
                ('rf', RandomForestClassifier())]
)
voter.fit(X, y, sample_weight=np.ones(y.shape))
print("First fit successful")
voter.set_params(lr=None)
try:
    voter.fit(X, y, sample_weight=np.ones(y.shape))
    print("Second fit successful")
except Exception as e:
    print(f"Second fit failed with error: {e}")
    import traceback
    traceback.print_exc()
EOF
```
````

</details>

<details>
<summary><strong>Step 2</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
</output>
```

## LLM response

````text
```bash
python reproduce_issue.py
```
````

</details>

<details>
<summary><strong>Step 3</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
/testbed/sklearn/linear_model/logistic.py:432: FutureWarning: Default solver will be changed to 'lbfgs' in 0.22. Specify a solver to silence this warning.
  FutureWarning)
/testbed/sklearn/linear_model/logistic.py:469: FutureWarning: Default multi_class will be changed to 'auto' in 0.22. Specify the multi_class option to silence this warning.
  "this warning.", FutureWarning)
/testbed/sklearn/ensemble/forest.py:245: FutureWarning: The default value of n_estimators will change from 10 in version 0.20 to 100 in 0.22.
  "10 in version 0.20 to 100 in 0.22.", FutureWarning)
Traceback (most recent call last):
  File "reproduce_issue.py", line 16, in <module>
    voter.fit(X, y, sample_weight=np.ones(y.shape))
  File "/testbed/sklearn/ensemble/voting.py", line 273, in fit
    return super().fit(X, transformed_y, sample_weight)
  File "/testbed/sklearn/ensemble/voting.py", line 81, in fit
    if not has_fit_parameter(step, 'sample_weight'):
  File "/testbed/sklearn/utils/validation.py", line 808, in has_fit_parameter
    return parameter in signature(estimator.fit).parameters
AttributeError: 'NoneType' object has no attribute 'fit'
First fit successful
Second fit failed with error: 'NoneType' object has no attribute 'fit'
</output>
```

## LLM response

````text
```bash
grep -n "has_fit_parameter" /testbed/sklearn/ensemble/voting.py
```
````

</details>

<details>
<summary><strong>Step 4</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
25:from ..utils.validation import has_fit_parameter, check_is_fitted
81:                if not has_fit_parameter(step, 'sample_weight'):
</output>
```

## LLM response

````text
```bash
nl -ba /testbed/sklearn/ensemble/voting.py | sed -n '70,100p'
```
````

</details>

<details>
<summary><strong>Step 5</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
    70	                                 ' should be a list of (string, estimator)'
    71	                                 ' tuples')
    72	
    73	        if (self.weights is not None and
    74	                len(self.weights) != len(self.estimators)):
    75	            raise ValueError('Number of `estimators` and weights must be equal'
    76	                             '; got %d weights, %d estimators'
    77	                             % (len(self.weights), len(self.estimators)))
    78	
    79	        if sample_weight is not None:
    80	            for name, step in self.estimators:
    81	                if not has_fit_parameter(step, 'sample_weight'):
    82	                    raise ValueError('Underlying estimator \'%s\' does not'
    83	                                     ' support sample weights.' % name)
    84	
    85	        names, clfs = zip(*self.estimators)
    86	        self._validate_names(names)
    87	
    88	        n_isnone = np.sum([clf is None for _, clf in self.estimators])
    89	        if n_isnone == len(self.estimators):
    90	            raise ValueError('All estimators are None. At least one is '
    91	                             'required!')
    92	
    93	        self.estimators_ = Parallel(n_jobs=self.n_jobs)(
    94	                delayed(_parallel_fit_estimator)(clone(clf), X, y,
    95	                                                 sample_weight=sample_weight)
    96	                for clf in clfs if clf is not None)
    97	
    98	        self.named_estimators_ = Bunch()
    99	        for k, e in zip(self.estimators, self.estimators_):
   100	            self.named_estimators_[k[0]] = e
</output>
```

## LLM response

````text
```bash
grep -n "class VotingRegressor" /testbed/sklearn/ensemble/voting.py
```
````

</details>

<details>
<summary><strong>Step 6</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
368:class VotingRegressor(_BaseVoting, RegressorMixin):
</output>
```

## LLM response

````text
```bash
nl -ba /testbed/sklearn/ensemble/voting.py | sed -n '368,450p'
```
````

</details>

<details>
<summary><strong>Step 7</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
   368	class VotingRegressor(_BaseVoting, RegressorMixin):
   369	    """Prediction voting regressor for unfitted estimators.
   370	
   371	    .. versionadded:: 0.21
   372	
   373	    A voting regressor is an ensemble meta-estimator that fits base
   374	    regressors each on the whole dataset. It, then, averages the individual
   375	    predictions to form a final prediction.
   376	
   377	    Read more in the :ref:`User Guide <voting_regressor>`.
   378	
   379	    Parameters
   380	    ----------
   381	    estimators : list of (string, estimator) tuples
   382	        Invoking the ``fit`` method on the ``VotingRegressor`` will fit
   383	        clones of those original estimators that will be stored in the class
   384	        attribute ``self.estimators_``. An estimator can be set to `None`
   385	        using ``set_params``.
   386	
   387	    weights : array-like, shape (n_regressors,), optional (default=`None`)
   388	        Sequence of weights (`float` or `int`) to weight the occurrences of
   389	        predicted values before averaging. Uses uniform weights if `None`.
   390	
   391	    n_jobs : int or None, optional (default=None)
   392	        The number of jobs to run in parallel for ``fit``.
   393	        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
   394	        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
   395	        for more details.
   396	
   397	    Attributes
   398	    ----------
   399	    estimators_ : list of regressors
   400	        The collection of fitted sub-estimators as defined in ``estimators``
   401	        that are not `None`.
   402	
   403	    named_estimators_ : Bunch object, a dictionary with attribute access
   404	        Attribute to access any fitted sub-estimators by name.
   405	
   406	    Examples
   407	    --------
   408	    >>> import numpy as np
   409	    >>> from sklearn.linear_model import LinearRegression
   410	    >>> from sklearn.ensemble import RandomForestRegressor
   411	    >>> from sklearn.ensemble import VotingRegressor
   412	    >>> r1 = LinearRegression()
   413	    >>> r2 = RandomForestRegressor(n_estimators=10, random_state=1)
   414	    >>> X = np.array([[1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36]])
   415	    >>> y = np.array([2, 6, 12, 20, 30, 42])
   416	    >>> er = VotingRegressor([('lr', r1), ('rf', r2)])
   417	    >>> print(er.fit(X, y).predict(X))
   418	    [ 3.3  5.7 11.8 19.7 28.  40.3]
   419	
   420	    See also
   421	    --------
   422	    VotingClassifier: Soft Voting/Majority Rule classifier.
   423	    """
   424	
   425	    def __init__(self, estimators, weights=None, n_jobs=None):
   426	        self.estimators = estimators
   427	        self.weights = weights
   428	        self.n_jobs = n_jobs
   429	
   430	    def fit(self, X, y, sample_weight=None):
   431	        """ Fit the estimators.
   432	
   433	        Parameters
   434	        ----------
   435	        X : {array-like, sparse matrix}, shape (n_samples, n_features)
   436	            Training vectors, where n_samples is the number of samples and
   437	            n_features is the number of features.
   438	
   439	        y : array-like, shape (n_samples,)
   440	            Target values.
   441	
   442	        sample_weight : array-like, shape (n_samples,) or None
   443	            Sample weights. If None, then samples are equally weighted.
   444	            Note that this is supported only if all underlying estimators
   445	            support sample weights.
   446	
   447	        Returns
   448	        -------
   449	        self : object
   450	        """
</output>
```

## LLM response

````text
```bash
nl -ba /testbed/sklearn/ensemble/voting.py | sed -n '451,455p'
```
````

</details>

<details>
<summary><strong>Step 8</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
   451	        return super().fit(X, y, sample_weight)
   452	
   453	    def predict(self, X):
   454	        """Predict regression target for X.
   455	
</output>
```

## LLM response

````text
```bash
sed -i '80,81s/for name, step in self.estimators:/for name, step in self.estimators:\n                if step is None:\n                    continue/' /testbed/sklearn/ensemble/voting.py
```
````

</details>

<details>
<summary><strong>Step 9</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
</output>
```

## LLM response

````text
```bash
nl -ba /testbed/sklearn/ensemble/voting.py | sed -n '75,90p'
```
````

</details>

<details>
<summary><strong>Step 10</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
    75	            raise ValueError('Number of `estimators` and weights must be equal'
    76	                             '; got %d weights, %d estimators'
    77	                             % (len(self.weights), len(self.estimators)))
    78	
    79	        if sample_weight is not None:
    80	            for name, step in self.estimators:
    81	                if step is None:
    82	                    continue
    83	                if not has_fit_parameter(step, 'sample_weight'):
    84	                    raise ValueError('Underlying estimator \'%s\' does not'
    85	                                     ' support sample weights.' % name)
    86	
    87	        names, clfs = zip(*self.estimators)
    88	        self._validate_names(names)
    89	
    90	        n_isnone = np.sum([clf is None for _, clf in self.estimators])
</output>
```

## LLM response

````text
```bash
python reproduce_issue.py
```
````

</details>

<details>
<summary><strong>Step 11</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
/testbed/sklearn/linear_model/logistic.py:432: FutureWarning: Default solver will be changed to 'lbfgs' in 0.22. Specify a solver to silence this warning.
  FutureWarning)
/testbed/sklearn/linear_model/logistic.py:469: FutureWarning: Default multi_class will be changed to 'auto' in 0.22. Specify the multi_class option to silence this warning.
  "this warning.", FutureWarning)
/testbed/sklearn/ensemble/forest.py:245: FutureWarning: The default value of n_estimators will change from 10 in version 0.20 to 100 in 0.22.
  "10 in version 0.20 to 100 in 0.22.", FutureWarning)
/testbed/sklearn/ensemble/forest.py:245: FutureWarning: The default value of n_estimators will change from 10 in version 0.20 to 100 in 0.22.
  "10 in version 0.20 to 100 in 0.22.", FutureWarning)
First fit successful
Second fit successful
</output>
```

## LLM response

````text
```bash
cat <<'EOF' > test_voting_regressor.py
import numpy as np
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

X = np.array([[1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36]])
y = np.array([2, 6, 12, 20, 30, 42])
er = VotingRegressor([('lr', LinearRegression()), ('rf', RandomForestRegressor(n_estimators=10))])
er.fit(X, y, sample_weight=np.ones(y.shape))
print("First fit successful")
er.set_params(lr=None)
try:
    er.fit(X, y, sample_weight=np.ones(y.shape))
    print("Second fit successful")
except Exception as e:
    print(f"Second fit failed with error: {e}")
    import traceback
    traceback.print_exc()
EOF
python test_voting_regressor.py && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && git add -A && git diff --cached
```
````

</details>

<details>
<summary><strong>Step 12</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>0</returncode>
<output>
First fit successful
Second fit successful
COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT
diff --git a/reproduce_issue.py b/reproduce_issue.py
new file mode 100644
index 000000000..89e0d963e
--- /dev/null
+++ b/reproduce_issue.py
@@ -0,0 +1,21 @@
+import numpy as np
+from sklearn.datasets import load_iris
+from sklearn.ensemble import VotingClassifier
+from sklearn.linear_model import LogisticRegression
+from sklearn.ensemble import RandomForestClassifier
+
+X, y = load_iris(return_X_y=True)
+voter = VotingClassifier(
+    estimators=[('lr', LogisticRegression()),
+                ('rf', RandomForestClassifier())]
+)
+voter.fit(X, y, sample_weight=np.ones(y.shape))
+print("First fit successful")
+voter.set_params(lr=None)
+try:
+    voter.fit(X, y, sample_weight=np.ones(y.shape))
+    print("Second fit successful")
+except Exception as e:
+    print(f"Second fit failed with error: {e}")
+    import traceback
+    traceback.print_exc()
diff --git a/sklearn/ensemble/voting.py b/sklearn/ensemble/voting.py
index 7afa7180c..d8e14b152 100644
--- a/sklearn/ensemble/voting.py
+++ b/sklearn/ensemble/voting.py
@@ -78,6 +78,8 @@ class _BaseVoting(_BaseComposition, TransformerMixin):
 
         if sample_weight is not None:
             for name, step in self.estimators:
+                if step is None:
+                    continue
                 if not has_fit_parameter(step, 'sample_weight'):
                     raise ValueError('Underlying estimator \'%s\' does not'
                                      ' support sample weights.' % name)
diff --git a/test_voting_regressor.py b/test_voting_regressor.py
new file mode 100644
index 000000000..8e4f0d5cd
--- /dev/null
+++ b/test_voting_regressor.py
@@ -0,0 +1,18 @@
+import numpy as np
+from sklearn.ensemble import VotingRegressor
+from sklearn.linear_model import LinearRegression
+from sklearn.ensemble import RandomForestRegressor
+
+X = np.array([[1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36]])
+y = np.array([2, 6, 12, 20, 30, 42])
+er = VotingRegressor([('lr', LinearRegression()), ('rf', RandomForestRegressor(n_estimators=10))])
+er.fit(X, y, sample_weight=np.ones(y.shape))
+print("First fit successful")
+er.set_params(lr=None)
+try:
+    er.fit(X, y, sample_weight=np.ones(y.shape))
+    print("Second fit successful")
+except Exception as e:
+    print(f"Second fit failed with error: {e}")
+    import traceback
+    traceback.print_exc()
</output>
```

## LLM response

````text
```bash
rm reproduce_issue.py test_voting_regressor.py && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && git add -A && git diff --cached
```
````

</details>
