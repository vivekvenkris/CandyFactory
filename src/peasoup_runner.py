from constants import StatusManager
import sys
import argparse
from config_parser import ConfigurationReader
from log import Logger, init_logging
import datetime
from ledger import Ledger
from app_utils import ensure_correct_processing_status
from gen_utils import run_process, run_with_singularity
def get_args():
    argparser = argparse.ArgumentParser(description="Run peasoup")
    argparser.add_argument("-config", dest="config", help="configuration file")
    argparser.add_argument("-verbose", dest="verbose", help="Enable verbose terminal logging", action="store_true")
    argparser.add_argument("-beam_num", dest="beam_num", help="beam number to process")
    argparser.add_argument("-ledger_file", dest="ledger_file", help="ledger_file")
    argparser.add_argument("-force", dest="force", help="Try to force run peasoup even if status is not as expected")
    argparser.add_argument("-log_file_prefix", dest="log_file_prefix", help="Name of log file",default="candyfactory")


    argparser.add_argument("-search_type", dest="search_type", help="Search time: ZERO_ACC, ACC, SEGMENTED",default="candyfactory")

    args = argparser.parse_args()
    return args


def main(args):


    #get args, inititalise logger, config and ledger
    args = get_args()    
    logger = init_logging(file_name="{}_{}.log".format(args.log_file_prefix,(datetime.datetime.now()).strftime("%Y-%m-%d-%H:%M:%S")),
                             file_level=logging.DEBUG if args.verbose else None)

    config_reader = ConfigurationReader(args.config) 
    config = config_reader.config

    ledger = Ledger(args.ledger_file)

    status_manager = StatusManager.getInstance()

    status = ledger.get_status(args.beam_num)
    ensure_correct_processing_status(status,status_manager.ZERO_DM_ACCELSEARCH)

    search_type = args.search_type
    peasoup_config = config.peasoup_config

    base_peasoup_cmd = "/usr/local/bin/peasoup --dm_file {} --pad -z {}.birds -k {}.badchan_peasoup {}" \
                        .format(config.dm_file, args.beam_num, args.beam_num, config.peasoup_config.peasoup_flags )

    if(search_type == status_manager.SEARCH_TYPE_ZERO_ACC):

        peasoup_cmd = "{} --acc_start 0 --acc_end 0 -o zero_acc".format(base_peasoup_cmd) 

        run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)

    else:

        for segment_config in config.peasoup_config.segment_configs:


            peasoup_cmd = "{} --acc_start {} --acc_end {} ".format(base_peasoup_cmd, segment_config.acc_start, segment_config.acc_end)

            if( segment_config.fractional_segment_length == 1):

                peasoup_cmd = "{} --start {} --end {} -o full".format(peasoup_cmd, peasoup_config.start_offset, peasoup_config.end_offset)
                run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)


            else:

                start = peasoup_config.start_offset

                end = start + segment_config.fractional_segment_length

                while start + segment_config.fractional_segment_length <= peasoup_config.end_offset:

                    end = start + segment_config.fractional_segment_length

                    dir_str = segment_config.fractional_segment_length_start_end

                    peasoup_cmd = "{} --start {} --end {}",format(start, end)
                    run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)

                    start = end

                #if there are any residual data, choose the last segment from the end
                start = end - segment_config.fractional_segment_length

                peasoup_cmd = "{} --start {} --end {}",format(start, end)

                run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)


if __name__ == '__main__':
    main(sys.argv)







        



















