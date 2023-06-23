__author__ = "reed@reedjones.me"

import os
import subprocess
import time

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer


class Watcher:
    DIRECTORY_TO_WATCH: str

    def __init__(self, d):
        self.DIRECTORY_TO_WATCH = d
        self.observer = Observer()

    def run(self):
        print(f"Watching {self.DIRECTORY_TO_WATCH} \n cwd: {os.getcwd()}")
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            print(e)

        self.observer.join()


def run_command(working_dir, cmd):
    print(f"Running cmd {cmd} in {working_dir}")
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=working_dir,
                               shell=True)
    stdout, stderr = process.communicate()
    if stderr:
        print(stderr)
        exit(1)
    print(stdout)
    return stdout


class Handler(FileSystemEventHandler):
    cmd = ["python", "drupan/drupan.py", "config.yaml"]
    working_dir = "C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog"

    def __init__(self, *args, **kwargs):
        self.running = False

    def run_command(self):
        print("hello")
        try:
            if self.running:
                print("Got command but running so won't do anything....")
                return
            self.running = True
            out = run_command(self.working_dir, self.cmd)
            self.running = False
            return out
        except KeyboardInterrupt:
            print(f"Leaving")
            exit(0)

    def on_any_event(self, event: FileSystemEvent):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            self.run_command()


        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)
            self.run_command()


if __name__ == '__main__':
    w = Watcher("C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog\\content")
    w.run()
