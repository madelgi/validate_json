import os
import codecs
import json

from sphinx.builders import Builder
from sphinx.util.console import yellow, red


class JSONValidateBuilder(Builder):
    """
    Checks JSON samples in a document.
    """
    name = 'validate'

    def init(self):
        self.output_filename = os.path.join(self.outdir, 'output.txt')
        self.output = codecs.open(self.output_filename, 'w', encoding='UTF-8')

    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self, docnames):
        return

    def get_target_uri(self, docname, typ=None):
        return ''

    def write_doc(self, docname, doctree):

        for node in doctree.traverse(condition=json_block):
            lineno = node.line

            body = node.astext()

            # check if the json is valid.
            if not check_json(body):
                f = docname + '.rst'
                msg = f + ' | [INVALID JSON] | Line ' + str(lineno)
                self.info(red(msg))
                self.output.write(u"%s [Invalid JSON] %s \n" % (
                    self.env.doc2path(docname, None),
                    lineno
                ))

            # check if the indentation is consistent
            if not check_indent(body):
                f = docname + '.rst'
                msg = f + ' | [INDENT ERROR] | Line ' + str(lineno)
                self.info(yellow(msg))
                self.output.write(u"%s [INDENT] %s \n" % (
                    self.env.doc2path(docname, None),
                    lineno
                ))

        return

    def finish(self):
        self.output.close()
        self.info('JSON error messages written to %s' %
                  self.output_filename)
        return


def check_json(block):
    """ Check if the given block is valid JSON """
    try:
        json.loads(block)
    except ValueError, e:
        return False
    return True


def check_indent(json_string):
    """Catches poorly indented JSON samples.

    Args:
        json_string ([string]): a list of strings comprising a json code block.
            Should be lines ripped directly from an rst file, with leading
            whitespace intact, e.g.:

            ['{', '    "key": "value"', '}']

    Returns:
        A bool reflecting whether the block has been indented in a
        consistent manner.

    """
    block = json_string.split('\n')

    if len(block) <= 1:
        return True

    indent = leading_wspace(block[1]) - leading_wspace(block[0])
    # if there is no indent on the line following the opening bracket, return
    # false.
    if indent == 0:
        return False

    prev_indent = leading_wspace(block[0])
    for i in xrange(1, len(block)):
        current_indent = leading_wspace(block[i])

        if current_indent == 0:
            continue
        if not (current_indent - prev_indent) in [0, indent, -indent]:
            return False

        prev_indent = current_indent

    return True


def leading_wspace(string):
    """Takes a string and returns the number of leading spaces."""
    return len(string) - len(string.lstrip(' '))


def json_block(node):
    """Check if a docutils node is a json block"""
    if node.tagname == 'literal_block' and is_lang(node, 'json'):
            return True
    return False


def is_lang(node, language):
    """Check the langauge of a `literal_block` node"""
    strnode = str(node)

    if 'language=\"' + language + "\"" in strnode:
        return True
    return False


def setup(app):
    app.info('Initializing JSON Validation')
    app.add_builder(JSONValidateBuilder)
    return
