import shutil, os, glob
import pandas as pd
from datetime import datetime, timedelta
import requests
# from package import createPPT as cp

class DOSOMETHING():
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        
    def copy2backup(self, path1, path2, backupPath):
        backupTime = datetime.now().strftime('%Y%m%d%H%M%S')
        if os.path.exists(path1):
            file1 = path1.split('\\')[-1]
            shutil.copyfile(f'{path1}', f"{backupPath}\{backupTime}_{file1}")
            self.writeLog('BACKUP', path1, backupPath)
            fileCount = glob.glob(f"{backupPath}\*_{file1}")
            if len(fileCount)>10:
                list(map(lambda x: os.remove(x), fileCount[:-10]))
        if os.path.exists(path2):
            file2 = path2.split('\\')[-1]
            shutil.copyfile(f'{path2}', f"{backupPath}\{backupTime}_{file2}")
            self.writeLog('BACKUP', path2, backupPath)
            fileCount = glob.glob(f"{backupPath}\*_{file2}")
            if len(fileCount)>10:
                list(map(lambda x: os.remove(x), fileCount[:-10])) 
        return 1

    def api_load_data_forTest(self, children, data):
        api_urls = f'http://192.168.56.1:8005/streamlit/{children}'
        req = requests.post(api_urls, json = data)
        if req.status_code == 404:
            self.writeLog('API', 'FAIL', children)
            return pd.DataFrame()#req.content
        else:
            result = req.json()
            if len(result) == 1 and 'result' in result:
                return result['result']
            else:
                return pd.DataFrame(req.json())