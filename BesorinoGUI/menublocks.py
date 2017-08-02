# File name: menublocks.py
from kivy.uix.relativelayout import RelativeLayout
from draggingblock import DragBlock

class Block(RelativeLayout):
    
    def __init__(self, **kwargs):
        self.ds = None
        self.selected = None
        super(Block,self).__init__(**kwargs)
        
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.ds = self.parent.parent.parent.drawing_area
            (x,y) = self.ds.to_widget(touch.x, touch.y)
            self.draw(self.ds, x, y)
            return True
        return super(Block,self).on_touch_down(touch)

    def draw(self, ds, x, y):
        db = DragBlock()
        db.center = (x,y)
        ds.add_widget(db)
        ds.children = ds.children[::-1]