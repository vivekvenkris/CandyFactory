import argparse
from rfi_utils import RFIUtils

from constants import STATUS_DICT

def get_args():
    argparser = argparse.ArgumentParser(description="Excise RFI using PulsarX zero DM matched filter, and generate dynamic birdie list / zap mask for peasoup search")
    argparser.add_argument("-config", dest="config", help="configuration file")
    argparser.add_argument("-verbose", dest="verbose", help="Enable verbose terminal logging", action="store_true")
    argparser.add_argument("-beam_num", dest="beam_num", help="beam number to process")
    argparser.add_argument("-ledger_file", dest="ledger_file", help="ledger_file")
    args = argparser.parse_args()
    return args




def main():


	level = logging.WARN
	args = get_args()

	if(args.verbose):
		level = logging.DEBUG

	#inititalise logger
	logger = init_logging(file_name="{}_{}.log".format(args.log_file_prefix,(datetime.datetime.now()).strftime("%Y-%m-%d-%H:%M:%S")), file_level=level)

	#initialise config read
 	if args.config_file is not None and os.path.isfile(args.config_file):
 	    config = parse_config(args.config_file)
   else:
        logger.warning("Config file not provided or incorrect. Proceeding with default")

    ledger = Ledger() is args.ledger_file is None else Ledger()

    status = ledger.get_status(args.beam_num)

    if(status < STATUS_DICT['02_RSYNC_2']):
        logger.fatal("Processing status {} < {}, aborting. ".format(status, STATUS_DICT['RSYNC_2']) )
        exit(1)

    elif
    if(status >= STATUS_DICT['02_RSYNC_2']):
        logger.fatal("Processing status {} > {}, skipping. ".format(status, STATUS_DICT['RSYNC_2']) )
        exit(0)


    rfi_utils = RFIUtils(config.presto_config.singularity_image,
                    config.presto_config.singularity_flags, ledger)



    rfi_utils.do_zero_dm_filter()

    rfi_utils.do_rfifind()



    rfi_utils.do_accelsearch()




    #update ledger
