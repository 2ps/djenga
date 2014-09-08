import pynliner


class EngineBase(object):
    def __init__(self, html, css):
        self.html = html
        self.css = css

    def render(self):
        raise NotImplementedError()


class InlineCssEngine(EngineBase):
    def render(self):
        inliner = pynliner.Pynliner().from_string(self.html)
        inliner = inliner.with_cssString(self.css)
        return inliner.run()


class NullEngine(EngineBase):
    def render(self):
        return self.html
