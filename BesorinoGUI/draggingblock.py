# File name: draggingblock.py
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color

class DragBlock(RelativeLayout):
    selected = None
    def __init__(self,**kwargs):
        super(DragBlock, self).__init__(**kwargs)
        self.selected = True
        self.left_block = None
        self.event = None
        with self.canvas:
            Color(1, 0, 0, 1)  # set the color to red
                           
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.left_block = None
            self.selected = True
        elif self.left_block is not None :
            self.center = (self.left_block.center_x + self.left_block.width,self.left_block.center_y)
        return RelativeLayout.on_touch_down(self, touch)        
    
    def on_touch_move(self, touch):
        if self.selected:
            self.center = (touch.x,touch.y)
        elif self.left_block is not None :
            self.center = (self.left_block.center_x + self.left_block.width,self.left_block.center_y)
        return RelativeLayout.on_touch_move(self, touch)
    
    def on_touch_up(self, touch):
        if (self.selected):
            trash_can = self.parent.trash_can
            #Delete the DragBlock
            if trash_can.collide_point(touch.x, touch.y):
                self.parent.remove_widget(self)
                return True
            #Connect Blocks
            left_block = False             
            for block in self.parent.children:
                if block is not self:
                    if self.checkLeft(block,touch):
                        block.left_block = self
                        self.pos = block.x - block.width, block.y
                    elif self.checkRight(block, touch):
                        self.left_block = block
                        self.pos = self.left_block.x + self.left_block.width, self.left_block.y
                        left_block = True
            if left_block is not True:
                self.left_block = None          
            self.selected = False
        elif self.left_block is not None:
            self.center = (self.left_block.center_x + self.left_block.width,self.left_block.center_y)
        #Return default event for upper class   
        return RelativeLayout.on_touch_up(self, touch)
    
    def checkRight(self,block,touch):
        if touch.x - (self.width/2) > block.x + (block.width/2) and touch.x - (self.width/2) < block.x  + block.width and self.y >= block.y and self.y <= block.y + block.height:
            return True
    def checkLeft(self,block,touch):
        if touch.x + (self.width/2) > block.x  and touch.x + (self.width/2) < block.x + (block.width/2) and self.y >= block.y and self.y <= block.y + block.height:
            return True