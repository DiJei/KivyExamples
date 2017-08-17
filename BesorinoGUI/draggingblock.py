# File name: draggingblock.py
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.core.audio import SoundLoader
from wifi import my_socket

play_sound_fail = SoundLoader.load('sounds/start_fail.wav')
play_sound_succes = SoundLoader.load('sounds/start_succes.wav')
connect_sound = SoundLoader.load('sounds/connect.mp3')
click_sound = SoundLoader.load('sounds/touch.wav')
erase_sound = SoundLoader.load('sounds/erase.wav')

class DragBlock(RelativeLayout):
    id = 0
    command_list = []
    def __init__(self,id,source_photo,**kwargs):
        super(DragBlock, self).__init__(**kwargs)
        self.selected = True
        self.left_block = None
        self.id = id
        self.command_list = [self.id]
        self.bind(pos=self.update)
        self.bind(size=self.update)
        with self.canvas:
            self.rect = Rectangle(source=source_photo, pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.left_block is not None:
                self.left_block.command_list = [self.left_block.id]
            self.left_block = None
            self.selected = True
            click_sound.play()
            return True

    def on_touch_move(self, touch):
        if self.selected:
            for block in self.parent.children:
                if block is self:
                    self.center = (touch.x,touch.y)
                elif block.left_block is not None :
                    block.center = (block.left_block.center_x + block.left_block.width,block.left_block.center_y)
        return RelativeLayout.on_touch_up(self, touch)

    def on_touch_up(self, touch):
        if (self.selected):
            menu_block = self.parent.block_menu
            #Delete the DragBlock
            if menu_block.collide_point(touch.x, touch.y):
                self.parent.remove_widget(self)
                erase_sound.play()
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
                        connect_sound.play()
                    elif block.left_block is not None:
                        block.center = (block.left_block.center_x + block.left_block.width,block.left_block.center_y)
                        block.left_block.command_list = [block.left_block.id] + block.command_list
            if left_block is not True:
                self.left_block = None
            self.selected = False
            return True
        #Return default event for upper class
        return RelativeLayout.on_touch_up(self, touch)

    def update(self, *args):
        self.rect.size = (self.size)

    def checkRight(self,block,touch):
        if self.x > block.x + (block.width/2) and self.x < block.x  + block.width and self.y >= block.y and self.y <= block.y + block.height:
            return True
    def checkLeft(self,block,touch):
        if self.x + self.width > block.x  and self.x + self.width < block.x + (block.width/2) and self.y >= block.y and self.y <= block.y + block.height:
            return True

class DragPlayButton(DragBlock):
    command_list = {}
    data_list = []

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.checkCenter(touch):
                self.sendCommands()
            if self.left_block is not None:
                self.left_block.command_list = [self.left_block.id]
            self.left_block = None
            self.selected = True
            return True

    def checkRight(self,block,touch):
        return False

    def sendCommands(self):
        my_socket.connect()
        self.data_list = self.command_list[1:]
        msg = ""
        for x in self.data_list:
            msg += str(x)
        if my_socket.send_data(msg):
            play_sound_fail.play()
        else:
            play_sound_succes.play()

    def checkCenter(self,touch):
        if touch.x > self.x + self.width*0.70 or touch.x < self.x + self.width*0.30:
            return False
        if touch.y > self.y + self.height*0.70 or touch.y < self.y + self.height*0.30:
            return False
        return True
