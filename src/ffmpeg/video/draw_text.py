class FFmPegDrawText:
    def __init__(self):
        self.commands: list = []

    def font_file(self, file):
        self.commands.append(f"fontfile={file}")
        return self

    def text(self, text):
        self.commands.append(f"text={text}")
        return self

    def font_size(self, size):
        self.commands.append(f"fontsize={size}")
        return self

    def font_color(self, color):
        self.commands.append(f"fontcolor={color}")
        return self

    def enable_box(self):
        self.commands.append(f"box=1")
        return self

    def box_color(self, color, transparency):
        self.commands.append(f"boxcolor={color}@{transparency}")
        return self

    def border_width(self, width):
        self.commands.append(f"boxborderw={width}")
        return self

    def duration(self, value):
        self.commands.append(f"duration={value}")

    def position(self, pos, padding):
        if pos == 'top_right':
            x = "(w-text_w)"
            y = "0"

        elif pos == 'bottom_left':
            x = "0"
            y = "(h-text_h)"

        elif pos == 'bottom_right':
            x = "(w-text_w)"
            y = "(h-text_h)"

        elif pos == 'centre':
            x = "(w-text_w)/2"
            y = "(h-text_h)/2"

        else:
            # resetting coordinates for top left
            x = "0"
            y = "0"

        x = f"{x}-{padding}" if x != "0" else f"{padding}"
        y = f"{y}-{padding}" if y != "0" else f"{padding}"

        self.commands.append(f"x={x}:y={y}")
        return self

    def enable_after(self, value: int = None, duration: int = None):
        """
        The value will be in seconds in integer type
        :param value:
        :type value:
        :param duration:
        :type duration:
        :return:
        :rtype:
        """
        if duration:
            self.commands.append(f"enable='between(t,{value}, {duration})'") # start and end at given time
        else:
            self.commands.append(f"enable='gte(t,{value})'") # start after time and till the end
        return self

    def repeat(self, time: int):
        self.commands.append(f"enable='mod(t,{time*2})<{time}'")
        return self

    def flux(self):
        return "drawtext=" + ":".join(self.commands)

def generate_filter_string(text, font_file, font_color=None, font_size=None, position=None, padding=None, enable_box=None, box_color=None, border_width=None, transparency=None, start_after=None, repeat=None, duration=None):
    tObj = FFmPegDrawText()
    tObj.font_file(font_file).text(text).font_color(font_color).font_size(font_size)

    if enable_box:
        tObj.enable_box()

    tObj.box_color(box_color, transparency).border_width(border_width).position(position, padding)

    if start_after:
        tObj.enable_after(start_after, duration)

    elif repeat:
        tObj.repeat(repeat)

    return tObj.flux()
