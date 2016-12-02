#!/usr/bin/env python2
"""
Generate command lines to run MSIsensor on PCAWG paired tumor-normal BAMs.
"""

import sys, argparse, os

def __main(args):
    o = open(args.output, 'w')
    n_all = n_succ = 0
    for s in open(args.input):
        normal_wgs_aliquot_id, status, normal_bam_path, tumor_wgs_aliquot_id, \
            tumor_bam_path = s.strip().split('\t')
        if normal_wgs_aliquot_id == 'normal_wgs_aliquot_id':
            continue
        n_all += 1
        if status != 'Success':
            continue
        n_succ += 1
        if args.regions == '-':
            regions = ''
        else:
            regions = '-e ' + args.regions
        params = {'msissensor' : args.msisensor,
                  'msisensor_ref' : args.reference,
                  'nbam' : normal_bam_path,
                  'tbam' : tumor_bam_path,
                  'output' : args.outdir + '/' + tumor_wgs_aliquot_id,
                  'regions' : regions,
                  'fdr' : args.fdr,
                  'cov_thr' : args.coverage_threshold,
                  'min_hp_size' : args.min_hp_size,
                  'min_hp_size_dist' : args.min_hp_size_dist,
                  'max_hp_size_dist' : args.max_hp_size_dist,
                  'min_ms_size' : args.min_ms_size,
                  'min_ms_size_dist' : args.min_ms_size_dist,
                  'max_ms_size_dist' : args.max_ms_size_dist,
                  'span' : args.span,
                  'threads' : args.threads,
                  'disfile' : args.outdir + '/' + tumor_wgs_aliquot_id + '_dis'}
        cmd = "/usr/bin/time -v %(msissensor)s msi -d %(msisensor_ref)s -n %(nbam)s \
-t %(tbam)s -o %(output)s %(regions)s \
-f %(fdr)f -c %(cov_thr)d -l %(min_hp_size)d -p %(min_hp_size_dist)d \
-m %(max_hp_size_dist)d -q %(min_ms_size)d -s %(min_ms_size_dist)d \
-w %(max_ms_size_dist)d -u %(span)d -b %(threads)d && rm %(disfile)s" % params
        o.write('%s\n' % cmd)

if __name__ == '__main__':
    pdir = os.path.abspath(os.path.dirname(sys.argv[0]) + '/../' )
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', help = 'PCAWG tumor-normal paired BAMs [%(default)s]',
        default = pdir + '/configuration/release_may2016.v1.4.tumor_normal_pairs.tsv')
    p.add_argument('-o', '--output', help = 'Command lines to run MSIsensor', required = True)
    p.add_argument('--msisensor', help = '[%(default)s]', default = '/opt/msisensor/msisensor')
    p.add_argument('--reference', help = '[%(default)s]', default = '/shared/data/msisensor/genome.microsatellites')
    p.add_argument('--outdir', help = '[%(default)s]', default = '/shared/data/results/msisensor')
    p.add_argument('--regions', help = '[%(default)s]', default = pdir + '/configuration/regions.bed')
    p.add_argument('--fdr', help = '[%(default)s]', default = 0.05, type = float)
    p.add_argument('--coverage-threshold', help = '[%(default)s]', default = 15, type = int) # default for WGS
    p.add_argument('--min-hp-size', help = '[%(default)s]', default = 5, type = int)
    p.add_argument('--min-hp-size-dist', help = '[%(default)s]', default = 10, type = int)
    p.add_argument('--max-hp-size-dist', help = '[%(default)s]', default = 50, type = int)
    p.add_argument('--min-ms-size', help = '[%(default)s]', default = 3, type = int)
    p.add_argument('--min-ms-size-dist', help = '[%(default)s]', default = 5, type = int)
    p.add_argument('--max-ms-size-dist', help = '[%(default)s]', default = 40, type = int)
    p.add_argument('--span', help = '[%(default)s]', default = 500, type = int)
    p.add_argument('--threads', help = '[%(default)s]', default = 2, type = int)
    args = p.parse_args()
    if args.input is None:
        p.print_usage()
        sys.exit(2)
    __main(args)
