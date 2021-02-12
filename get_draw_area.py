from pymouse import PyMouseEvent

def get_draw_area():

    class ListenInterrupt(Exception):
        pass

    class get_draw_area_handler(PyMouseEvent):
        def __init__(self):
            PyMouseEvent.__init__(self)
            self.top_left = False
            self.bottom_right = False
            print("Click the top left corner of the area to draw in..")

        def click(self, x, y, button, press):
            '''Print Fibonacci numbers when the left click is pressed.'''
            if button == 1:
                if press:
                    if not self.top_left:
                        print("Top left is:", (x, y))
                        self.top_left = (x, y)
                        print("Now click the bottom right..")
                    elif not self.bottom_right:
                        print("Bottom right is:", (x, y))
                        self.bottom_right = (x, y)
                        raise ListenInterrupt("Calibrated.")
                    # print(x, y, button, press)
            else:  # Exit if any other mouse button used
                raise ListenInterrupt("Calibrated.")

    draw_area_clicker = get_draw_area_handler()
    try:
        draw_area_clicker.run()
    except ListenInterrupt as e:
        print(e.args[0])

    return draw_area_clicker.top_left, draw_area_clicker.bottom_right


