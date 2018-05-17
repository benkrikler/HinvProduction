from CRABClient.UserUtilities import config, getUsernameFromSiteDB


def auto_find_request_name(directory, name, index=1):
    import os
    full = "{}_{}".format(name, index)
    if not os.path.isdir(os.path.join(directory, "crab_" + full)):
        return full
    return auto_find_request_name(directory, name, index + 1)


config = config()
config.General.workArea        = 'crab_ZH_ZToQQ_Hinv_M125'
config.General.requestName = auto_find_request_name(config.General.workArea,'ZH_ZToQQ_Hinv_M125_LHE')
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = '/afs/cern.ch/work/b/bkrikler/chia/HinvProduction/ZH/cmsdriver_cfgs/driver_cfg_LHE.py'
config.JobType.outputFiles = ['output_lhe.root']

config.Data.outputPrimaryDataset = 'ZH_ZToQQ_Hinv_M125'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 100
config.Data.totalUnits           = 160000
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = 'ZH_ZToQQ_Hinv_M125_LHE'

config.Site.storageSite = 'T2_UK_London_IC'
#config.Site.storageSite = 'T2_UK_SGrid_Bristol'
