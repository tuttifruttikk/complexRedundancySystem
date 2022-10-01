class RepairTeam:
    def __init__(self):
        self.status = True
        self.ending = 0
        self.repair_num = 5

    def start_repairing(self, s, e, n):
        self.status = s
        self.ending = e
        self.repair_num = n

    def free(self):
        self.status = True
        self.ending = 0
        self.repair_num = 5
