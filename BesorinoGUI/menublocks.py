# File name: menublocks.py
from kivy.uix.relativelayout import RelativeLayout
from draggingblock import DragBlock
from draggingblock import DragPlayButton

#Super Class Block
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
        pass

#Each Block
class ForwardBlock(Block):
    def draw(self, ds, x, y):
        db = DragBlock()
        db.setId(1,"images/forward.png")
        db.center = (x,y)
        ds.add_widget(db)
        ds.children = ds.children[::-1]

class ReverseBlock(Block):
    def draw(self, ds, x, y):
        db = DragBlock()
        db.setId(2,"images/reverse.png")
        db.center = (x,y)
        ds.add_widget(db)
        ds.children = ds.children[::-1]

class TurnRightBlock(Block):
    def draw(self, ds, x, y):
        db = DragBlock()
        db.setId(3,"images/turn_right.png")
        db.center = (x,y)
        ds.add_widget(db)
        ds.children = ds.children[::-1]

class TurnLeftBlock(Block):
    def draw(self, ds, x, y):
        db = DragBlock()
        db.setId(4,"images/turn_left.png")
        db.center = (x,y)
        ds.add_widget(db)
        ds.children = ds.children[::-1]

class PlayBlock(Block):
    def draw(self, ds, x, y):
        db = DragPlayButton()
        db.setId(0,"images/playicon.png")
        db.center = (x,y)
        ds.add_widget(db)
        ds.children = ds.children[::-1]
