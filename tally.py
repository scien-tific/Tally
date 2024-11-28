import sublime
from sublime_plugin import ApplicationCommand, EventListener


SETTINGS_FILE = "Tally.sublime-settings"
DEFAULT_SYNTAX = "default"


class TallyEventListener(EventListener):
	def get_regex(self, syntax):
		if syntax is None:
			return self.settings.get(DEFAULT_SYNTAX)
		
		if self.settings.has(syntax.name):
			return self.settings.get(syntax.name)
		
		return self.settings.get(DEFAULT_SYNTAX)
	
	def is_shown(self):
		return self.settings.get("show")
	
	def max_size(self):
		return self.settings.get("max_size")
	
	
	def update(self, view):
		if not self.is_shown() or view.size() > self.max_size():
			view.erase_status("tally")
			for v in view.clones():
				v.erase_status("tally")
			
			return
		
		syntax = view.syntax()
		regex = self.get_regex(syntax)
		count = len(view.find_all(regex))
		status = "Tally " + str(count)
		
		view.set_status("tally", status)
		for v in view.clones():
			v.set_status("tally", status)
	
	
	def on_init(self, views):
		self.settings = sublime.load_settings(SETTINGS_FILE)
	
	def on_activated_async(self, view):
		self.update(view)
	
	def on_modified_async(self, view):
		if not view.is_primary():
			self.update(view)


class TallyShowCommand(ApplicationCommand):
	def run(self):
		settings = sublime.load_settings(SETTINGS_FILE)
		settings.set("show", True)
		sublime.save_settings(SETTINGS_FILE)

class TallyHideCommand(ApplicationCommand):
	def run(self):
		settings = sublime.load_settings(SETTINGS_FILE)
		settings.set("show", False)
		sublime.save_settings(SETTINGS_FILE)