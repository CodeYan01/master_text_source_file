"""
@author: CodeYan
"""
import obspython as obs
import os
import re

# Script Data
file_path = ""
file_check_delay = 0
previous_missing_file = "" # If the file is still not found, don't log it again
previous_found_file = ""
previous_mtime = None
previous_missing_sources = set()
source_name_re = re.compile(r"^\s*<(.*)>\s*$")
update_when_changed = False

def script_properties():
    """Adds script options that the user can edit"""
    # global obs_props
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, "file_path", "File Path: ", obs.OBS_PATH_FILE, "*.txt", "")
    obs.obs_properties_add_int(props, "file_check_delay", "Check delay (ms):", 50, 2**31-1, 100)
    obs.obs_properties_add_bool(props, "update_when_changed", "Only update sources when file is modified")

    return props

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "file_check_delay", 1000)
    obs.obs_data_set_default_bool(settings, "update_when_changed", True)

def script_update(settings):
    global file_path
    global file_check_delay
    global update_when_changed
    global previous_mtime

    new_file_path = obs.obs_data_get_string(settings, "file_path")
    new_file_check_delay = obs.obs_data_get_int(settings, "file_check_delay")
    update_when_changed = obs.obs_data_get_bool(settings, "update_when_changed")

    if not update_when_changed:
        previous_mtime = None

    if file_path != new_file_path:
        file_path = new_file_path
        read_file()
    if file_check_delay != new_file_check_delay and new_file_check_delay > 0:
        file_check_delay = new_file_check_delay
        obs.timer_remove(read_file)
        obs.timer_add(read_file, file_check_delay)

def read_file():
    _read_file(file_path)

def _read_file(file_path: str):
    global previous_missing_file
    global previous_found_file
    global previous_mtime

    if not file_path:
        return
    try:
        if update_when_changed:
            mtime = os.stat(file_path).st_mtime
            if mtime == previous_mtime:
                return
            previous_mtime = mtime

        with open(file_path, mode='r') as f:
            previous_missing_file = ""
            if previous_found_file != file_path:
                print(f"Found file '{file_path}'")
                previous_found_file = file_path
            source = None
            text_lines = []
            for line in f:
                match = source_name_re.match(line)
                if match:
                    if source:
                        # Text sources are only updated once another source name
                        # is read, as the lines are accumulated in text_lines
                        # first.
                        set_source_text(source, join_text_lines(text_lines))
                        obs.obs_source_release(source)
                    text_lines = []

                    source_name = match[1]
                    source = obs.obs_get_source_by_name(source_name)
                    if source is None:
                        if source_name not in previous_missing_sources:
                            print(f"Source '{source_name}' not found.")
                            previous_missing_sources.add(source_name)
                    elif source_name in previous_missing_sources:
                        print(f"Found source '{source_name}'")
                        previous_missing_sources.remove(source_name)
                else:
                    text_lines.append(line.rstrip('\n'))

            # For last scene
            if source:
                set_source_text(source, join_text_lines(text_lines))
                obs.obs_source_release(source)
    except FileNotFoundError as e:
        # Print once per missing file to avoid spam
        if previous_missing_file != file_path:
            print(e)
            previous_missing_file = file_path
            previous_found_file = ""
            previous_mtime = None

def join_text_lines(lines: list):
    if len(lines) > 0 and lines[-1] == '':
        lines.pop()
    return "\n".join(lines)

def set_source_text(source, text):
    source_settings = obs.obs_source_get_settings(source)
    old_text = obs.obs_data_get_string(source_settings, "text")
    if text != old_text:
        obs.obs_data_set_string(source_settings, "text", text)
        obs.obs_source_update(source, source_settings)
    obs.obs_data_release(source_settings)
