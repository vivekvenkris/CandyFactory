import argparse
from rfi_utils import RFIUtils

from constants import STATUS_DICT,StatusManager

def get_args():
    argparser = argparse.ArgumentParser(description="Excise RFI using PulsarX zero DM matched filter, and generate dynamic birdie list / zap mask for peasoup search")
    argparser.add_argument("-config", dest="config", help="configuration file")
    argparser.add_argument("-verbose", dest="verbose", help="Enable verbose terminal logging", action="store_true")
    argparser.add_argument("-beam_num", dest="beam_num", help="beam number to process")
    argparser.add_argument("-log_file_prefix", dest="log_file_prefix", help="Name of log file",default="candyfactory")
    argparser.add_argument("-ledger_file", dest="ledger_file", help="ledger_file")
    args = argparser.parse_args()
    return args


def main(args):

    args = get_args()    
    logger = init_logging(file_name="{}_{}.log".format(args.log_file_prefix,(datetime.datetime.now()).strftime("%Y-%m-%d-%H:%M:%S")),
                             file_level=logging.DEBUG if args.verbose else None)
    config = parse_config(args.config_file)
    ledger = Ledger() is args.ledger_file is None else Ledger()

    logger.info("Using the following Ledger file: {}", ledger_file)

    status = ledger.get_status(args.beam_num)
    ensure_correct_processing_status(status,StatusManager.RSYNC_TO_PROCESSING)


    rfi_utils = RFIUtils(config.presto_config.singularity_image,
                    config.presto_config.singularity_flags, ledger)

    rfi_utils.run_filtool()
    self.ledger.update_status(i,StatusManager.FILTOOLS )


    rfi_utils.run_rfifind()
    self.ledger.update_status(i, StatusManager.RFIFIND_MASK)

    rfi_utils.run_accelsearch()
    self.ledger.update_status(i, StatusManager.ZERO_DM_ACCELSEARCH)



if __name__ == __main__():
    main(args)



    #update ledger
