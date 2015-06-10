import sublime, sublime_plugin
from datetime import datetime

_start_time = None
_start_count = None

class WordCountUtil(object):
	@staticmethod
	def update_selection_data(view):
		words = 0
		if len(view.sel()) and _start_time:
			for selection in view.sel():
				words += WordCountEvents._count_region(view, selection)

		if words == 0:
			view.erase_status("selection")
		else:
			view.set_status("selection", "SELECTED WORDS: {0}".format(words))

	@staticmethod
	def _count_words(string):
		return sum(1 for word in string.split() if any(c.isalpha() for c in word) and len(word) > 2)

	@staticmethod
	def _count_region(view, region):
		return WordCountUtil._count_words(view.substr(region))

	@staticmethod
	def get_word_count(view):
		return WordCountUtil._count_region(view, sublime.Region(0, view.size()))

	@staticmethod
	def update_word_counts(view):
		global _start_count

		if _start_time:
			word_count = WordCountUtil.get_word_count(view)
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
				view.set_status("word_min", "WORD TIME: {0}".format(delta_min))


	@staticmethod
	def clear_status(view):
		view.erase_status("wpm")
		view.erase_status("wc")
		view.erase_status("word_min")
		view.erase_status("selection")

class StopWordCountCommand(sublime_plugin.TextCommand):
	def is_visible(self):
		return _start_time is not None

	def run(self, edit):
		global _start_time
		_start_time = None
		WordCountUtil.clear_status(self.view)

class WordCountCommand(sublime_plugin.TextCommand):
	def is_visible(self):
		return _start_time is None

	def run(self, edit):
		global _start_time
		global _start_count
		_start_time = datetime.utcnow()
		WordCountUtil.update_selection_data(self.view)
		_start_count = WordCountUtil.get_word_count(self.view)
		# add in selection count

class WordCountEvents(sublime_plugin.EventListener):
	@staticmethod
	def _count_words(string):
		return sum(1 for word in string.split() if any(c.isalpha() for c in word) and len(word) > 2)

	@staticmethod
	def _count_region(view, region):
		return WordCountEvents._count_words(view.substr(region))

	def on_selection_modified(self, view):
		WordCountUtil.update_selection_data(view)

	def on_modified(self, view):
		WordCountUtil.update_word_counts(view)
