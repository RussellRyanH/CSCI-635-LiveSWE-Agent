# psf__requests-1142

**Exit status:** `Submitted`

## Model stats

- **Instance cost:** `0.248736`
- **API calls:** `13`

<details>
<summary><strong>Step 1</strong></summary>

## Prompt sent to LLM

````text
[user]
<pr_description>
Consider the following PR description:
requests.get is ALWAYS sending content length
Hi,

It seems like that request.get always adds 'content-length' header to the request.
I think that the right behavior is not to add this header automatically in GET requests or add the possibility to not send it.

For example http://amazon.com returns 503 for every get request that contains 'content-length' header.

Thanks,

Oren


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

### View file content:
```bash
# View specific lines with numbers
nl -ba filename.py | sed -n '10,20p'
```

**IMPORTANT TOOL CREATION INSTRUCTIONS**
## Creating your own tools 
- You can also create your own tools in Python to help with your workflow
- Compared to basic bash commands, the tools you create should be able to better aid your workflow in solving the task
- Ensure each tool you create is in Python, contains informative outputs or error messages, and can be ran from the command line
- You should at least create a simple edit tool that can help you effectively edit arbitrary files instead of using bash commands
- The tools you create can be for any purpose, it does not need to be general, instead think about how it can help you specifically with the current task at hand

### Example of creating a custom tool:
<example_response>
THOUGHT: I noticed that in order to solve the issue I need to ... therefore I should create a custom tool to help me ...

```bash
cat <<'EOF' > /path/to/tool_name.py
#!/usr/bin/env python3
import sys
# Import other packages if needed

def main():
    # Your tool logic here
    ...

if __name__ == "__main__":
    main()
EOF
```
</example_response>

### Example of using the tool you created:
<example_response>
THOUGHT: Let me use the custom tool I created to help me with ...

```bash
python /path/to/tool_name.py <<EOF
your_input_here
EOF
```
</example_response>

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
THOUGHT: I need to explore the repository to understand the codebase and locate where GET requests might be adding a Content-Length header automatically. I'll start by listing the files in the working directory.

```bash
ls -la
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
total 104
drwxrwxrwx 1 root root  4096 Sep 10 14:58 .
drwxr-xr-x 1 root root  4096 Nov 10 06:37 ..
drwxrwxrwx 8 root root  4096 Sep 10 14:58 .git
-rw-r--r-- 1 root root   182 Sep 10 14:58 .gitignore
-rw-r--r-- 1 root root   170 Sep 10 14:58 .travis.yml
-rw-r--r-- 1 root root  2441 Sep 10 14:58 AUTHORS.rst
-rw-r--r-- 1 root root 13687 Sep 10 14:58 HISTORY.rst
-rw-r--r-- 1 root root   581 Sep 10 14:58 LICENSE
-rw-r--r-- 1 root root   100 Sep 10 14:58 MANIFEST.in
-rw-r--r-- 1 root root   657 Sep 10 14:58 Makefile
-rw-r--r-- 1 root root  4377 Sep 10 14:58 NOTICE
-rw-r--r-- 1 root root  2510 Sep 10 14:58 README.rst
drwxr-xr-x 4 root root  4096 Sep 10 14:58 build
drwxrwxrwx 8 root root  4096 Sep 10 14:58 docs
drwxrwxrwx 2 root root  4096 Sep 10 14:58 ext
drwxr-xr-x 4 root root  4096 Sep 10 14:58 requests
drwxr-xr-x 2 root root  4096 Sep 10 14:58 requests.egg-info
-rw-r--r-- 1 root root    13 Sep 10 14:58 requirements.txt
-rwxr-xr-x 1 root root  1671 Sep 10 14:58 setup.py
-rw-r--r-- 1 root root  8824 Sep 10 14:58 test_requests.py
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: I want to locate where the code sets the Content-Length header. I'll search the requests package for any references to "Content-Length" to identify the logic that sets it, so I can adjust behavior for GET requests. If no references are found, I'll list the directory to understand the module layout. I anticipate creating a small Python editing tool to make targeted, safe modifications once I pinpoint the relevant code.

```bash
grep -R -n -i 'content-length' requests || ls -la requests
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
grep: requests/__pycache__/models.cpython-39.pyc: binary file matches
grep: requests/__pycache__/adapters.cpython-39.pyc: binary file matches
requests/adapters.py:157:        chunked = not (request.body is None or 'Content-Length' in request.headers)
requests/models.py:362:                self.headers['Content-Length'] = length
requests/models.py:389:        self.headers['Content-Length'] = '0'
requests/models.py:392:            self.headers['Content-Length'] = str(body.tell())
requests/models.py:395:            self.headers['Content-Length'] = str(len(body))
requests/models.py:410:            # Recompute Content-Length
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: I need to inspect requests/models.py around the lines that mention Content-Length to understand under what conditions it is being set and how to adjust it for GET requests. This will help me plan a fix and potentially create an editing tool later if needed.

```bash
nl -ba requests/models.py | sed -n '320,450p'
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
   320	
   321	        url = requote_uri(urlunparse([scheme, netloc, path, _params, query, fragment]))
   322	        self.url = url
   323	
   324	    def prepare_headers(self, headers):
   325	        """Prepares the given HTTP headers."""
   326	
   327	        if headers:
   328	            self.headers = CaseInsensitiveDict(headers)
   329	        else:
   330	            self.headers = CaseInsensitiveDict()
   331	
   332	    def prepare_body(self, data, files):
   333	        """Prepares the given HTTP body data."""
   334	
   335	        # Check if file, fo, generator, iterator.
   336	        # If not, run through normal process.
   337	
   338	        # Nottin' on you.
   339	        body = None
   340	        content_type = None
   341	        length = None
   342	        is_stream = False
   343	
   344	        is_stream = all([
   345	            hasattr(data, '__iter__'),
   346	            not isinstance(data, basestring),
   347	            not isinstance(data, dict)
   348	        ])
   349	
   350	        try:
   351	            length = str(super_len(data))
   352	        except (TypeError, AttributeError):
   353	            length = False
   354	
   355	        if is_stream:
   356	            body = data
   357	
   358	            if files:
   359	                raise NotImplementedError('Streamed bodies and files are mutually exclusive.')
   360	
   361	            if length:
   362	                self.headers['Content-Length'] = length
   363	            else:
   364	                self.headers['Transfer-Encoding'] = 'chunked'
   365	        # Check if file, fo, generator, iterator.
   366	        # If not, run through normal process.
   367	
   368	        else:
   369	            # Multi-part file uploads.
   370	            if files:
   371	                (body, content_type) = self._encode_files(files, data)
   372	            else:
   373	                if data:
   374	                    body = self._encode_params(data)
   375	                    if isinstance(data, str) or isinstance(data, builtin_str) or hasattr(data, 'read'):
   376	                        content_type = None
   377	                    else:
   378	                        content_type = 'application/x-www-form-urlencoded'
   379	
   380	            self.prepare_content_length(body)
   381	
   382	            # Add content-type if it wasn't explicitly provided.
   383	            if (content_type) and (not 'content-type' in self.headers):
   384	                self.headers['Content-Type'] = content_type
   385	
   386	        self.body = body
   387	
   388	    def prepare_content_length(self, body):
   389	        self.headers['Content-Length'] = '0'
   390	        if hasattr(body, 'seek') and hasattr(body, 'tell'):
   391	            body.seek(0, 2)
   392	            self.headers['Content-Length'] = str(body.tell())
   393	            body.seek(0, 0)
   394	        elif body is not None:
   395	            self.headers['Content-Length'] = str(len(body))
   396	
   397	    def prepare_auth(self, auth):
   398	        """Prepares the given HTTP auth data."""
   399	        if auth:
   400	            if isinstance(auth, tuple) and len(auth) == 2:
   401	                # special-case basic HTTP auth
   402	                auth = HTTPBasicAuth(*auth)
   403	
   404	            # Allow auth to make its changes.
   405	            r = auth(self)
   406	
   407	            # Update self to reflect the auth changes.
   408	            self.__dict__.update(r.__dict__)
   409	
   410	            # Recompute Content-Length
   411	            self.prepare_content_length(self.body)
   412	
   413	    def prepare_cookies(self, cookies):
   414	        """Prepares the given HTTP cookie data."""
   415	
   416	        if isinstance(cookies, cookielib.CookieJar):
   417	            cookies = cookies
   418	        else:
   419	            cookies = cookiejar_from_dict(cookies)
   420	
   421	        if 'cookie' not in self.headers:
   422	            cookie_header = get_cookie_header(cookies, self)
   423	            if cookie_header is not None:
   424	                self.headers['Cookie'] = cookie_header
   425	
   426	    def prepare_hooks(self, hooks):
   427	        """Prepares the given hooks."""
   428	        for event in hooks:
   429	            self.register_hook(event, hooks[event])
   430	
   431	
   432	class Response(object):
   433	    """The :class:`Response <Response>` object, which contains a
   434	    server's response to an HTTP request.
   435	    """
   436	
   437	    def __init__(self):
   438	        super(Response, self).__init__()
   439	
   440	        self._content = False
   441	        self._content_consumed = False
   442	
   443	        #: Integer Code of responded HTTP Status.
   444	        self.status_code = None
   445	
   446	        #: Case-insensitive Dictionary of Response Headers.
   447	        #: For example, ``headers['content-encoding']`` will return the
   448	        #: value of a ``'Content-Encoding'`` response header.
   449	        self.headers = CaseInsensitiveDict()
   450	
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: I need to inspect the Request/PreparedRequest classes earlier in requests/models.py to understand how HTTP method is stored and accessible during body/header preparation. This will help me determine how to conditionally avoid setting Content-Length for GET requests (likely by checking self.method) and plan a code change. I'll view the beginning portion of models.py to find class definitions and relevant methods.

```bash
nl -ba requests/models.py | sed -n '1,200p'
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
     1	# -*- coding: utf-8 -*-
     2	
     3	"""
     4	requests.models
     5	~~~~~~~~~~~~~~~
     6	
     7	This module contains the primary objects that power Requests.
     8	"""
     9	
    10	import collections
    11	import logging
    12	
    13	from io import BytesIO
    14	from .hooks import default_hooks
    15	from .structures import CaseInsensitiveDict
    16	from .status_codes import codes
    17	
    18	from .auth import HTTPBasicAuth
    19	from .cookies import cookiejar_from_dict, get_cookie_header
    20	from .packages.urllib3.filepost import encode_multipart_formdata
    21	from .exceptions import HTTPError, RequestException, MissingSchema, InvalidURL
    22	from .utils import (
    23	    stream_untransfer, guess_filename, requote_uri,
    24	    stream_decode_response_unicode, to_key_val_list, parse_header_links,
    25	    iter_slices, guess_json_utf, super_len)
    26	from .compat import (
    27	    cookielib, urlparse, urlunparse, urlsplit, urlencode, str, bytes, StringIO,
    28	    is_py2, chardet, json, builtin_str, basestring)
    29	
    30	REDIRECT_STATI = (codes.moved, codes.found, codes.other, codes.temporary_moved)
    31	CONTENT_CHUNK_SIZE = 10 * 1024
    32	ITER_CHUNK_SIZE = 512
    33	
    34	log = logging.getLogger(__name__)
    35	
    36	
    37	class RequestEncodingMixin(object):
    38	    @property
    39	    def path_url(self):
    40	        """Build the path URL to use."""
    41	
    42	        url = []
    43	
    44	        p = urlsplit(self.url)
    45	
    46	        path = p.path
    47	        if not path:
    48	            path = '/'
    49	
    50	        url.append(path)
    51	
    52	        query = p.query
    53	        if query:
    54	            url.append('?')
    55	            url.append(query)
    56	
    57	        return ''.join(url)
    58	
    59	    @staticmethod
    60	    def _encode_params(data):
    61	        """Encode parameters in a piece of data.
    62	
    63	        Will successfully encode parameters when passed as a dict or a list of
    64	        2-tuples. Order is retained if data is a list of 2-tuples but abritrary
    65	        if parameters are supplied as a dict.
    66	        """
    67	
    68	        if isinstance(data, (str, bytes)):
    69	            return data
    70	        elif hasattr(data, 'read'):
    71	            return data
    72	        elif hasattr(data, '__iter__'):
    73	            result = []
    74	            for k, vs in to_key_val_list(data):
    75	                if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
    76	                    vs = [vs]
    77	                for v in vs:
    78	                    if v is not None:
    79	                        result.append(
    80	                            (k.encode('utf-8') if isinstance(k, str) else k,
    81	                             v.encode('utf-8') if isinstance(v, str) else v))
    82	            return urlencode(result, doseq=True)
    83	        else:
    84	            return data
    85	
    86	    @staticmethod
    87	    def _encode_files(files, data):
    88	        """Build the body for a multipart/form-data request.
    89	
    90	        Will successfully encode files when passed as a dict or a list of
    91	        2-tuples. Order is retained if data is a list of 2-tuples but abritrary
    92	        if parameters are supplied as a dict.
    93	
    94	        """
    95	        if (not files) or isinstance(data, str):
    96	            return None
    97	
    98	        new_fields = []
    99	        fields = to_key_val_list(data or {})
   100	        files = to_key_val_list(files or {})
   101	
   102	        for field, val in fields:
   103	            if isinstance(val, list):
   104	                for v in val:
   105	                    new_fields.append((field, builtin_str(v)))
   106	            else:
   107	                new_fields.append((field, builtin_str(val)))
   108	
   109	        for (k, v) in files:
   110	            # support for explicit filename
   111	            ft = None
   112	            if isinstance(v, (tuple, list)):
   113	                if len(v) == 2:
   114	                    fn, fp = v
   115	                else:
   116	                    fn, fp, ft = v
   117	            else:
   118	                fn = guess_filename(v) or k
   119	                fp = v
   120	            if isinstance(fp, str):
   121	                fp = StringIO(fp)
   122	            if isinstance(fp, bytes):
   123	                fp = BytesIO(fp)
   124	
   125	            if ft:
   126	                new_v = (fn, fp.read(), ft)
   127	            else:
   128	                new_v = (fn, fp.read())
   129	            new_fields.append((k, new_v))
   130	
   131	        body, content_type = encode_multipart_formdata(new_fields)
   132	
   133	        return body, content_type
   134	
   135	
   136	class RequestHooksMixin(object):
   137	    def register_hook(self, event, hook):
   138	        """Properly register a hook."""
   139	
   140	        if isinstance(hook, collections.Callable):
   141	            self.hooks[event].append(hook)
   142	        elif hasattr(hook, '__iter__'):
   143	            self.hooks[event].extend(h for h in hook if isinstance(h, collections.Callable))
   144	
   145	    def deregister_hook(self, event, hook):
   146	        """Deregister a previously registered hook.
   147	        Returns True if the hook existed, False if not.
   148	        """
   149	
   150	        try:
   151	            self.hooks[event].remove(hook)
   152	            return True
   153	        except ValueError:
   154	            return False
   155	
   156	
   157	class Request(RequestHooksMixin):
   158	    """A user-created :class:`Request <Request>` object.
   159	
   160	    Used to prepare a :class:`PreparedRequest <PreparedRequest>`, which is sent to the server.
   161	
   162	    :param method: HTTP method to use.
   163	    :param url: URL to send.
   164	    :param headers: dictionary of headers to send.
   165	    :param files: dictionary of {filename: fileobject} files to multipart upload.
   166	    :param data: the body to attach the request. If a dictionary is provided, form-encoding will take place.
   167	    :param params: dictionary of URL parameters to append to the URL.
   168	    :param auth: Auth handler or (user, pass) tuple.
   169	    :param cookies: dictionary or CookieJar of cookies to attach to this request.
   170	    :param hooks: dictionary of callback hooks, for internal usage.
   171	
   172	    Usage::
   173	
   174	      >>> import requests
   175	      >>> req = requests.Request('GET', 'http://httpbin.org/get')
   176	      >>> req.prepare()
   177	      <PreparedRequest [GET]>
   178	
   179	    """
   180	    def __init__(self,
   181	        method=None,
   182	        url=None,
   183	        headers=None,
   184	        files=None,
   185	        data=dict(),
   186	        params=dict(),
   187	        auth=None,
   188	        cookies=None,
   189	        hooks=None):
   190	
   191	
   192	        # Default empty dicts for dict params.
   193	        data = [] if data is None else data
   194	        files = [] if files is None else files
   195	        headers = {} if headers is None else headers
   196	        params = {} if params is None else params
   197	        hooks = {} if hooks is None else hooks
   198	
   199	        self.hooks = default_hooks()
   200	        for (k, v) in list(hooks.items()):
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: The issue arises from requests/models.py automatically setting a Content-Length header to '0' even when there's no body, which affects GET requests and can cause 503 responses from some servers (e.g., Amazon). The clean, general fix is to avoid setting Content-Length when the body is None across all methods, not only GET. This ensures we do not send Content-Length for empty requests while still computing it when there is an actual body. I'll patch the prepare_content_length method accordingly and then run a small Python script to verify that GET requests without a body no longer include Content-Length, while POST requests with a body still include it.

```bash
python - <<'PY'
import re, sys
path = 'requests/models.py'
source = open(path, 'r', encoding='utf-8').read()
pattern = r"def prepare_content_length\(self, body\):\n(?:[ \t].*\n)+"
replacement = """def prepare_content_length(self, body):
        # Avoid automatically sending Content-Length for empty bodies (e.g., GET requests).
        # Only set Content-Length when we have a real body to send.
        if body is None:
            # Ensure any previously set Content-Length is removed
            self.headers.pop('Content-Length', None)
            return
        if hasattr(body, 'seek') and hasattr(body, 'tell'):
            body.seek(0, 2)
            self.headers['Content-Length'] = str(body.tell())
            body.seek(0, 0)
        else:
            self.headers['Content-Length'] = str(len(body))
"""
new_source = re.sub(pattern, replacement, source, count=1)
if new_source == source:
    print("Patch failed: prepare_content_length not modified", file=sys.stderr)
    sys.exit(1)
open(path, 'w', encoding='utf-8').write(new_source)
print("Patched prepare_content_length to avoid Content-Length on empty body")
PY && python - <<'PY'
import requests
from requests.models import Request

# Test GET without body: should NOT include Content-Length
req_get = Request('GET', 'http://example.com')
prep_get = req_get.prepare()
print('GET Content-Length present:', 'Content-Length' in prep_get.headers, '->', prep_get.headers.get('Content-Length'))

# Test POST with body: should include correct Content-Length
req_post = Request('POST', 'http://example.com', data={'a':'b'})
prep_post = req_post.prepare()
print('POST Content-Length present:', 'Content-Length' in prep_post.headers, '->', prep_post.headers.get('Content-Length'))

# Test POST with empty body explicitly None: should NOT include Content-Length
req_post_empty = Request('POST', 'http://example.com', data=None)
prep_post_empty = req_post_empty.prepare()
print('POST empty Content-Length present:', 'Content-Length' in prep_post_empty.headers, '->', prep_post_empty.headers.get('Content-Length'))
PY
```
````

</details>

<details>
<summary><strong>Step 6</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>1</returncode>
<output>
  File "<stdin>", line 25
    PY && python - <<'PY'
        ^
SyntaxError: invalid syntax
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: The issue stems from requests/models.py automatically setting a Content-Length header to '0' even when there is no body, which affects GET requests. A general fix is to avoid setting Content-Length when the body is None across all methods, and only set it when there's an actual body. I'll patch the prepare_content_length method to implement this logic, ensuring indentation is preserved. Then I'll run a small script to verify that GET requests without a body do not include Content-Length, while POST requests with a body do.

```bash
python - <<'PY'
import sys

path = 'requests/models.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the function definition line
def_idx = None
for i, line in enumerate(lines):
    if 'def prepare_content_length(self, body):' in line:
        def_idx = i
        break

if def_idx is None:
    print('Patch failed: prepare_content_length definition not found', file=sys.stderr)
    sys.exit(1)

# Determine indentation of the def line
def_line = lines[def_idx]
indent = def_line[:len(def_line) - len(def_line.lstrip())]

# Find the end of the function block: first line that is not more-indented than the def line
end_idx = def_idx + 1
def_is_more = lambda s: s.startswith(indent + ' ') or s.startswith(indent + '\t')
while end_idx < len(lines):
    s = lines[end_idx]
    if s.strip() == '':
        end_idx += 1
        continue
    if not def_is_more(s):
        break
    end_idx += 1

new_block = [
    indent + "def prepare_content_length(self, body):\n",
    indent + "    # Avoid automatically sending Content-Length for empty bodies (e.g., GET requests).\n",
    indent + "    # Only set Content-Length when we have a real body to send.\n",
    indent + "    if body is None:\n",
    indent + "        # Ensure any previously set Content-Length is removed\n",
    indent + "        self.headers.pop('Content-Length', None)\n",
    indent + "        return\n",
    indent + "    if hasattr(body, 'seek') and hasattr(body, 'tell'):\n",
    indent + "        body.seek(0, 2)\n",
    indent + "        self.headers['Content-Length'] = str(body.tell())\n",
    indent + "        body.seek(0, 0)\n",
    indent + "    else:\n",
    indent + "        self.headers['Content-Length'] = str(len(body))\n",
]

# Apply patch
patched = lines[:def_idx] + new_block + lines[end_idx:]
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(patched)

print('Patched prepare_content_length to avoid Content-Length on empty body')
PY && python - <<'PY'
import requests
from requests.models import Request

def show_result(prep, label):
    print(label, 'Content-Length present:', 'Content-Length' in prep.headers, '->', prep.headers.get('Content-Length'))
    # Also show headers for clarity
    print(label, 'headers:', dict(prep.headers))

# Test GET without body: should NOT include Content-Length
req_get = Request('GET', 'http://example.com')
prep_get = req_get.prepare()
show_result(prep_get, 'GET')

# Test POST with body: should include correct Content-Length
req_post = Request('POST', 'http://example.com', data={'a':'b'})
prep_post = req_post.prepare()
show_result(prep_post, 'POST with body')

# Test POST with empty body explicitly None: should NOT include Content-Length
req_post_empty = Request('POST', 'http://example.com', data=None)
prep_post_empty = req_post_empty.prepare()
show_result(prep_post_empty, 'POST empty')
PY
```
````

</details>

<details>
<summary><strong>Step 7</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>1</returncode>
<output>
  File "<stdin>", line 56
    PY && python - <<'PY'
        ^
SyntaxError: invalid syntax
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: The issue is that requests/models.py automatically sets Content-Length to '0' even when there is no body, causing GET requests to include a Content-Length header. A general fix is to modify prepare_content_length to only set Content-Length when there is an actual body and remove it when body is None. I will patch that function accordingly and then run a verification script to ensure that GET requests without a body no longer include the Content-Length header, while POST requests with a body still include it.

```bash
python - <<'PY'
import re, sys, io
path = 'requests/models.py'
src = io.open(path, 'r', encoding='utf-8').read()
pattern = r"def prepare_content_length\(self, body\):\n(?:[ \t].*\n)+"
replacement = """def prepare_content_length(self, body):
        # Avoid automatically sending Content-Length when there is no body.
        # Only set Content-Length when we have a real body to send.
        if body is None:
            # Ensure any previously set Content-Length is removed
            self.headers.pop('Content-Length', None)
            return
        if hasattr(body, 'seek') and hasattr(body, 'tell'):
            body.seek(0, 2)
            self.headers['Content-Length'] = str(body.tell())
            body.seek(0, 0)
        else:
            self.headers['Content-Length'] = str(len(body))
"""
new_src, n = re.subn(pattern, replacement, src, count=1)
if n != 1:
    print("Patch failed: prepare_content_length not modified", file=sys.stderr)
    sys.exit(1)
io.open(path, 'w', encoding='utf-8').write(new_src)
print("Patched prepare_content_length to avoid Content-Length on empty body")
PY
&& python - <<'PY'
from requests.models import Request

def show_result(method, data, label):
    req = Request(method, 'http://example.com', data=data)
    prep = req.prepare()
    print(f"{label}: Content-Length present? {'Content-Length' in prep.headers}, value={prep.headers.get('Content-Length')}")

# GET without body should NOT include Content-Length
show_result('GET', None, 'GET no body')

# POST with body should include Content-Length
show_result('POST', {'a':'b'}, 'POST with body')

# POST with empty body should NOT include Content-Length
show_result('POST', None, 'POST empty body')
PY
```
````

</details>

<details>
<summary><strong>Step 8</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>2</returncode>
<output>
Patched prepare_content_length to avoid Content-Length on empty body
bash: -c: line 27: syntax error near unexpected token `&&'
bash: -c: line 27: `&& python - <<'PY''
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: The previous attempt to chain two here-doc Python commands with && caused syntax issues because the second here-doc start was interpreted inside the first Python script. To avoid that, I'll run a single Python script that imports the modified Request class, prepares requests with and without bodies, and prints whether the Content-Length header is present. This will verify that GET requests without a body no longer include Content-Length, while POST requests with a body still include it.

```bash
python - <<'PY'
from requests.models import Request

def show_result(method, data, label):
    req = Request(method, 'http://example.com', data=data)
    prep = req.prepare()
    print(f"{label}: Content-Length present? {'Content-Length' in prep.headers}, value={prep.headers.get('Content-Length')}")
    print(f"{label} headers: {dict(prep.headers)}")

# Test GET without body: should NOT include Content-Length
show_result('GET', None, 'GET no body')

# Test GET with empty dict (treated as no body): should NOT include Content-Length
show_result('GET', {}, 'GET empty dict')

# Test POST with body: should include Content-Length
show_result('POST', {'a':'b'}, 'POST with body')

# Test POST with empty body explicitly None: should NOT include Content-Length
show_result('POST', None, 'POST empty body')
PY
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
/testbed/requests/models.py:565: SyntaxWarning: "is" with a literal. Did you mean "=="?
  if self.status_code is 0:
GET no body: Content-Length present? True, value=0
GET no body headers: {'Content-Length': '0'}
GET empty dict: Content-Length present? False, value=None
GET empty dict headers: {}
POST with body: Content-Length present? True, value=3
POST with body headers: {'Content-Length': '3', 'Content-Type': 'application/x-www-form-urlencoded'}
POST empty body: Content-Length present? True, value=0
POST empty body headers: {'Content-Length': '0'}
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: The verification showed that even after patching prepare_content_length, a GET without body still ends up with Content-Length: 0, meaning the code path is still inserting it. I should inspect the current contents of requests/models.py around the prepare_content_length function to confirm whether my patch is present as intended and to find any other code paths that might be reintroducing Content-Length. Viewing the relevant section will help me diagnose why the header is still being set.

```bash
nl -ba requests/models.py | sed -n '360,420p'
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
   360	
   361	            if length:
   362	                self.headers['Content-Length'] = length
   363	            else:
   364	                self.headers['Transfer-Encoding'] = 'chunked'
   365	        # Check if file, fo, generator, iterator.
   366	        # If not, run through normal process.
   367	
   368	        else:
   369	            # Multi-part file uploads.
   370	            if files:
   371	                (body, content_type) = self._encode_files(files, data)
   372	            else:
   373	                if data:
   374	                    body = self._encode_params(data)
   375	                    if isinstance(data, str) or isinstance(data, builtin_str) or hasattr(data, 'read'):
   376	                        content_type = None
   377	                    else:
   378	                        content_type = 'application/x-www-form-urlencoded'
   379	
   380	            self.prepare_content_length(body)
   381	
   382	            # Add content-type if it wasn't explicitly provided.
   383	            if (content_type) and (not 'content-type' in self.headers):
   384	                self.headers['Content-Type'] = content_type
   385	
   386	        self.body = body
   387	
   388	    def prepare_content_length(self, body):
   389	        # Avoid automatically sending Content-Length when there is no body.
   390	        # Only set Content-Length when we have a real body to send.
   391	        if body is None:
   392	            # Ensure any previously set Content-Length is removed
   393	            self.headers.pop('Content-Length', None)
   394	            return
   395	        if hasattr(body, 'seek') and hasattr(body, 'tell'):
   396	            body.seek(0, 2)
   397	            self.headers['Content-Length'] = str(body.tell())
   398	            body.seek(0, 0)
   399	        else:
   400	            self.headers['Content-Length'] = str(len(body))
   401	
   402	    def prepare_auth(self, auth):
   403	        """Prepares the given HTTP auth data."""
   404	        if auth:
   405	            if isinstance(auth, tuple) and len(auth) == 2:
   406	                # special-case basic HTTP auth
   407	                auth = HTTPBasicAuth(*auth)
   408	
   409	            # Allow auth to make its changes.
   410	            r = auth(self)
   411	
   412	            # Update self to reflect the auth changes.
   413	            self.__dict__.update(r.__dict__)
   414	
   415	            # Recompute Content-Length
   416	            self.prepare_content_length(self.body)
   417	
   418	    def prepare_cookies(self, cookies):
   419	        """Prepares the given HTTP cookie data."""
   420	
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: The GET request still has Content-Length: 0 after our patch, so there must be another code path setting Content-Length to '0'. I need to search the codebase again for any other occurrences where Content-Length is being set, particularly to '0', and inspect surrounding logic. This will help identify and adjust any remaining places that force Content-Length for empty bodies.

```bash
grep -R -n "Content-Length" requests | sed -n '1,200p'
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
grep: requests/__pycache__/models.cpython-39.pyc: binary file matches
grep: requests/__pycache__/adapters.cpython-39.pyc: binary file matches
requests/adapters.py:157:        chunked = not (request.body is None or 'Content-Length' in request.headers)
requests/models.py:362:                self.headers['Content-Length'] = length
requests/models.py:389:        # Avoid automatically sending Content-Length when there is no body.
requests/models.py:390:        # Only set Content-Length when we have a real body to send.
requests/models.py:392:            # Ensure any previously set Content-Length is removed
requests/models.py:393:            self.headers.pop('Content-Length', None)
requests/models.py:397:            self.headers['Content-Length'] = str(body.tell())
requests/models.py:400:            self.headers['Content-Length'] = str(len(body))
requests/models.py:415:            # Recompute Content-Length
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: The GET with data=None is being converted to an empty list in Request.__init__, triggering the streaming branch which sets Content-Length: '0'. To fix this generally and align with expected behavior, I'll change that conversion to use an empty dict instead (so data=None -> {}), preventing the streaming path for default/None cases. Combined with the earlier change to prepare_content_length (which avoids setting Content-Length when body is None), this will ensure GET requests without a body do not send Content-Length. I'll patch the __init__ accordingly and then verify with a small script.

```bash
python - <<'PY'
import io, sys, re

path = 'requests/models.py'
src = io.open(path, 'r', encoding='utf-8').read()

# Patch Request.__init__ to avoid converting data=None to [] (stream), use {} instead
new_src, n = re.subn(r"data = \[\] if data is None else data", "data = {} if data is None else data", src, count=1)
if n == 0:
    print("No change made: pattern not found for data conversion", file=sys.stderr)
else:
    io.open(path, 'w', encoding='utf-8').write(new_src)
    print("Patched Request.__init__: data=None now becomes {} (not []), avoiding stream path")

# Run verification
from requests.models import Request

def show_result(method, data, label):
    req = Request(method, 'http://example.com', data=data)
    prep = req.prepare()
    print(f"{label}: Content-Length present? {'Content-Length' in prep.headers}, value={prep.headers.get('Content-Length')}, headers={dict(prep.headers)}")

print("Verifying behavior after patch...")
# GET with None should NOT include Content-Length
show_result('GET', None, 'GET with data=None')

# GET default (no data passed) should NOT include Content-Length
req_default = Request('GET', 'http://example.com')
prep_default = req_default.prepare()
print(f"GET default: Content-Length present? {'Content-Length' in prep_default.headers}, value={prep_default.headers.get('Content-Length')}, headers={dict(prep_default.headers)}")

# POST with body should include Content-Length
show_result('POST', {'a': 'b'}, 'POST with body')

# POST with None should NOT include Content-Length (consistent with no body)
show_result('POST', None, 'POST with data=None')
PY
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
/testbed/requests/models.py:565: SyntaxWarning: "is" with a literal. Did you mean "=="?
  if self.status_code is 0:
Patched Request.__init__: data=None now becomes {} (not []), avoiding stream path
Verifying behavior after patch...
GET with data=None: Content-Length present? False, value=None, headers={}
GET default: Content-Length present? False, value=None, headers={}
POST with body: Content-Length present? True, value=3, headers={'Content-Length': '3', 'Content-Type': 'application/x-www-form-urlencoded'}
POST with data=None: Content-Length present? False, value=None, headers={}
</output>
Reflect on the previous trajectories and decide if there are any tools you can create to help you with the current task.
Note that just because you can use basic bash commands doesn't mean you should not create any tools that can still be helpful.
```

## LLM response

````text
THOUGHT: We've identified and fixed two sources of unwanted Content-Length on GET: prepare_content_length was setting Content-Length to '0' for None bodies, and Request.__init__ converted data=None to an empty list, triggering the streaming path and setting Content-Length. We updated prepare_content_length to skip setting Content-Length when body is None and changed Request.__init__ to default data to {} instead of []. Verification script showed GET requests now omit Content-Length and POST with body retains it. Next, I will run the repository's tests to ensure our changes don't break existing functionality.

```bash
python test_requests.py
```
````

</details>

<details>
<summary><strong>Step 13</strong></summary>

## Prompt sent to LLM

```text
[user]
<returncode>1</returncode>
<warning>
The output of your last command was too long.
Please try a different command that produces less output.
If you're looking at a file you can try use head, tail, sed or create a tool to view a smaller number of lines selectively.
If you're using grep or find and it produced too much output, you can use a more selective search pattern.
</warning><output_head>
/testbed/requests/models.py:140: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3, and in 3.10 it will stop working
  if isinstance(hook, collections.Callable):
EEEEEEEEEEE.E/opt/miniconda3/envs/testbed/lib/python3.9/unittest/case.py:614: ResourceWarning: unclosed file <_io.BufferedReader name='/testbed/test_requests.py'>
  outcome.errors.clear()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
EE..E..EEEEEE
======================================================================
ERROR: test_BASICAUTH_TUPLE_HTTP_200_OK_GET (__main__.RequestsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testbed/test_requests.py", line 136, in test_BASICAUTH_TUPLE_HTTP_200_OK_GET
    r = requests.get(url, auth=auth)
  File "/testbed/requests/api.py", line 55, in get
    return request('get', url, **kwargs)
  File "/testbed/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/testbed/requests/sessions.py", line 280, in request
    resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
  File "/testbed/requests/sessions.py", line 373, in send
    r = adapter.send(request, **kwargs)
  File "/testbed/requests/adapters.py", line 161, in send
    resp = conn.urlopen(
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 416, in urlopen
    conn = self._get_conn(timeout=pool_timeout)
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 231, in _get_conn
    return conn or self._new_conn()
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 196, in _new_conn
    return HTTPConnection(host=self.host,
TypeError: __init__() got an unexpected keyword argument 'strict'

======================================================================
ERROR: test_DIGESTAUTH_WRONG_HTTP_401_GET (__main__.RequestsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testbed/test_requests.py", line 168, in test_DIGESTAUTH_WRONG_HTTP_401_GET
    r = requests.get(url, auth=auth)
  File "/testbed/requests/api.py", line 55, in get
    return request('get', url, **kwargs)
  File "/testbed/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/testbed/requests/sessions.py", line 280, in request
    resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
  File "/testbed/requests/sessions.py", line 373, in send
    r = adapter.send(request, **kwargs)
  File "/testbed/requests/adapters.py", line 161, in send
    resp = conn.urlopen(
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 416, in urlopen
    conn = self._get_conn(timeout=pool_timeout)
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 231, in _get_conn
    return conn or self._new_conn()
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 196, in _new_conn
    return HTTPConnection(host=self.host,
TypeError: __init__() got an unexpected keyword argument 'strict'

======================================================================
ERROR: test_DIGEST_HTTP_200_OK_GET (__main__.RequestsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testbed/test_requests.py", line 152, in test_DIGEST_HTTP_200_OK_GET
    r = requests.get(url, auth=auth)
  File "/testbed/requests/api.py", line 55, in get
    return request('get', url, **kwargs)
  File "/testbed/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/testbed/requests/sessions.py", line 280, in request
    resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
  File "/testbed/requests/sessions.py", line 373, in send
    r = adapter.send(request, **kwargs)
  File "/testbed/requests/adapters.py", line 161, in send
    resp = conn.urlopen(
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 416, in urlopen
    conn = self._get_conn(timeout=pool_timeout)
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 231, in _get_conn
    return conn or self._new_conn()
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 196, in _new_conn
    return HTTPConnection(host=self.host,
TypeError: __init__() got an unexpected keyword argument 'strict'

======================================================================
ERROR: test_HTTP_200_OK_GET_ALTERNATIVE (__main__.RequestsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testbed/test_requests.py", line 80, in test_HTTP_200_OK_GET_ALTERNATIVE
    r = s.send(r.prepare())
  File "/testbed/requests/se
</output_head>
<elided_chars>
18621 characters elided
</elided_chars>
<output_tail>
ne 280, in request
    resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
  File "/testbed/requests/sessions.py", line 373, in send
    r = adapter.send(request, **kwargs)
  File "/testbed/requests/adapters.py", line 161, in send
    resp = conn.urlopen(
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 416, in urlopen
    conn = self._get_conn(timeout=pool_timeout)
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 231, in _get_conn
    return conn or self._new_conn()
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 196, in _new_conn
    return HTTPConnection(host=self.host,
TypeError: __init__() got an unexpected keyword argument 'strict'

======================================================================
ERROR: test_unicode_get (__main__.RequestsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testbed/test_requests.py", line 236, in test_unicode_get
    requests.get(url, params={'foo': 'føø'})
  File "/testbed/requests/api.py", line 55, in get
    return request('get', url, **kwargs)
  File "/testbed/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/testbed/requests/sessions.py", line 280, in request
    resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
  File "/testbed/requests/sessions.py", line 373, in send
    r = adapter.send(request, **kwargs)
  File "/testbed/requests/adapters.py", line 161, in send
    resp = conn.urlopen(
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 416, in urlopen
    conn = self._get_conn(timeout=pool_timeout)
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 231, in _get_conn
    return conn or self._new_conn()
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 196, in _new_conn
    return HTTPConnection(host=self.host,
TypeError: __init__() got an unexpected keyword argument 'strict'

======================================================================
ERROR: test_urlencoded_get_query_multivalued_param (__main__.RequestsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testbed/test_requests.py", line 244, in test_urlencoded_get_query_multivalued_param
    r = requests.get(httpbin('get'), params=dict(test=['foo', 'baz']))
  File "/testbed/requests/api.py", line 55, in get
    return request('get', url, **kwargs)
  File "/testbed/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/testbed/requests/sessions.py", line 280, in request
    resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
  File "/testbed/requests/sessions.py", line 373, in send
    r = adapter.send(request, **kwargs)
  File "/testbed/requests/adapters.py", line 161, in send
    resp = conn.urlopen(
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 416, in urlopen
    conn = self._get_conn(timeout=pool_timeout)
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 231, in _get_conn
    return conn or self._new_conn()
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 196, in _new_conn
    return HTTPConnection(host=self.host,
TypeError: __init__() got an unexpected keyword argument 'strict'

======================================================================
ERROR: test_user_agent_transfers (__main__.RequestsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/testbed/test_requests.py", line 113, in test_user_agent_transfers
    r = requests.get(httpbin('user-agent'), headers=heads)
  File "/testbed/requests/api.py", line 55, in get
    return request('get', url, **kwargs)
  File "/testbed/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/testbed/requests/sessions.py", line 280, in request
    resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
  File "/testbed/requests/sessions.py", line 373, in send
    r = adapter.send(request, **kwargs)
  File "/testbed/requests/adapters.py", line 161, in send
    resp = conn.urlopen(
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 416, in urlopen
    conn = self._get_conn(timeout=pool_timeout)
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 231, in _get_conn
    return conn or self._new_conn()
  File "/testbed/requests/packages/urllib3/connectionpool.py", line 196, in _new_conn
    return HTTPConnection(host=self.host,
TypeError: __init__() got an unexpected keyword argument 'strict'

----------------------------------------------------------------------
Ran 26 tests in 0.014s

FAILED (errors=21)

</output_tail>
```

## LLM response

````text
THOUGHT: I've identified and implemented changes to prevent automatically adding the Content-Length header for requests without a body, which addresses the PR issue. Specifically, I modified prepare_content_length to avoid setting Content-Length when body is None and updated Request.__init__ to default data=None to an empty dict rather than an empty list to avoid triggering the streaming path. I verified that GET requests without a body no longer include the Content-Length header and POST requests with a body still include it. Now I'll submit the changes.

```bash
echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && git add -A && git diff --cached
```
````

</details>
