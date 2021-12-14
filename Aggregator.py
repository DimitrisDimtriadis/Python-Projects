import sys
from Modules.AppSettings import appsettings
sys.path.insert(0, appsettings.APP_MODULES_PATH)

import Modules.MoviesWatchDog as mWd
import Modules.CreateMessage as cMsg
import Modules.EmailTool as eT

if __name__ == "__main__":
    # Download the data and place them to DB
    mWd.main()
    # Create the message based on last data
    cMsg.createTxtMessage()
    # Send the data to recipients
    eT.main()
    # Mark data as seen
    cMsg.updateDataInDB()
    # Clean message txt
    cMsg.cleanTxtMessage()
