import sublime
import sublime_plugin
import re

"""
Fixes up the 'indentation' of documentation comment keywords.

E.g. if you type this:

    ///          Summary:

it gets fixed up to:

    /// Summary:

This is necessary because the default keymap inserts lines beginning with "///"
plus ten spaces whenever you type a newline in a documentation comment.
"""

SEARCH_REGEX = {
    'line': re.compile(r'^(\s*)///\s+((?:summary|param|returns|throws|remarks)(?:\s+[^:\s]+)?)\s*$', re.IGNORECASE),
    'block': re.compile(r'^(\s*)\*\s+((?:summary|param|returns|throws|remarks)(?:\s+[^:\s]+)?)\s*$', re.IGNORECASE),
}
REPLACEMENT = {
    'line': r'\g<1>/// \g<2>:',
    'block': r'\g<1>* \g<2>:',
}

def fix_doc_indentation(line, kind):
    regex = SEARCH_REGEX[kind]
    repl = REPLACEMENT[kind]
    return regex.sub(repl, line)

def get_line_before_selection(view, region):
    line_region = view.line(region.begin())
    return sublime.Region(line_region.begin(), region.begin())

class OspreyFixDocCommentKeywordIndent(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        kind = args['kind']
        view = self.view

        selection = view.sel()
        new_selection = []

        # Process in reversed order, otherwise later regions will be weird when text has been replaced.
        for region in reversed(selection):
            before_sel_region = get_line_before_selection(view, region)
            before_sel_text = view.substr(before_sel_region)

            new_contents = fix_doc_indentation(before_sel_text, kind)

            view.replace(edit, sublime.Region(before_sel_region.begin(), region.end()), new_contents)

            new_sel_index = before_sel_region.begin() + len(new_contents)
            new_selection.append(sublime.Region(new_sel_index, new_sel_index))

        selection.clear()
        selection.add_all(new_selection)
