from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder

# You could also put the following in your kv file...
kv = '''
<DragLabel>:
    # Define the properties for the DragLabel
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0

FloatLayout:
    # Define the root widget
    DragLabel:
        canvas:
            Color:
                rgb: 1,1,0
            Rectangle:
                size: root.height * 0.25,root.height * 0.25
'''

class DragLabel(DragBehavior, RelativeLayout):
    pass


class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()