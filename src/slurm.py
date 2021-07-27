
# Vivek: code inspired from https://github.com/brentp/slurmpy/blob/master/slurmpy/slurmpy.py but with several modifications

import sys
import os
import subprocess
import tempfile
import hashlib
from datetime import datetime

TEMPLATE = """\
#!/bin/bash

#SBATCH -e {log_dir}/{name}.%J.err
#SBATCH -o {log_dir}/{name}.%J.out
#SBATCH -J {name}

{header}

{bash_setup}

__script__"""

VALID_DEPENDENCY_TYPES = {
    "after",
    "afterany",
    "afterburstbuffer",
    "aftercorr",
    "afternotok",
    "afterok",
    "expand",
}





class Slurm(object):


    def __init__(self, name, slurm_kwargs={}, tmpl=TEMPLATE,
                 date_in_name=True, scripts_dir="slurm-scripts",
                 log_dir='logs', ):

        self.log_dir = log_dir
        self.bash_setup = "set -eo pipefail -o nounset"
        self.scripts_dir = os.path.abspath(scripts_dir)
        self.date_in_name = bool(date_in_name)


        header = []

        for k, v in slurm_kwargs.items():
            if len(k) > 1:
                k = "--" + k + "="
            else:
                k = "-" + k + " "
            header.append("#SBATCH %s%s" % (k, v))



            

        self.header = "\n".join(header)
        self.name = "".join(x for x in name.replace(
            " ", "-") if x.isalnum() or x == "-")
        self.tmpl = tmpl
        self.slurm_kwargs = slurm_kwargs



    def __str__(self):
        return self.tmpl.format(name=self.name, header=self.header,
                                log_dir=self.log_dir,
                                bash_setup=self.bash_setup)

    def _tmpfile(self):

        for _dir in [self.scripts_dir, self.log_dir]:
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        return "%s/%s.sh" % (self.scripts_dir, self.name)

    def run(self, command, out_prefix="", cmd_kwargs=None,
            _cmd="sbatch", tries=1, depends_on=None, depends_how='afterok'):
        """
        command: a bash command that you want to run
        out_prefix: if not specified, the sha1 of the command to run
                       appended to job name. if it is "date", the yyyy-mm-dd
                       date will be added to the job name.
        cmd_kwargs: dict of extra arguments to fill in command
                   (so command itself can be a template).
        _cmd: submit command (change to "bash" for testing).
        tries: try to run a job either this many times or until the first
               success.
        depends_on: job ids that this depends on before it is run (users 'afterok')
        depends_how: ability to change how a job depends on others
        """
        if depends_how not in VALID_DEPENDENCY_TYPES:
            raise ValueError(f"depends_how must be in {VALID_DEPENDENCY_TYPES}")

        if self.date_in_name:
            out_prefix += "-" + datetime.strftime(datetime.now(), 
                                                     format='%y-%m-%d-%H-%M-%S')
        out_prefix = name_addition.strip(" -")

        if cmd_kwargs is None:
            cmd_kwargs = {}

        n = self.name
        self.name = self.name.strip(" -")
        self.name += ("-" + out_prefix.strip(" -"))
        args = []
        for k, v in cmd_kwargs.items():
            args.append("export %s=%s" % (k, v))
        args = "\n".join(args)

        tmpl = str(self).replace("__script__", args + "\n###\n" + command)
        if depends_on is None or (len(depends_on) == 1 and depends_on[0] is None):
            depends_on = []

        with open(self._tmpfile(), "w") as sh:
            sh.write(tmpl)

        job_id = None
        for itry in range(1, tries + 1):
            args = [_cmd]
            # sbatch (https://slurm.schedmd.com/sbatch.html) job dependency has the following format:
            # -d, --dependency=<dependency_list>
            #       <dependency_list> is of the form <type:job_id[:job_id][,type:job_id[:job_id]]> 
            # Create job dependency string
            dependency_string = "".join([f":{d}" for d in depends_on])
            if depends_on:
                dependency_string= f"{depends_how}{dependency_string}"
            if itry > 1:
                mid = f"afternotok:{job_id}"
                # Merge retry dependency to job dependencies
                if dependency_string:
                    dependency_string = f"{dependency_string},{mid}"
                else:
                    dependency_string= mid
            # Add dependency option to sbatch
            if dependency_string:
                args.extend([f"--dependency={dependency_string}" ])
            args.append(sh.name)
            res = subprocess.check_output(args).strip()
            print(res, file=sys.stderr)
            self.name = n
            if not res.startswith(b"Submitted batch"):
                return None
            j_id = int(res.split()[-1])
            if itry == 1:
                job_id = j_id
        return job_id
