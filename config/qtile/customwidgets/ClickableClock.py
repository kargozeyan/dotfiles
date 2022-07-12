from qtile_extras import widget

class ClickableClock(widget.Clock):
    def __init__(self, **config):
        widget.Clock.__init__(self, **config)
        self.format = config['primary']
        self.primary = config['primary']
        self.secondary = config['secondary']
        self.mouse_callbacks = {
            'Button1': self.switch_format
        }

    def switch_format(self):
        self.format = self.secondary if self.format == self.primary else self.primary
        self.bar.draw()