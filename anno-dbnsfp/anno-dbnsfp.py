#!/usr/bin/env python
from __future__ import print_function
import os, sys
import argparse


if __name__ == '__main__':
#    print sys.argv
    arg_parser = argparse.ArgumentParser(
        description='Annotate a vcf file,\
        or a csv file containing columns CHROM POS REF ALT,\
        with values from dbNSFP')
    arg_parser.add_argument('input_file',
                            default='',
                            type=str,
                            help='A VCF file, or a comma delimited file\
                            containing columns CHROM POS REF ALT')
    arg_parser.add_argument('--dbnsfp_cols',
                            default='genename',
                            type=str,
                            help='a coma delimited string of dbNSFP columns to\
                            include in annotation, e.g.\
                            1000Gp3_AF,ExAC_AF,TWINSUK_AF,ALSPAC_AF,genename')
    arg_parser.add_argument('--engine',
                            default='bcftools',
                            type=str,
                            help='Which program to use for annotation. For now,\
                            only one option - bcftools.\
                            It has to be in your PATH')
    arg_parser.add_argument('--dbnsfp',
                            default='/mnt/xfs1/scratch/asalomatov/data/dbNSFP/dbNSFPv3.4a/dbNSFP3.4a.hg19.bcft.txt.gz',
                            type=str,
                            help='A path to compressed and indexed dbNSFP with the header\
                            modified to contain CHROM, POS, REF, ALT')
    
    args = arg_parser.parse_args()
    print(args)
    pass
