from enum import Enum

class LogProfiles(Enum):
    D = "Development"
    P = "Production"

class appsettings:
    
    # WATCHDOG CONFIG
    
    # For Windows
    # APP_MODULES_PATH = 'E:\\SourceTree\\WatchDog\\Modules'
    # EMAIL_FILE_PATH = APP_MODULES_PATH + "\\rawFiles\\emailConfig.csv"
    # EMAIL_MESSAGE_PATH = APP_MODULES_PATH + "\\rawFiles\\message.txt"
    # LOGGER_FILES_PATH = APP_MODULES_PATH + "\\rawFiles"
    # APP_MOVIES_CSV_PATH = APP_MODULES_PATH + '\\rawFiles\\movies.csv'
    
    # For Ubuntu
    # APP_MODULES_PATH = '/home/pi/WatchDog/Modules'
    # EMAIL_FILE_PATH = APP_MODULES_PATH + "/rawFiles/emailConfig.csv"
    # EMAIL_MESSAGE_PATH = APP_MODULES_PATH + "/rawFiles/message.txt" 
    # LOGGER_FILES_PATH = APP_MODULES_PATH + "/rawFiles"
    # APP_MOVIES_CSV_PATH = APP_MODULES_PATH + '/rawFiles/movies.csv'

    # For Test
    APP_MODULES_PATH = '/Users/dimitriosdimitriadis/Fork/WatchDog/Modules'
    EMAIL_FILE_PATH = APP_MODULES_PATH + "/rawFiles/emailConfig.csv"
    EMAIL_MESSAGE_PATH = APP_MODULES_PATH + "/rawFiles/message.txt" 
    LOGGER_FILES_PATH = APP_MODULES_PATH + "/rawFiles"
    APP_MOVIES_CSV_PATH = APP_MODULES_PATH + '/rawFiles/movies.csv'
    
    # About movies
    APP_MOVIES_URL = 'https://www.subs4free.club/'
    
    # LOGGER CONFIG
    LOGGER_ACTIVE_PROFILE = LogProfiles.D
    LOGGER_FILE_MAX_SIZE = -1

    # CREATE MSG CONFIG
    MSG_SUB_TITLE = "<div>Hey, see what's new today!</div>"
    MSG_MAIN_BODY_TEMPLATE = '''<div id="image" style="display:inline-block; margin:20px; width:100%%; "><img style="font-size: 14px; float: left; margin-right: 10px;" src="%s" width="60" />
    <p style="float: left;">%s <br /><span style="font-size: 8px;">IMDB: </span>%s</p>
    </div>'''