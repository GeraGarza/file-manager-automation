from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import os
import json
import time

folder_destination = "C:/Users/Gera/Videos"
ext = ".mp4"
changed_name = f"video_"
i = 0
max_wait = 1


def transfer_video(filename):
    if ext not in filename:
        return

    new_name = f"{changed_name}1{ext}"
    if ".crdownload" in filename:
        filename = filename.split(".crdownload")[0]
        j = 0
        print("downloading",end="")

        while (not os.path.exists(filename)) or max_wait > j:
            time.sleep(1)
            j += 1
            print(".", end="")
        print("")

        if j >= max_wait:
            return

    file_exists = os.path.isfile(f"{folder_destination}/{new_name}")
    print(new_name)
    while file_exists:
        global i
        i += 1
        new_name = f"{changed_name}{i}{ext}"
        file_exists = os.path.isfile(f"{folder_destination}/{new_name}")

    new_destination = folder_destination + "/" + new_name
    os.rename(filename, new_destination)


def on_created(event):
    filename = event.src_path[2:]
    print(f"created: {filename}")
    transfer_video(filename)


def on_deleted(event):
    print(f"deleted: {event.src_path}!")


def on_modified(event):
    filename = event.src_path[2:]
    print(f"modified: {filename}")
    transfer_video(filename)


def on_moved(event):
    filename = event.src_path[2:]
    new_file_name = event.dest_path[2:]
    print(f"moved: {filename} to {new_file_name}")


if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
