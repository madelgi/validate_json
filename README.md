# Sphinx JSON Validator

This is a small sphinx extension for checking json source examples in documentation
for correctness and style.

## Usage

Place `validate_json.py` in your extension directory, and add `validate_json` to the
`extensions` list in your conf.py file. When building your docs, add the `-b validate`
flag to initialize JSON validation.

The extension will begin looking for JSON that is either:

1. Syntactically incorrect
2. Indented inconsistently


**Sample Output**:

```bash
sdk/bleep.rst | [INDENT ERROR] | Line 7943
sdk/bleep.rst | [INVALID JSON] | Line 8039
sdk/bleep.rst | [INVALID JSON] | Line 8103
sdk/bleep.rst | [INDENT ERROR] | Line 8269
sdk/bleep.rst | [INVALID JSON] | Line 8680
sdk/bleep.rst | [INDENT ERROR] | Line 8680
sdk/bleep.rst | [INVALID JSON] | Line 8807
sdk/bleep.rst | [INVALID JSON] | Line 8890
sdk/bleep.rst | [INDENT ERROR] | Line 8890
sdk/other_doc.rst | [INDENT ERROR] | Line 754
sdk/other_doc.rst | [INDENT ERROR] | Line 2374
```


### Manual Override

Sometimes, this tool will throw an error on JSON that is technically incorrect, but still valid
from a documentation point of view. For example, you may occasionally choose to use pseudo-json
in your documentation, e.g.:

```rst
.. sourcecode:: json

   [
      {
         "key1": 3,
         "key2": "bar"
      },
      { "..." }
   ]
```

In the above example, the ``{ "..." }`` just implies that there may be more objects in the list,
but the syntax is not technically valid JSON. To prevent ``make validate`` from throwing errors
when encountering json like this, preface the directive with ``.. json_valid``:

```rst
.. json_valid
.. sourcecode:: json

   [
      {
         "key1": 3,
         "key2": "bar"
      },
      { "..." }
   ]
```

The above example will no longer throw an ``[INVALID JSON]`` error.
