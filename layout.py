from gettext import gettext as _
import pygtk
pygtk.require('2.0')
import gtk
import pango
from sugar.activity import activity
from toolbars import *

class BoardLayout:

    def __init__(self, parent):
        self._parent = parent
        self.create_dialog()

    def create_color(self, rf, gf, bf):
        return gtk.gdk.Color(int(rf*0xFFFF), int(gf*0xFFFF), int(bf*0xFFFF))

    def create_button_data(self):
        self.button_data = [
# [x, y, width, label, bgcol, cb]
            [0, 0, 1, '7', self.col_gray2, lambda w: self._parent.add_text('7')],
            [1, 0, 1, '8', self.col_gray2, lambda w: self._parent.add_text('8')],
            [2, 0, 1, '9', self.col_gray2, lambda w: self._parent.add_text('9')],
      
      
            [0, 2, 1, '1', self.col_gray2, lambda w: self._parent.add_text('1')],
            [1, 2, 1, '2', self.col_gray2, lambda w: self._parent.add_text('2')],
            [2, 2, 1, '3', self.col_gray2, lambda w: self._parent.add_text('3')],
                            ]
        
    def create_dialog(self):
# Toolbar
#        toolbox = activity.ActivityToolbox(self._parent)
#        self._parent.set_toolbox(toolbox)
#        toolbox.add_toolbar(_('Edit'), EditToolbar(self._parent))
#        toolbox.add_toolbar(_('Algebra'), AlgebraToolbar(self._parent))
#        toolbox.add_toolbar(_('Trigonometry'), TrigonometryToolbar(self._parent))
#        toolbox.add_toolbar(_('Boolean'), BooleanToolbar(self._parent))
#        toolbox.add_toolbar(_('Constants'), ConstantsToolbar(self._parent))
#        toolbox.add_toolbar(_('Format'), FormatToolbar(self._parent))
#        toolbox.show_all()

# Some layout constants
        self.input_font = pango.FontDescription(str='sans bold 12')
        self.button_font = pango.FontDescription(str='sans bold 16')
        self.col_white = self.create_color(1.00, 1.00, 1.00)
        self.col_gray1 = self.create_color(0.69, 0.71, 0.72)
        self.col_gray2 = self.create_color(0.51, 0.51, 0.53)
        self.col_gray3 = self.create_color(0.30, 0.30, 0.31)
        self.col_black = self.create_color(0.00, 0.00, 0.00)
        self.col_red = self.create_color(1.00, 0.00, 0.00)

# Big - Table, 16 rows, 10 columns, homogeneously divided
        self.grid = gtk.Table(16, 11, True)
        self.grid.set_border_width(6)
        self.grid.set_row_spacings(6)
        self.grid.set_col_spacings(6)

# Left part: container and input
        hc1 = gtk.HBox(False, 10)
        label1 = gtk.Label(_('Label:'))
        hc1.add(label1)
        self.label_entry = gtk.Entry()
        hc1.add(self.label_entry)
        self.grid.attach(hc1, 0, 6, 0, 1)
        
        self.text_entry = gtk.Entry()
        self.text_entry.set_size_request(400, 100)
        self.text_entry.connect('key_press_event', self._parent.ignore_key_cb)
        self.text_entry.modify_font(self.input_font)
        self.grid.attach(self.text_entry, 0, 6, 1, 5)

# Left part: buttons
        self.pad = gtk.Table(4, 6, True)
        self.pad.set_row_spacings(6)
        self.pad.set_col_spacings(6)
        self.create_button_data()
        self.buttons = {}
        for x, y, w, cap, bgcol, cb in self.button_data:
            button = self.create_button(_(cap), cb, self.col_white, bgcol, w)
            self.buttons[cap] = button
            self.pad.attach(button, x, x+w, y, y+1)

# Not for now...
#        self.pad_ebox = gtk.EventBox()
#        self.pad_ebox.add(self.pad)
#        self.pad_ebox.modify_bg(gtk.STATE_NORMAL, self.col_black)

        self.grid.attach(self.pad, 0, 6, 5, 16)

# Right part: container and equation button
        hc2 = gtk.HBox()
        self.minebut = TextToggleToolButton([_('All equations'), _('My equations')],
            lambda x: self._parent.refresh_bar())
        self.varbut = TextToggleToolButton([_('Show history'), _('Show variables')],
            lambda x: self._parent.refresh_bar())
        hc2.add(self.minebut)
        hc2.add(self.varbut)
        self.grid.attach(hc2, 6, 11, 0, 1)
        
# Right part: last equation
        self.last_eq = gtk.TextView()
        self.last_eq.set_editable(False)
        self.last_eq.set_wrap_mode(gtk.WRAP_WORD)
        self.grid.attach(self.last_eq, 6, 11, 1, 5)

# Right part: history
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.history = gtk.VBox()
        self.history.set_homogeneous(False)
        self.history.set_border_width(6)
        scrolled_window.add_with_viewport(self.history)
        self.grid.attach(scrolled_window, 6, 11, 5, 16)

    def show_it(self):
        self._parent.set_canvas(self.grid)
        self._parent.show_all()
        self.text_entry.grab_focus()

    def show_history(self, window_list):
        if self.history is None:
            return
        for el in self.history.get_children():
            self.history.remove(el)
        for w in window_list:
            self.history.pack_start(w, expand=False, fill=False, padding=1)
        self._parent.show_all()

    def create_button(self, cap, cb, fgcol, bgcol, width):
        button = gtk.Button(_(cap))
        self.modify_button_appearance(button, fgcol, bgcol, width)
        button.connect("clicked", cb)
        button.connect("key_press_event", self._parent.ignore_key_cb)
        return button

    def modify_button_appearance(self, button, fgcol, bgcol, width):
        width = 50 * width
        button.get_child().set_size_request(width, 50)
        button.get_child().modify_font(self.button_font)
        button.get_child().modify_fg(gtk.STATE_NORMAL, fgcol)
        button.modify_bg(gtk.STATE_NORMAL, bgcol)
