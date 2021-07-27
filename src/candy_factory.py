import argparse 
from log import Logger, init_logging
import logging
import random, time, datetime
import os, sys, pathlib, errno, time
import numpy as np

from rfi_finder import RfiFinder
from ledger import Ledger
from exceptions import IncorrectInputsException
from rsyncer import Rsyncer
from config_parser import ConfigurationReader
from peasoup_runner import PeasoupRunner
from status_manager import StatusManager

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
    # try:
    #     import pretty_traceback
    #     pretty_traceback.install()
    # except ImportError:
    #     pass    # no need to fail because of missing dev dependency


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
            print( os.path.join(pathlib.Path().resolve(), "candy_factory.db"))
            ledger = Ledger(os.path.join(pathlib.Path().resolve(), "candy_factory.db"))
            sys.exit(os.EX_OK)
        except OSError as e:
            if e.errno ==  errno.EEXIST:
                raise IncorrectInputsException("{} directory already exists".format(args.init))
            sys.exit(os.EX_OK)




    config_reader = ConfigurationReader(args.config) 
    config = config_reader.config

    ledger_name = os.path.join(config.root_output_dir, "candy_factory.db")
    ledger = Ledger(ledger_name)
    print(ledger.get_ledger_table())


    status_manager = StatusManager.getInstance()


    beam_list = config.beam_list if config.beam_list is not None else np.arange(0,config.observations.nbeams, 1)

    #Rsyncs data from tape -> staging and staging -> processing. 
    rsyncer = Rsyncer(config.file_locations, beam_list, config.max_beams_on_processing_disk)
    rsyncer.transfer_files()

    out_prefix = config.observations.generate_prefix()


    rfi_finder = RfiFinder(config, out_prefix)
    peasoup_runner = PeasoupRunner(config, out_prefix)



    while True:

        print(ledger.get_ledger_table())

        current_beam_list = ledger.get_beams_for_status(status_manager.RSYNC_TO_PROCESSING)
        print("current_beam_list for RFI excision:",current_beam_list)

        for beam_name in current_beam_list:
            rfi_finder.find_rfi(beam_name)


        current_beam_list = ledger.get_beams_for_status(status_manager.ZERO_DM_ACCELSEARCH)
        print("current_beam_list for peasoup:",current_beam_list)


        for beam_name in current_beam_list:

            for search_type in [status_manager.SEARCH_TYPE_ACC]: #[status_manager.SEARCH_TYPE_ZERO_ACC,status_manager.SEARCH_TYPE_ACC, status_manager.SEARCH_TYPE_SEGMENTED]:
                if not ledger.has_beam(beam_name, search_type):
                    ledger.add_to_ledger(beam_name, search_type=search_type)
                peasoup_runner.run_peasoup(beam_name, search_type)

            break

        time.sleep(5)

if __name__ == '__main__':
 	main()