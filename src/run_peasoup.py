from constants import StatusManager
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
    config = parse_config(args.config_file)
    ledger = Ledger(args.ledger_file) if args.ledger_file is None else Ledger()

    status = ledger.get_status(args.beam_num)
    ensure_correct_processing_status(status,StatusManager.ZERO_DM_ACCELSEARCH)

    type = args.search_type
    peasoup_config = config.peasoup_config

    base_peasoup_cmd = "/usr/local/bin/peasoup --dm_file {} --pad -z {}.birds -k {}.badchan_peasoup {}"
                        .format(config.dm_file, args.beam_num, args.beam_num, config.peasoup_config.peasoup_flags )

    if(type == StatusManager.ZERO_ACC):

        peasoup_cmd = "{} --acc_start 0 --acc_end 0 -o zero_acc".format(base_peasoup_cmd) 

        run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)

    else:

        for segment in config.peasoup_config.segment_list:


            peasoup_cmd = "{} --acc_start {} --acc_end {} ".format(base_peasoup_cmd, segment.acc_start, segment.acc_end)

            if( segment.fractional_segment_length == 1):

                peasoup_cmd = "{} --start {} --end {} -o full".format(peasoup_cmd, peasoup_config.start_offset, peasoup_config.end_offset)
                run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)


            else:

                start = peasoup_config.start_offset

                end = start + segment.fractional_segment_length

                while start + segment.fractional_segment_length <= peasoup_config.end_offset:

                    end = start + segment.fractional_segment_length

                    dir_str = segment.fractional_segment_length_start_end

                    peasoup_cmd = "{} --start {} --end {}",format(start, end)
                    run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)

                    start = end

                #if there are any residual data, choose the last segment from the end
                start = end - segment.fractional_segment_length

                peasoup_cmd = "{} --start {} --end {}",format(start, end)

                run_with_singularity(config.peasoup_config.singularity_image, peasoup_config.singularity_flags, peasoup_cmd)








        




















if __name__ == __main__():
    main(args)