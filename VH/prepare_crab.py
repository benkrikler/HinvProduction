#! /usr/bin/env python3
"""
"""
import os
import string
import re

ScriptDir = os.path.realpath(os.path.dirname(__file__))
CrabCfgDir = "crab_cfgs"


def process_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-m", "--prod-mode", help="Which Production mode to generate for", choices=("ZH", "WplusH", "WminusH"), required=True)
    parser.add_argument("-b", "--build-dir", help="What is the 'build' directory to use.  Defaults to 'build_{prod-mode}' if not given.", default=None)
    parser.add_argument("-s", "--stage", help="Which stage in the data processing to run")
    parser.add_argument("-r", "--replacements", action="append", help="Add a list of variables to replace in the input config file.  Must take form: 'KEY=Value'", default=[])
    parser.add_argument("-k", "--kernel-ext", default=None, help="Additional sequence to include in the job name kernel")
    args = parser.parse_args()
    if not args.build_dir:
        args.build_dir = "build_" + args.prod_mode
    args.build_dir = os.path.realpath(args.build_dir)
    args.crab_dir = os.path.join(args.build_dir, CrabCfgDir) 
    return args


def setup(build_dir, crab_dir):
    os.makedirs(build_dir, exist_ok=True)
    if not os.path.isdir(crab_dir):
        os.mkdir(crab_dir)


def make_config(stage, crab_dir, prod_mode, build_dir, replacements, kernel_ext):
    repls = dict(Kernel = prod_mode + "_Vhadronic_Hinv_M125",
                 Driver = os.path.join(build_dir, "driver_cfg_{stage}.py").format(stage=stage)
                )
    if kernel_ext:
	    repls["Kernel"] = repls["Kernel"] + "_" + kernel_ext
    for repl in replacements:
        key, value = repl.split("=")
        repls[key] = value
    in_cfg = os.path.join(ScriptDir, CrabCfgDir, "crab_submission_{stage}.py").format(stage=stage)
    out_cfg = os.path.join(crab_dir, "crab_submission_{stage}.py").format(stage=stage)
    print("Input Crab config template:", in_cfg)
    print("Output Crab config:", out_cfg)
    print("Replacements:", repls)

    with open(in_cfg, "r") as infile:
        lines = infile.read()

    for key, repl in repls.items():
        lines = re.sub("%%" + key.upper() + "%%", repl, lines)

    with open(out_cfg, "w") as outfile:
        outfile.write(lines)


if __name__ == "__main__":
    args = process_args()
    setup(args.build_dir, args.crab_dir)
    make_config(**vars(args))
