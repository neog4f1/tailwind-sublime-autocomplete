import sublime_plugin
import sublime

class tailwindCompletions(sublime_plugin.EventListener):
    # def __init__(self):
        # self.class_completions = [("%s \tTailwind Class" % s, s) for s in tailwindClasses]
        
    def on_init(self, views):
        self.settings = sublime.load_settings("tailwind_autocomplete.sublime-settings")
        tailwindClasses = self.settings.get("tailwindClasses")
        self.class_completions = [("%s \tTailwind Class" % s, s) for s in tailwindClasses]

    def on_query_completions(self, view, prefix, locations):
        # settings = sublime.load_settings("tailwind_autocomplete.sublime-settings")
        jsSources = self.settings.get("scopes")

        # matchHTMLString = view.match_selector(locations[0], "text.html string.quoted")
        checkScope = next(filter(lambda source: view.match_selector(locations[0], source), jsSources), None)
        
        if not checkScope:
            return []

        classNames = self.settings.get("classNames")
        # max search size
        LIMIT = self.settings.get("limitChars")

        # Cursor is inside a quoted attribute
        # Now check if we are inside the class attribute

        # place search cursor one word back
        cursor = locations[0] - len(prefix) - 1

        # dont start with negative value
        start  = max(0, cursor - LIMIT - len(prefix))

        # get part of buffer
        line   = view.substr(sublime.Region(start, cursor))

        # split attributes
        parts  = line.split('=')
        
        # classNames
        # classNames = ["className", "ClassName", "class"]
        
        for item in classNames:
            if len(parts) > 1 and parts[-2].strip().endswith(item):
                return self.class_completions

        # is the last typed attribute a class attribute?
        # if matchHTMLString:
          # if len(parts) > 1 and parts[-2].strip().endswith("class"):
            # return self.class_completions
        # if matchJSString:
        # if len(parts) > 1 and parts[-2].strip().endswith("className"):
          # return self.class_completions
        # if len(parts) > 1 and parts[-2].strip().endswith("class"):
            # return self.class_completions

        return []
