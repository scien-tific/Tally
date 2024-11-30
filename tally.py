import sublime
from sublime_plugin import ApplicationCommand, EventListener


SETTINGS_FILE = "Tally.sublime-settings"
DEFAULT_SYNTAX = "default"


class TallyEventListener(EventListener):
	def __init__(self):
		self.settings = sublime.load_settings(SETTINGS_FILE)
		self.line_counts = {}
	
	
	def get_regex(self, syntax):
		if syntax is not None and self.settings.has(syntax.name):
			return self.settings.get(syntax.name)
		
		return self.settings.get(DEFAULT_SYNTAX)
	
	def enabled(self):
		return self.settings.get("enabled")
	
	def max_size(self):
		return self.settings.get("max_size")
	
	
	def update(self, view):
		if not view.is_valid() or view.element() is not None:
			return
		
		if not self.enabled() or view.size() > self.max_size():
			view.erase_status("tally")
			return
		
		syntax = view.syntax()
		count = 0
		change_count = -1
		
		if view.buffer_id() in self.line_counts:
			(count, change_count) = self.line_counts[view.buffer_id()]
		
		if view.change_count() != change_count:
			regex = self.get_regex(syntax)
			count = len(view.find_all(regex))
			change_count = view.change_count()
			self.line_counts[view.buffer_id()] = (count, change_count)
		
		view.set_status("tally", "Tally " + str(count))
	
	
	def on_activated_async(self, view):
		self.update(view)
	
	def on_modified_async(self, view):
		self.update(view)


class TallyEnableCommand(ApplicationCommand):
	def run(self):
		settings = sublime.load_settings(SETTINGS_FILE)
		settings.set("enabled", True)
		sublime.save_settings(SETTINGS_FILE)

class TallyDisableCommand(ApplicationCommand):
	def run(self):
		settings = sublime.load_settings(SETTINGS_FILE)
		settings.set("enabled", False)
		sublime.save_settings(SETTINGS_FILE)