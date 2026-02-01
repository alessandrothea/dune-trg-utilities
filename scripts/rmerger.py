#!/usr/bin/env python
import click
from rich import print
from pathlib import Path


def merge_unsafe(ntuple_files, outfile):
    print(f"Merging {len(ntuple_files)} files")
    import ROOT

    m = ROOT.TFileMerger()
    for i,f in enumerate(ntuple_files):
        print(i, type(f), f)
        m.AddFile(f)
    m.OutputFile(str(outfile))
    m.Merge()
    print(f"Merged {len(ntuple_files)} files into {outfile}")


@click.command()
@click.argument('ntuple_files', type=click.Path(dir_okay=False, exists=True), nargs=-1)
@click.option('-o', '--outfile', type=click.Path(exists=False), default='tfile_merged.root')
def main(ntuple_files, outfile):

    max_files = 500

    num_files = len(ntuple_files)
    print(num_files)
    print(num_files/max_files)
    outfile = Path(outfile)
    if num_files/max_files  > 1:
        chunks = [ntuple_files[x:x+max_files] for x in range(0, num_files, max_files)]

        tmp_files = []
        for i,fs in enumerate(chunks):
            tmp_out = outfile.parent / (f'tmp_{i:03d}_' + outfile.name)
            tmp_files.append(tmp_out)

            merge_unsafe(fs, tmp_out)

    
        merge_unsafe([str(f) for f in tmp_files], outfile)

        for tmp_file in tmp_files:
            tmp_file.unlink(missing_ok=True) 
    

    else:
        merge_unsafe(ntuple_files, outfile)

        # print(chunks, )










if __name__=='__main__':
    main()