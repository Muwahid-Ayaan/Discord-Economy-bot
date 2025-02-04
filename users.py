from datetime import datetime, timedelta

class User_data:
    def __init__(self,user_id):
        self.Stars = 0
        self.Stars_in_bank = 0
        self.last_work = datetime(2022, 11, 20, 12, 30)
        self.last_rob = datetime(2022, 11, 20, 12, 30)
        self.last_beg = datetime(2022, 11, 20, 12, 30)
        self.last_heist = datetime(2022,11,20,12,30)
    def reset(self):
        self.Stars = 0
        self.Stars_in_bank = 0
        self.last_work = datetime(2022, 11, 20, 12, 30)
        self.last_rob = datetime(2022, 11, 20, 12, 30)
        self.last_beg = datetime(2022, 11, 20, 12, 30)
        self.last_heist = datetime(2022,11,20,12,30)