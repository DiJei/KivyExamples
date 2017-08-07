# File name: draggingblock.py
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle
from kivy.graphics import Color
from wifi import my_socket

class DragBlock(RelativeLayout):
    id = 0
    command_list = []
    def __init__(self,**kwargs):
        super(DragBlock, self).__init__(**kwargs)
        self.selected = True
        self.left_block = None

    def setId(self,id,source_photo):
        self.id = id
        self.command_list = [self.id]
        with self.canvas.before:
            Rectangle(source=source_photo, pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.left_block is not None:
                self.left_block.command_list = [self.left_block.id]
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
                        block.command_list = block.command_list + self.command_list
                        self.pos = self.left_block.x + self.left_block.width, self.left_block.y
                        left_block = True
            if left_block is not True:
                self.left_block = None
            self.selected = False
        elif self.left_block is not None:
            self.center = (self.left_block.center_x + self.left_block.width,self.left_block.center_y)
            self.left_block.command_list = [self.left_block.id] + self.command_list
        #Return default event for upper class
        return RelativeLayout.on_touch_up(self, touch)

    def checkRight(self,block,touch):
        if touch.x - (self.width/2) > block.x + (block.width/2) and touch.x - (self.width/2) < block.x  + block.width and self.y >= block.y and self.y <= block.y + block.height:
            return True
    def checkLeft(self,block,touch):
        if touch.x + (self.width/2) > block.x  and touch.x + (self.width/2) < block.x + (block.width/2) and self.y >= block.y and self.y <= block.y + block.height:
            return True

class DragPlayButton(DragBlock):
    command_list = {}
    data_list = []
    def __init__(self):
        DragBlock.__init__(self)
        self.play_button.bind(on_press=self.sendCommands)


    def checkRight(self,block,touch):
        return False

    def sendCommands(self,*args):
        self.data_list = self.command_list[1:]
        msg = ""
        for x in self.data_list:
            msg += str(x)
        my_socket.send_data(msg)
