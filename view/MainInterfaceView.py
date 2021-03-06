from gi.repository import Gtk
from GtkView import GtkView


class MainInterfaceView(GtkView):

	has_dragged_playlist = False

	def __init__(self, main_interface_controller):
		self.gladefile = "view/designs/main_interface.glade"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladefile)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("main_interface_window")
		self.slider = self.builder.get_object("seek_bar")
		self.file_chooser_button = self.builder.get_object("file_chooser_button")
		self.slider.set_range(0, 100)
		super(MainInterfaceView, self).__init__(main_interface_controller)
		self.window.show()

	def on_window1_destroy(self, object, data=None):
		Gtk.main_quit()

	def on_gtk_quit_activate(self, menuitem, data=None):
		Gtk.main_quit()

	def on_play_button_clicked(self, button, data=None):
		self.controller.play_handler()

	def on_pause_button_clicked(self, button, data=None):
		self.controller.pause_handler()

	def on_stop_button_clicked(self, button, data=None):
		self.controller.stop_handler()

	def on_next_button_clicked(self, button, data=None):
		self.controller.next_clip_handler()

	def on_previous_button_clicked(self, button, data=None):
		self.controller.previous_clip_handler()

	def on_loop_toggle_button_toggled(self, button, data=None):
		self.controller.loop_handler(button.get_active())

	def on_seek_bar_button_release_event(self, seek_bar, data=None):
		self.controller.seek_bar_button_release_handler(seek_bar.get_value())

	def on_add_to_playlist_button_clicked(self, button, data=None):
		self.controller.add_file_handler(self.file_chooser_button.get_filenames())

	def on_open_activate(self, button, data=None):
		self.controller.import_playlist_button_clicked()

	def on_save_activate(self, button, data=None):
		self.controller.export_playlist_button_clicked()

	def on_save_as_activate(self, button, data=None):
		self.controller.export_playlist_button_clicked()

	def on_new_activate(self, button, data=None):
		self.controller.new_activated_handler()

	def on_add_unit_button_clicked(self, button, data=None):
		self.controller.add_unit_button_clicked()

	def on_remove_button_clicked(self, button, data=None):
		self.controller.remove_clip()

	def on_in_button_clicked(self, button, data=None):
		self.controller.set_in()

	def on_out_button_clicked(self, button, data=None):
		self.controller.set_out()

	def on_unit_tree_view_cursor_changed(self, tree_selection):
		model, list_iter = tree_selection.get_selection().get_selected()
		self.controller.unit_tree_view_cursor_changed(model.get_path(list_iter)[0])

	def on_playlist_tree_view_cursor_changed(self, tree_selection):
		model, list_iter = tree_selection.get_selection().get_selected()
		if len(model) > 0:
			self.controller.playlist_tree_view_cursor_changed(model.get_path(list_iter)[0])

	def on_in_slider_change_value(self, scale_object, scroll_type, value):
		self.controller.in_slider_change_value_handler(value)

	def on_out_slider_change_value(self, scale_object, scroll_type, value):
		self.controller.out_slider_change_value_handler(value)

	def on_playlist_tree_view_drag_begin(self, drag, drag2):
		self.has_dragged_playlist = True

	def on_playlist_tree_view_drag_end(self, drag, drag2):
		self.has_dragged_playlist = False

	def dragged_playlist(self):
		return self.has_dragged_playlist

	def on_playlist_list_store_row_deleted(self, list_store, tree_path):
		self.controller.check_playlist_order_changed()