import sublime, sublime_plugin
from datetime import datetime

_start_time = None
_start_count = None

class WordCountCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global _start_time
		global _start_count
		if not _start_time:
			_start_time = datetime.utcnow()
			content = self.view.substr(sublime.Region(0, self.view.size()))
			_start_count = sum(1 for word in content.split() if any(c.isalpha() for c in word) and len(word) > 2)
		else:
			_start_time = None
			self.view.erase_status("wpm")
			self.view.erase_status("wc")


class WordCountEvents(sublime_plugin.EventListener):
	def on_modified(self, view):
		global _start_count

		if _start_time:
			content = view.substr(sublime.Region(0, view.size()))
			word_count = sum(1 for word in content.split() if any(c.isalpha() for c in word) and len(word) > 2)
			word_count = word_count - _start_count

			view.set_status("wc", "WORD COUNT: {0}".format(word_count))

			now = datetime.utcnow()
			delta = now - _start_time
			delta_sec = delta.seconds
			if(delta_sec > 0):
				delta_min = delta_sec / 60
				if delta_min < 1:
					delta_min = 1
				wpm = word_count / delta_min
				view.set_status("wpm", "WORDS PER MIN: {0}".format(wpm))
		else:
			view.erase_status("wpm")
			view.erase_status("wc")

