import argparse 
from log import Logger, init_logging
import logging
import random, time, datetime
from rsyncer import Rsyncer

def get_args():
    argparser = argparse.ArgumentParser(description="Processing pipeline for TRAPUM pulsar searches on the Hercules 2 cluster")
    argparser.add_argument("-config", dest="config", help="configuration file")
    argparser.add_argument("-init", dest="init",  help= "init pipeline and unload a sample config file")
    argparser.add_argument("-dest", dest="dest",  help= "Output directory for the pipeline")
    argparser.add_argument("-verbose", dest="verbose", help="Enable verbose terminal logging", action="store_true")
    argparser.add_argument("-log_file_prefix", dest="log_file_prefix", help="Name of log file",default="candyfactory")
    argparser.add_argument("-slurm", dest="slurm", help="Submit as a slurm job", action="store_true" )
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

    ledger = Ledger()


   # Rsyncs data from tape -> staging and staging -> processing. 
   rsyncer = rsyncer(config.file_locations, config.beam_list, config.max_beams_on_processing_disk, ledger)
   rsyncer.transfer_files()

   if(args.slurm):

   		







if __name__ == '__main__':
 	main()