import argparse 
from log import Logger, init_logging
import logging
import random, time, datetime
import os, sys, pathlib, errno, time
import numpy as np

from rfi_utils import RFIUtils
from ledger import Ledger
from exceptions import IncorrectInputsException
from rsyncer import Rsyncer
from config_parser import ConfigurationReader

def get_args():
    argparser = argparse.ArgumentParser(description="Processing pipeline for TRAPUM pulsar searches on the Hercules 2 cluster")

    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument("-config", dest="config", help="configuration file")
    group.add_argument("-init", dest="init",  help= "init pipeline and unload a sample config file in this directory")

    argparser.add_argument("-verbose", dest="verbose", help="Enable verbose terminal logging", action="store_true")
    argparser.add_argument("-log_file_prefix", dest="log_file_prefix", help="Name of log file",default="candyfactory")
    argparser.add_argument("-slurm", dest="slurm", help="Submit as a slurm job", action="store_true" )
    args = argparser.parse_args()
    return args




def main():

    args = get_args()

    #inititalise logger
    logger = init_logging(file_name="{}_{}.log".format(args.log_file_prefix,(datetime.datetime.now()).strftime("%Y-%m-%d-%H:%M:%S")),
                             file_level=logging.DEBUG if args.verbose else None)

    if args.init is not None:
        try:
            pathlib.Path(args.init).mkdir(parents=True, exist_ok=False)
            os.chdir(args.init)
            ConfigurationReader.init_default()
            for i in ["known_pulsars"]:
                os.mkdir(i)
            sys.exit(os.EX_OK)
        except OSError as e:
            pass
            if e.errno ==  errno.EEXIST:
                raise IncorrectInputsException("{} directory already exists".format(args.init))



    config_reader = ConfigurationReader(args.config) 

    config = config_reader.config

    ledger_name = os.path.join(config.root_output_dir, "candy_factory.db")

    ledger = Ledger(ledger_name)


    beam_list = config.beam_list if config.beam_list is not None else np.arange(0,config.observations.nbeams, 1)
    print(beam_list)
    #Rsyncs data from tape -> staging and staging -> processing. 
    #rsyncer = Rsyncer(config.file_locations, beam_list, config.max_beams_on_processing_disk)
    #rsyncer.transfer_files()

    #out_prefix = config.observations.generate_prefix()
    #rfi_utils = RFIUtils(config, out_prefix)
    #rfi_utils.find_rfi()

    



if __name__ == '__main__':
 	main()