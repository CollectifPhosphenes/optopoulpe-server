from datamodels import GlobalState, Track, ColorMod, MaskMod, Slicer, Feedback, Strobe, ColorPalette, reduce_int

STATE_MAPPING = {
    "do_kill_lights": "kill_all_tracks_enabled",
}

TRACKS_MAPPING = {
    "speed_scale": "time_scale",
    "is_active_on_master": "is_on_group1",
    "is_active_on_solo": "is_on_group2",
    "do_ignore_solo": "is_on_group3",
    "do_litmax": "slider_max_enabled",

    # "slider_value": "slider_value",
}

EFFECTS_MAPPING = {
    "colormod": "modulation",
    "maskmod": "mask",
    "slicer": "slicer",
    "feedback": "feedback",
    "strobe": "strobe",
}


def parse_dump_value(value: str):
    """
    Parse a value from the data dump file and return it as the correct type:
    - if "n" / "y" -> bool
    - elif Number with > chars -> float
    - else -> int
    """
    if value == "n":
        return False
    elif value == "y":
        return True
    elif len(value) > 3:
        return float(value)
    return int(value)


def parse_dump_file(file_path: str):
    with open(file_path) as file:
        lines = file.readlines()

    state = GlobalState(
        tracks={
            str(idx): Track(
                index=idx,
                modulation=ColorMod(label="Color Modulation", color_palette=ColorPalette()),
                mask=MaskMod(label="Mask"),
                slicer=Slicer(label="Uneven Slicer"),
                feedback=Feedback(label="Sustain"),
                strobe=Strobe(label="Strobe"),
            ) for idx in range(8)
        },
    )

    for line in lines:
        # Ignore all lines starting with solo, blur and sync (dead features)
        if line.startswith(("solo", "blur", "sync")):
            continue

        line = line.rstrip()

        parts = line.split(":")

        # Global state data
        if len(parts) == 1:
            attribute_name, attribute_value = parts[0].split(" ")
            setattr(
                state,
                STATE_MAPPING.get(attribute_name, attribute_name),
                parse_dump_value(attribute_value)
            )
            continue

        # Track state data
        attribute = parts[0]
        track_index, value = parts[1].split(" ")

        # Track palette data
        if attribute == "palette":
            setattr(
                state.tracks[track_index].modulation.color_palette,
                "selected_palette",
                reduce_int(parse_dump_value(value), 16)
            )
            continue

        # Track core data
        if attribute in TRACKS_MAPPING:
            setattr(
                state.tracks[track_index],
                TRACKS_MAPPING[attribute],
                parse_dump_value(value)
            )
            continue

        # Effect data
        if attribute.startswith(tuple(EFFECTS_MAPPING.keys())):
            fx_name, fx_attribute = attribute.split("_")

            # Enabled toggle
            if fx_attribute in ("enable", "useuneven"):
                effect = getattr(state.tracks[track_index], EFFECTS_MAPPING.get(fx_name, fx_name))
                effect.enabled = parse_dump_value(value)
                setattr(
                    state.tracks[track_index],
                    EFFECTS_MAPPING.get(fx_name, fx_name),
                    effect,
                )
                continue

            # Effect attribute
            getattr(
                state.tracks[track_index], EFFECTS_MAPPING.get(fx_name, fx_name)
            ).set_attribute(fx_attribute, parse_dump_value(value))

    return state
