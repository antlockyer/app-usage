import time
import win32gui
from pymongo import MongoClient

# MongoDB connection settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'focused_app_logs'
MONGO_COLLECTION = 'app_usage'

# Initialize MongoDB client and collection
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Function to get the currently focused application's title
def get_focused_application():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return title

# Function to log the time spent on the focused application
def log_time_spent():
    previous_app = None
    start_time = time.time()

    while True:
        try:
            current_app = get_focused_application()

            if current_app != previous_app:
                if previous_app:
                    end_time = time.time()
                    time_spent = end_time - start_time

                    # Log the time spent on the previous application
                    log_entry = {
                        'application': previous_app,
                        'time_spent': time_spent
                    }

                    # If the application is Chrome, also log the website being visited
                    if previous_app.lower() == 'google chrome':
                        active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                        if active_window.startswith('Google Chrome'):
                            log_entry['website'] = active_window

                    collection.insert_one(log_entry)

                start_time = time.time()
                previous_app = current_app

            time.sleep(5)  # Check every 5 seconds

        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    log_time_spent()