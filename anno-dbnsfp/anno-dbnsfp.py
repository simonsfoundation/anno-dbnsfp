#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import sqlite3
import tempfile
import pandas
import subprocess


required_clms = ['CHROM', 'POS', 'REF', 'ALT']

join_hg19 = """
ATTACH '%(dbnsfp)s' as dbnsfp;
SELECT *
  FROM X a 
    LEFT OUTER JOIN
       dbnsfp.DBNSFP b 
    on
      a.CHROM = b.CHROM_hg19 and
      a.POS = b.POS_hg19 and
      a.REF = b.REF and
      a.ALT = b.ALT;"""
join_hg38 ="""
ATTACH '%(dbnsfp)s' as dbnsfp;
SELECT *
FROM
  X a
    LEFT OUTER JOIN
  dbnsfp.DBNSFP b
    on a.CHROM = b.CHROM and
       a.POS = b.POS and
       a.REF = b.REF and
       a.ALT = b.ALT;
"""


def runInShell(cmd, return_output=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        if return_output:
            return stdout
        else:
            return 0
    else:
        sys.stderr.write(stderr)
        return 1


def createDB(other_clms, required_clms):
    tbl_schema = []
    tbl_schema.append('"')
    tbl_schema.append('CREATE TABLE X(')
    tbl_schema.append('CHROM CHAR(2) NOT NULL, ')
    tbl_schema.append('POS INTEGER NOT NULL, ')
    tbl_schema.append('REF CHAR(1) NOT NULL, ')
    tbl_schema.append('ALT CHAR(1) NOT NULL')
    if not other_clms:
        tbl_schema.append(');')
        tbl_schema.append('"')
    else:
        for i in other_clms:
            tbl_schema.append(', %s CHAR(100) NOT NULL' % i)
        tbl_schema.append(');')
        tbl_schema.append('"')
    return ''.join(tbl_schema)


def getClmNames(conn, tbl):
    cursor = conn.execute('select * from %s' % tbl)
    nsfp_colnames = list(map(lambda x: x[0], cursor.description))
    print(' '.join(nsfp_colnames))


if __name__ == '__main__':
#    print sys.argv
    arg_parser = argparse.ArgumentParser(
        description='Annotate a vcf file,\
        or a csv file containing columns CHROM POS REF ALT,\
        with values from dbNSFP')
    arg_parser.add_argument('input_file',
                            default='',
                            type=str,
                            help='A comma or tab delimited file\
                            containing columns CHROM POS REF ALT,\
                            specify type with --tab or --csv')
    arg_parser.add_argument('--dbnsfp_cols',
                            default='genename,G1000p3_AF,ExAC_AF',
                            type=str,
                            help='a coma delimited string of dbNSFP columns to\
                            include in annotation, e.g.\
                            genename,G1000p3_AF,ExAC_AF,TWINSUK_AF,ALSPAC_AF')
#    arg_parser.add_argument('--sqlite',
#                            default='/mnt/xfs1/home/asalomatov/miniconda2/bin/sqlite3',
#                            type=str,
#                            help='\
#                            It has to be in your PATH')
    arg_parser.add_argument('--dbnsfp',
                            default='/mnt/xfs1/scratch/asalomatov/data/dbNSFP/dbNSFPv3.4a/dbNSFP3.4a.db',
                            type=str,
                            help='A path to a sqlite version of dbNSFP with the header\
                            modified to contain CHROM, POS, REF, ALT')
    arg_parser.add_argument('--genome_build',
                            default='hg19',
                            choices=set(('hg19', 'hg38')),
                            help='Which genome build to use.')
    arg_parser.add_argument('--output_dir',
                            default='./',
                            type=str,
                            help='A path to an output directory.')
    arg_parser.add_argument('-p',
                            action='store_true',
                            help='If run with this option, will print dbNSFP\
                            column names and exit')
    arg_parser.add_argument('--input_delim',
                            choices=set(('csv', 'tsv')),
                            default='tsv',
                            help='To specify if input file is comma or tab\
                            delimited.')
    
    args = arg_parser.parse_args()
    dbnsfp = args.dbnsfp
#    print(args)
    if args.p:
        connNSFP = sqlite3.connect(dbnsfp)
        getClmNames(connNSFP, 'DBNSFP')
        connNSFP.close()
    else:
        tmp_dir = tempfile.mkdtemp()
        tmp_inp = tempfile.mktemp(dir=tmp_dir, suffix='', prefix='')
        tmp_db = tempfile.mktemp(dir=tmp_dir, suffix='.sqlite', prefix='')
        tmp_sql = tempfile.mktemp(dir=tmp_dir, suffix='', prefix='')
        tmp_outp = tempfile.mktemp(dir=tmp_dir, suffix='.csv', prefix='')
        outp_file = os.path.join(args.output_dir, args.input_file + '.ann.tsv')
        # print('Working in %s' % tmp_dir)
        # print([tmp_inp, tmp_db])
        if args.input_delim == 'tsv':
            df = pandas.read_table(args.input_file)
        else:
            df = pandas.read_csv(args.input_file)
        
        for i in required_clms:
            if i not in df.columns:
                sys.exit('%s is not among input file columns' % i)
        
        other_clms = [i for i in df.columns if i not in required_clms]
        anno_clms = args.dbnsfp_cols.split(',')
        df = df[required_clms + other_clms]
        df.fillna('.', inplace=True)
        df.to_csv(tmp_inp, header=False, index=False)
        tbl_schema = createDB(other_clms, required_clms)
        cmd = 'sqlite3 %s ' % tmp_db + tbl_schema
        # print(cmd)
        runInShell(cmd)
        runInShell("echo .separator , > %s" % tmp_sql)
        runInShell("echo .import %(tmp_inp)s X >> %(tmp_sql)s" %
                   locals())
        cmd = "sqlite3 %(tmp_db)s < %(tmp_sql)s" % locals()
        # print(cmd)
        runInShell(cmd)
        if args.genome_build == 'hg19':
            x = join_hg19 % locals()
        else:
            x = join_hg38 % locals()
        # print(x)
        with open(tmp_sql, 'w') as f:
            f.write(x)
        cmd = 'sqlite3 -csv -header %(tmp_db)s < %(tmp_sql)s > %(tmp_outp)s'\
              % locals()
        # print(cmd)
        runInShell(cmd)
        res = pandas.read_csv(tmp_outp)
        res[required_clms + other_clms + anno_clms].to_csv(outp_file,
                                                           index=False,
                                                           sep='\t')
        runInShell('rm -r %s' % tmp_dir)
