'''
Referenced from http://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes
'''
import time;
import os;
from watchdog.observers import Observer;
from watchdog.events import FileSystemEventHandler;
from config import DIRECTORY_TO_BE_MONITORED;
from fileupload import FileUpload;
import sys

class FileAddedEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        input = sys.argv[1];
        after_file_list = os.listdir(DIRECTORY_TO_BE_MONITORED);
        file_added = [f for f in after_file_list if not f in self.before_file_list];
        file_path = os.path.join(DIRECTORY_TO_BE_MONITORED, file_added.__getitem__(0));
        file_upload = FileUpload();
        if input == "encrypted":
            file_upload.upload_file_to_cloud(file_path, True);
        else:
            file_upload.upload_file_to_cloud(file_path, False);
        self.before_file_list = after_file_list;
        
    def initialize(self):
        self.before_file_list = os.listdir(DIRECTORY_TO_BE_MONITORED);

if __name__=="__main__":
    directory_event_handler = FileAddedEventHandler();
    directory_event_handler.initialize();
    directory_observer = Observer();
    directory_observer.schedule(directory_event_handler, path=DIRECTORY_TO_BE_MONITORED, recursive=False);
    directory_observer.start();
    
    try:
        while True:
            time.sleep(1);
    except KeyboardInterrupt:
        directory_observer.stop();
    directory_observer.join();