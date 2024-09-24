__all__ = ["generate_filter_string"]

class FFMPegFilterBuilder:
    def __init__(self):
        self.commands = []
        self.sub_filters = []

    def filter_in(self, value):
        self.commands.append(f"[{value}]")
        return self

    def format_filter(self, format_type='rgba'):
        self.sub_filters.append(f"format={format_type}")
        return self

    def scale2ref(self, scale_factor=0.2):
        self.sub_filters.append(f"scale2ref=oh*mdar:ih*{scale_factor}")
        return self

    def overlay(self, x,y):
        self.sub_filters.append(f"overlay={x}:{y}")
        return self

    def color_channel_mixer(self, alpha):
        self.sub_filters.append(f"colorchannelmixer=aa={alpha}")
        return self

    def _setter(self):
        if self.sub_filters:
            self.commands.append(",".join(self.sub_filters))
            self.sub_filters = []

    def filter_out(self, output_stream):
        self._setter()
        self.commands.append(f"[{output_stream}]")
        return self

    def build(self):
        self._setter()
        return "".join(self.commands)

    def reset(self):
        self.commands = []
        self.sub_filters = []

    def flux(self):
        self.commands.append(";")
        return self



def overlay_coordinates(position: str, padding: int) -> tuple[str, str]:
    x: str = ""
    y: str = ""

    if position == 'top_right':
        x = "(main_w-overlay_w)"
        y = "0"

    elif position == 'bottom_left':
        x = "0"
        y = "(main_h-overlay_h)"

    elif position == 'bottom_right':
        x = "(main_w-overlay_w)"
        y = "(main_h-overlay_h)"

    elif position == 'centre':
        x = "(main_w-overlay_w)/2"
        y = "(main_h-overlay_h)/2"
    else:
        x = "0"
        y = "0"

    if padding:
        x = f"{x}-{str(padding)}" if x != "0" else str(padding)
        y = f"{y}-{str(padding)}" if y != "0" else str(padding)

    return x, y


def generate_filter_string(scale_factor, position, padding, transparency) -> str:

    x_coordinate, y_coordinate = overlay_coordinates(position, padding)

    fObj = FFMPegFilterBuilder()
    fObj.filter_in(1).format_filter('rgba').color_channel_mixer(alpha=transparency).filter_out('logo').flux()
    fObj.filter_in('logo').filter_in('0').scale2ref(scale_factor).filter_out("logo").filter_out('video').flux()
    fObj.filter_in('video').filter_in('logo').overlay(x_coordinate, y_coordinate)

    return fObj.build()
