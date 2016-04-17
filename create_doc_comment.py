import sublime
import sublime_plugin
import re

"""
Creates a documentation comment on the current line.

A doc comment is created only if the cursor is not already in a doc comment.
The cursor is in a doc comment if:

* The scope at the cursor matches 'common.block.documentation'; or
* The next or previous line starts with white space followed by "///".

If the plugin finds that the user is in a doc comment already, the trigger
text (usually "/" - sent as an argument to the command) is inserted, so the
user gets "///" and can write more of their glorious, wonderful documentation.
"""

DEFAULT_TRIGGER = '/'
TRIGGER_TO_DOC_LINE_START = {
    '/': '///',
    '*': '*'
}

has_doc_comment = re.compile(r'^\s*///')

def is_in_doc_comment(view, line_region, cursor_point):
    # Doc block comment - /** ... */
    if view.score_selector(cursor_point, 'comment.block.documentation') > 0:
        return True

    prev_line_region = view.line(line_region.begin() - 1)
    prev_line = view.substr(prev_line_region)
    if has_doc_comment.match(prev_line):
        return True

    next_line_region = view.line(line_region.end() + 1)
    next_line = view.substr(next_line_region)
    if has_doc_comment.match(next_line):
        return True

    return False

def generate_doc_comment_snippet(view, line_region, trigger):
    next_line_region = view.line(line_region.end() + 1)

    # At this point, we assume the user has some kind of sensible Osprey syntax
    # highlighter that gives parameters the scope 'variable.parameter'.
    # Unfortunately there doesn't seem to be a way to restrict find_by_selector
    # to a particular region, so we have to search the whole document and then
    # filter out anything outside the next line.
    # TODO: This will fail (or behave unpredictably) if the parameter list is
    # broken up over multiple lines.
    parameters = view.find_by_selector('variable.parameter')
    parameters = filter(next_line_region.contains, parameters)
    parameters = list(parameters) # need len

    if len(parameters) == 0:
        # No parameters, so just generate "/// Summary:"
        return trigger + ' Summary: '

    # If there are parameters, we want to create snippet fields for each of them.
    # Fields are numbered so that Summary is $1, the first parameter is $2, and
    # the last parameter is $0. So the user can keep typing after the last param
    # and maybe even add more sections, like Returns.

    snippet_text = trigger + ' Summary: $1'

    doc_line_start = TRIGGER_TO_DOC_LINE_START[trigger]

    for index, param_region in enumerate(parameters):
        param_name = view.substr(param_region)

        if index == len(parameters) - 1:
            field_index = 0
        else:
            # +2 because snippet_text is 1
            field_index = index + 2

        # No indentation; the snippet system fixes it up for us.
        snippet_text += '\n{0} Param {1}: ${2}'.format(doc_line_start, param_name, field_index)

    return snippet_text

class OspreyCreateDocCommentCommand(sublime_plugin.TextCommand):
    def is_enabled(self, **args):
        # This command can only be used when the selection is empty
        view = self.view
        if len(view.sel()) != 1:
            return False

        first_sel = view.sel()[0]
        return first_sel.empty()

    def run(self, edit, **args):
        trigger = args.get('trigger', DEFAULT_TRIGGER)

        view = self.view
        sel = view.sel()[0]
        line_region = view.line(sel.begin())

        if is_in_doc_comment(view, line_region, sel.begin()):
            # We're already in a doc comment (probably), so just insert the
            # trigger and let the user keep typing.
            view.run_command('insert', {'characters': trigger})
            snippet_text = trigger
        else:
            # We're NOT already in a doc comment, so let's generate one!
            snippet_text = generate_doc_comment_snippet(view, line_region, trigger)
            view.run_command('insert_snippet', {'contents': snippet_text})

