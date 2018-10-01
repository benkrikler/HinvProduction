#!/usr/bin/env python
from __future__ import print_function, division
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from itertools import combinations
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


from rootpy.utils.ext_glob import glob
import numpy as np


class NoIsolated(Module):
    def __init__(self, collection, iso_var, iso_cut, pt_thresh):
        self.writeHistFile=False
        self.collection = collection
        self.iso_var = collection + "_" + iso_var
        #self.iso_var = iso_var
        self.iso_cut = iso_cut
        self.pt_var = collection + "_pt"
        self.pt_thresh = pt_thresh

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

    def analyze(self, event):
        pt = np.array(list(getattr(event, self.pt_var)))
        iso = np.array(list(getattr(event, self.iso_var)))
        return np.all((pt < self.pt_thresh) | (iso > self.iso_cut))


class InvertedVBF(Module):
    def __init__(self, pt_thresh, d_eta_thresh, m_dijet_thresh):
        self.writeHistFile=False
        self.pt_thresh = pt_thresh
        self.d_eta_thresh = d_eta_thresh
        self.m_dijet_thresh = m_dijet_thresh

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

    def analyze(self, event):
        jets = Collection(event, "Jet")
        jets = [jets[i] for i in range(len(jets))]
        for jet1, jet2 in combinations(jets, 2):
            if jet1.pt < self.pt_thresh and jet2.pt < self.pt_thresh:
                continue
            mass = (jet1.p4() + jet2.p4()).M()
            if mass < self.m_dijet_thresh:
                continue
            delta_eta = abs(jet1.eta - jet2.eta)
            if delta_eta > self.d_eta_thresh:
                return False

        return True


def run(input_files, runsAndLumis=None, directory=".", for_crab=True):
    preselection=None
    modules = [
            NoIsolated("Electron", "miniPFRelIso_all", 0.1, pt_thresh=10),
            NoIsolated("Muon", "miniPFRelIso_all", 0.2, pt_thresh=10),
            NoIsolated("Photon", "pfRelIso03_all", 0.1, pt_thresh=10),
            InvertedVBF(30, 4, 700),
            ]

    if for_crab:
        ext_opts = dict(provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
    else:
        ext_opts = dict(histFileName="histOut.root",histDirName="plots", haddFileName="combined.root")
    p=PostProcessor(directory,input_files,cut=preselection,branchsel=None,modules=modules, **ext_opts)
    p.run()


#if __name__ == "__main__":
#    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#    run(inputFiles(), runsAndLumis=runsAndLumis())


if __name__ == "__main__":
    #files = ["root://gfe02.grid.hep.ph.ic.ac.uk:1097//store/user/bkrikler/ttH_HToInvisible_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_NanoAOD_1/180530_113050/0000/output_nanoaod_9.root"]

    model = "ttH_HToInvisible"
    files = glob("root://gfe02.grid.hep.ph.ic.ac.uk:1097//store/user/bkrikler/ttH_HToInvisible_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_NanoAOD_1/180530_113050/0000/output_nanoaod_*.root")
    print("Files to process: ", len(files))
    run(files, directory=model, for_crab=False)

#    from multiprocessing import Pool
#    jobs = 4
#    n_files = len(files)
#    if n_files < jobs:
#        jobs = n_files
#
#    p = Pool(jobs)
#    files_per_job = n_files // jobs
#    remainders = n_files % jobs
#    files_per_job = [files_per_job + (1 if i < remainders else 0) for i in range(jobs)]
#    files_per_job = list(np.cumsum(files_per_job))
#    files_per_job = [0] + files_per_job
#    file_lists = [files[start: stop] for start, stop in zip(files_per_job[:-1], files_per_job[1:])]
#    print(len(file_lists))
#    p.map(run, file_lists)
