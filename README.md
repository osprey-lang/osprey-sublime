# Osprey for Sublime Text

*(Heavy WIP.)*

**Compatible with Sublime Text 3 Build 3084 and above.**

Everything you need for rapid development of Osprey programs in Sublime Text.

Currently supported:

* Syntax highlighting (via `.sublime-syntax` file – works only with ST3 Build 3084 and above).
* Snippets for various constructs:
  - `get` for read-only properties, `prop` for read-write properties (inside class bodies)
  - `use`, `usea` (use alias), `usef` (use file)
  - `catch`, `const`, `do–while`, `else`, `finally`, `for`, `if`, `throw`, `try`, `var`, `while`, `with`
* Standard keyboard shortcuts for toggling comments (Default: <kbd>Ctrl/Cmd</kbd>+<kbd>/</kbd>, <kbd>Ctrl/Cmd</kbd>+<kbd>Shift</kbd>+<kbd>/</kbd>).
* Improved documentation comment editing:
  - Typing `///` will start a documentation comment, if you are not already in one.
  - The new documentation comment automatically gets parameters from the next line (but only the next line – parameter lists broken over multiple lines are not examined (this may be fixed in a future version))
  - Enter continues the doc comment onto the next line, with contents appropriately indented (use <kbd>Ctrl/Cmd</kbd>+<kbd>Enter</kbd> or <kbd>Shift</kbd>+<kbd>Enter</kbd> to start a new line without `///`)
  - Automatically fixes formatting of new sections: <code>///&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Remarks:</code> becomes `/// Remarks:`.
* Automatic file name suggestion based on types and functions declared in the file.
