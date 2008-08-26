from sugar.activity import activity
from sugar import env
import os
import gtk
import gobject
import hulahop
hulahop.startup(os.path.join(env.get_profile_path(), 'gecko'))


from sugar.activity.activity import Activity, ActivityToolbox, EditToolbar
import toolbar
from toolbar import SpreadSheetActivityToolbar, SpreadsheetEditToolbar, ViewToolbar
from sugar.activity,activity import get_bundle_path

from XOCom import XOCom

class SocialCalcActivity (activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.set_title('SocialCalc')

        # The XOCom object helps us communicate with the browser
        # This uses web/index.html as the default page to load
        self.xocom = XOCom()

        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        self.set_canvas( self.xocom.create_webview() )
        activity_toolbar_ext = SpreadSheetActivityToolbar(toolbox, self.set_canvas, self)

        self._edit_toolbar = SpreadsheetEditToolbar(self, self._edit_toolbar, set_canvas)
        toolbox.add_toolbar(_('Edit'),self._edit_toolbar)
        self._edit_toolbar.show()

        view_toolbar = ViewToolbar (self.set_canvas)
        self.set_canvas.show()
    
    def write_file(self, filename):
        content = self.xocom.send_to_browser('write')
        if content:
            fh = open(filename, 'w')
            fh.write(content)
            fh.close()

    def read_file(self, filename):
        fh = open(filename, 'r')
        content = fh.read()
        def send_delayed_read():
            self.xocom.send_to_browser('read', content)
            return False
        # We must delay this to give the browser time to start up
        # It would be better if this send_to_browser was instead triggered
        # once the browser had finished loading.
        gobject.timeout_add(5000, send_delayed_read)
