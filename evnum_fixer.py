#!/usr/bin/env python


# # Enable multi-threading with the specified amount of threads (let's start with just one)
# # Note that in newer ROOT versions you simply need to write ROOT.EnableImplicitMT()
# ROOT.EnableImplicitMT()

from rich import print
import click
from pathlib import Path
import re
import concurrent.futures


@click.command()
@click.argument('ntuple_files', type=click.Path(dir_okay=False, exists=True), nargs=-1)
@click.option('-o', '--outdir', type=click.Path(file_okay=False), default='data')
def main(ntuple_files, outdir):

    ntuple_regex = re.compile(r'(.*)_(\d+)_ana\.ntuple\.root$')
    no_match = []
    ntuple_list = {}
    for ntf in ntuple_files:
        m  = ntuple_regex.match(Path(ntf).name)
        if m:
            ntuple_list[int(m.group(2))] = (ntf, m.group(1))
        else:
            no_match.append(ntf)

    if no_match:
        print("Found file names without job id:")
        for ntf in no_match:
            print(f"- {ntf}")

    # Ready to go, let's load ROOT
    import ROOT

    ROOT.EnableImplicitMT()

    def process_ntuple(k, nt_path, nt_base):
        if nt_path.startswith('/eos/project/'):
            nt_path='root://eosproject.cern.ch/'+nt_path
        print(f"Processing file {k}: {nt_path}")
        
        info_obj = None
        tree_names = []
        tp_tree_names = []

        try:
            with ROOT.TFile.Open(nt_path) as infile:
                # infile['triggerAna'].ls()
                info_obj = infile['triggerAna/info']
                tree_names  = [k.GetName() for k in infile['triggerAna'].GetListOfKeys() if k.GetClassName()=='TTree']
                tp_tree_names  = [f'TriggerPrimitives/{k.GetName()}' for k in infile['triggerAna/TriggerPrimitives'].GetListOfKeys() if k.GetClassName()=='TTree']
        except OSError:
            print(f"Failed to open file {k} - skipping")
            return None

        outpath=f'{outdir}/{nt_base}_{k}_evfix_ana.ntuple.root'
        print(f"Saving fixed ntuples to {outpath}")


        with ROOT.TFile(outpath, "RECREATE") as outfile:
            outfile.mkdir('triggerAna')
            # outfile['triggerAna'].WriteObject(info_obj, 'info')


        rso = ROOT.RDF.RSnapshotOptions()
        rso.fMode = "UPDATE"
        # rso.fOutputFormat = ROOT.RDF.ESnapshotOutputFormat.kRNTuple

        for t in tree_names+tp_tree_names:
            rdf = ROOT.RDataFrame(f'triggerAna/{t}', nt_path)
            rdf_up = rdf.Redefine('event', f'event+{k*10}')
            rdf_up.Snapshot(f'triggerAna/{t}', outpath, options=rso)

        with ROOT.TFile(outpath, "UPDATE") as outfile:
            outfile['triggerAna'].WriteObject(info_obj, 'info')

        return outpath



    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        future_to_outpaths = {executor.submit(process_ntuple, k, nt_path, nt_base):k for k, (nt_path, nt_base) in ntuple_list.items()}
        for future in concurrent.futures.as_completed(future_to_outpaths):
            k = future_to_outpaths[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (k, exc))
            else:
                print(f"File {data} completed")


if __name__ == '__main__':
    main()