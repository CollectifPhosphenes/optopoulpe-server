from dataclasses import dataclass
from typing import Optional

from orjson import orjson


def reduce_int(int_value: int, ratio: int):
    return int(float(int_value) / ratio)


@dataclass
class Effect:
    label: str
    enabled: Optional[bool] = None

    def set_attribute(self, key, value):
        return super().__setattr__(key, value)


@dataclass
class ColorPalette:
    selected_palette: Optional[int] = None
    width: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class ColorMod(Effect):
    color_palette: ColorPalette = None
    oscillator_track: Optional[int] = None

    def set_attribute(self, key, value):
        if key == "osc":
            if self.enabled:
                self.oscillator_track = reduce_int(value, 32)
            else:
                self.color_palette.offset = value
        elif key == "width":
            self.color_palette.width = value


@dataclass
class MaskMod(Effect):
    oscillator_track: Optional[int] = None
    length: Optional[int] = None
    is_move_enabled: Optional[bool] = None

    def set_attribute(self, key, value):
        if key == "osc":
            self.oscillator_track = reduce_int(value, 32)
        elif key == "width":
            self.length = value
        elif key == "move":
            self.is_move_enabled = value


@dataclass
class Slicer(Effect):
    uneven_value: Optional[int] = None  # Display on top knob if enabled = False
    slices_value: Optional[int] = None  # Display on bottom know if enabled = True

    # Currently not used
    is_flip_enabled: Optional[bool] = None
    is_ribbon_merge_enabled: Optional[bool] = None

    def set_attribute(self, key, value):
        if key == "nslices":
            self.slices_value = value
        elif key == "nuneven":
            self.uneven_value = value
        elif key == "useflip":
            self.is_flip_enabled = value
        elif key == "mergeribbon":
            self.is_ribbon_merge_enabled = value


@dataclass
class Feedback(Effect):
    value: Optional[int] = None

    def set_attribute(self, key, value):
        if key == "qty":
            self.value = value


@dataclass
class Strobe(Effect):
    pass


@dataclass
class Track:
    modulation: ColorMod
    mask: MaskMod
    slicer: Slicer
    feedback: Feedback
    strobe: Strobe

    index: Optional[int] = None

    slider_value: Optional[int] = None
    slider_max_enabled: Optional[bool] = None

    time_scale: Optional[int] = None

    is_on_group1: Optional[bool] = None
    is_on_group2: Optional[bool] = None
    is_on_group3: Optional[bool] = None


@dataclass
class GlobalState:
    tracks: dict[int, Track]
    current_selected_track_index: Optional[int] = None
    current_selected_track: Optional[Track] = None

    kill_all_tracks_enabled: Optional[bool] = None

    bpm: Optional[float] = None

    def json(self):
        return orjson.dumps(self)
