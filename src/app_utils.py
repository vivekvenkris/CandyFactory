from exceptions import IncorrectStatusException

def ensure_correct_processing_status(status, reqd_status):
        if(status < reqd_status):
            IncorrectStatusException("Current processing status={} < required={}, aborting. ".format(status, reqd_status))

        elif(status > reqd_status):
            IncorrectStatusException("Current processing status={} >  required={}, skipping. ".format(status, reqd_status))