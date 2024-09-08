from datetime import datetime

class Vehicle:
    def __init__(self):
        self.post_date = ""
        self.file_date = ""
        self.plate = "uknown"
        self.sheet_date = ""
        self.sheet_time = ""
        self.speed = 0
        self.speed_units = ""
        self.street_name = ""
        self.direction = ""

    def reset(self):
        self.post_date = ""
        self.file_date = ""
        self.plate = "uknown"
        self.sheet_date = ""
        self.sheet_time = ""
        self.speed = 0
        # self.speed_units is set once during initialization
        # self.street_name is set once during initialization
        self.direction = ""

    def set_date(self):
        dt = datetime.now()
        self.post_date = dt.strftime('%A %B %d, %Y at %H:%M')
        self.file_date = dt.strftime("%Y%m%d-%H%M%S")
        self.sheet_date = dt.strftime('%Y-%m-%d')
        self.sheet_time = dt.strftime('%H:%M:%S')
    