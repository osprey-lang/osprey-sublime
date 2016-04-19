import sublime
import sublime_plugin

MAX_TITLE_LENGTH = 52

SELECTORS = [
    # First attempt: the first defined type name
    'source.osprey entity.name.type',
    # Second attempt: the first defined function
    # Note: this is basically guaranteed to be a
    # global function, because you can't declare
    # a method outside of a type.
    'source.osprey entity.name.function',
]

class SuggestFileName(sublime_plugin.EventListener):
    def on_modified(self, view):
        # Avoid doing unnecessary work
        if view.file_name() is not None:
            return

        syntax = view.settings().get('syntax')
        if syntax and 'Osprey' in syntax:
            name_region = None
            for selector in SELECTORS:
                regions = view.find_by_selector(selector)
                if regions:
                    name_region = regions[0]
                    break

            if name_region:
                name = view.substr(name_region)[:MAX_TITLE_LENGTH]
                view.set_name(name)
            else:
                view.set_name('')
