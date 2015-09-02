# Sphinx JSON Validator

This is a small sphinx extension for checking json source examples in documentation
for correctness and style.

## Usage

Place `validate_json.py` in your extension directory, and add `validate_json` to the
`extensions` list in your conf.py file. When building your docs, add the `-b validate` flag
to initialize JSON validation.
