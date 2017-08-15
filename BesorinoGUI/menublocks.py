# File name: menublocks.py
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
from draggingblock import DragBlock
from draggingblock import DragPlayButton

import json

#Tab
class BlocksMenu(TabbedPanel):
    def __init__(self, **kwargs):
        super(BlocksMenu,self).__init__(**kwargs)
        self.buildTab()

    def buildTab(self):
        self.background_image = "images/block_tab_background.png"
        with open("config/blocks.json") as json_data:
            blocks_config = json.load(json_data)
            for tab in blocks_config["tabs"]:
                newTab = TabbedPanelItem(text = str(tab["id"]))
                color_tab = []
                for color in tab["rgba"]:
                    color_tab.append(color)
                newTab.background_color = color_tab
                newLayout = StackLayout()
                for block in tab["blocks"]:
                    newBlock = Block(int(block["id"]),str(block["source"]))
                    newLayout.add_widget(newBlock)
                newTab.content = newLayout
                self.add_widget(newTab)


class Block(RelativeLayout):
    def __init__(self,id,source_image,**kwargs):
        super(Block,self).__init__(**kwargs)
        self.blockID = id
        self.source_image = source_image
        self.da = None
        self.bind(pos=self.update)
        self.bind(size=self.update)
        with self.canvas:
            self.rect = Rectangle(size = self.size, source = self.source_image)


    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.da = self.parent.parent.parent.drawing_area
            (x,y) = self.da.to_widget(touch.x, touch.y)
            if self.blockID != 0:
                self.draw(self.da, x, y,self.blockID,self.source_image)
            else:
                self.drawPlay(self.da, x, y,self.blockID,self.source_image)
            return True
        return super(Block,self).on_touch_down(touch)

    def update(self, *args):
        self.size = (self.parent.height,self.parent.height)
        self.rect.size = (self.parent.height,self.parent.height)

    def draw(self, da, x, y,id,source):
        db = DragBlock(id,source)
        db.center = (x,y)
        da.add_widget(db)
        da.children = da.children[::-1]

    def drawPlay(self, da, x, y,id,source):
        db = DragPlayButton(id,source)
        db.center = (x,y)
        da.add_widget(db)
        da.children = da.children[::-1]
