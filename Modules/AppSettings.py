from enum import Enum

class LogProfiles(Enum):
    D = "Development"
    P = "Production"

class appsettings:
    # EMAIL CONFIG
    EMAIL_FILE_PATH = "rawFiles/data.csv"
    EMAIL_MESSAGE_PATH = "rawFiles/message.txt"
    
    # LOGGER CONFIG
    LOGGER_ACTIVE_PROFILE=LogProfiles.D
    LOGGER_FILES_PATH="E:\\SourceTree\WatchDog\\rawFiles"
    LOGGER_FILE_MAX_SIZE=-1