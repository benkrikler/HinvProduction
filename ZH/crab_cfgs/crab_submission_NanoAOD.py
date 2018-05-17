from CRABClient.UserUtilities import config, getUsernameFromSiteDB


def auto_find_request_name(directory, name, index=1):
    import os
    full = "{}_{}".format(name, index)
    if not os.path.isdir(os.path.join(directory, "crab_" + full)):
        return full
    return auto_find_request_name(directory, name, index + 1)


config = config()
config.General.workArea        = 'crab_ZH_ZToQQ_Hinv_M125'
config.General.requestName     = auto_find_request_name(config.General.workArea,'ZH_ZToQQ_Hinv_M125_NanoAOD')
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName   = '/afs/cern.ch/work/b/bkrikler/chia/HinvProduction/ZH/cmsdriver_cfgs/driver_cfg_nanoaod.py'
config.JobType.outputFiles = ['output_nanoaod.root']
config.JobType.numCores = 4

config.Data.inputDataset         = '/ZH_ZToQQ_Hinv_M125/bkrikler-ZH_ZToQQ_Hinv_M125_MiniAOD-28028af67189b3de7224b79195bd0e1d/USER' # Update this
config.Data.inputDBS             = 'phys03'
config.Data.splitting            = 'FileBased'
config.Data.unitsPerJob          = 1
config.Data.totalUnits           = -1
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = config.General.requestName

config.Site.storageSite = 'T2_UK_London_IC'
#config.Site.storageSite = 'T2_UK_SGrid_Bristol'
