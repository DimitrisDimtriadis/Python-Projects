from enum import Enum

class LogProfiles(Enum):
    D = "Development"
    P = "Production"

class appsettings:
    # EMAIL CONFIG
    EMAIL_FILE_PATH = "Modules/rawFiles/data.csv"
    EMAIL_MESSAGE_PATH = "Modules/rawFiles/message.txt"
    
    # LOGGER CONFIG
    LOGGER_ACTIVE_PROFILE=LogProfiles.D
    LOGGER_FILES_PATH="E:\\SourceTree\WatchDog\\Modules\\rawFiles"
    LOGGER_FILE_MAX_SIZE=-1

    # CREATE MSG CONFIG
    MSG_SUB_TITLE="<div>Hey, see what's new today!</div>"
    MSG_MAIN_BODY_TEMPLATE='''<div id="image" style="display:inline-block; margin:20px; width:100%%; "><img style="font-size: 14px; float: left; margin-right: 10px;" src="%s" width="60" />
    <p style="float: left;">%s <br /><span style="font-size: 8px;">IMDB: </span>%s</p>
    </div>'''

    # DATABASE CONFIG
    DB_FILE_PATH="Modules/rawFiles/watchDogDB.sqlite"

    # WATCHDOG CONFIG
    APP_MOVIES_URL='https://www.subs4free.club/'
    APP_MOVIES_TABLE='MoviesTb'