from libqtile.widget import base

class KeyboardLanguage(base.ThreadPoolText, base.MarginMixin, base.PaddingMixin):

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(base.MarginMixin.defaults)
        self.add_defaults(base.PaddingMixin.defaults)
        self.update_interval = 1

    def poll(self):
        return self.call_process("xkb-switch -p".split())[0:2].upper()
