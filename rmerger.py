#!/usr/bin/env python

import ROOT
import click

@click.command()
@click.argument('ntuple_files', type=click.Path(dir_okay=False, exists=True), nargs=-1)
@click.option('-o', '--outfile', type=click.Path(exists=False), default='tfile_merged.root')

def main(ntuple_files, outfile):

    m = ROOT.TFileMerger()
    for f in ntuple_files:
        m.AddFile(f)
    m.OutputFile(outfile)
    m.Merge()

if __name__=='__main__':
    main()