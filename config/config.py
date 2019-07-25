"""
Contains all the knobs for the whole project
"""

import os

home = os.path.expanduser("~")


class Config:
    def __init__(self):
        """Project configuration"""

        #Path Configurations
        self.project_root = os.path.join(home, 'Desktop/workspace/indeed/Job-Satisfaction')
        self.data_path = os.path.join(self.project_root, "data")
        self.company_path = os.path.join(self.data_path, "companies")
        self.analysis_path = os.path.join(self.project_root, "analysis")