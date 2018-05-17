from CRABClient.UserUtilities import config, getUsernameFromSiteDB


def auto_find_request_name(directory, name, index=1):
    import os
    full = "{}_{}".format(name, index)
    if not os.path.isdir(os.path.join(directory, "crab_" + full)):
        return full
    return auto_find_request_name(directory, name, index + 1)


config = config()
config.General.workArea        = 'crab_ZH_ZToQQ_Hinv_M125'
config.General.requestName     = auto_find_request_name(config.General.workArea,'ZH_ZToQQ_Hinv_M125_AOD')
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName   = '/afs/cern.ch/work/b/bkrikler/chia/HinvProduction/ZH/cmsdriver_cfgs/driver_cfg_premix_step2.py'
config.JobType.outputFiles = ['output_premix.root']
config.JobType.numCores = 1

config.Data.inputDataset         = '/ZH_ZToQQ_Hinv_M125/bkrikler-ZH_ZToQQ_Hinv_M125_PUMix-16ca0fac1b892ff3c3d45d801745cbbf/USER' # Update this
config.Data.inputDBS             = 'phys03'
config.Data.splitting            = 'FileBased'
config.Data.unitsPerJob          = 1
config.Data.totalUnits           = -1
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = 'ZH_ZToQQ_Hinv_M125_AOD'

config.Site.storageSite = 'T2_UK_London_IC'
#config.Site.storageSite = 'T2_UK_SGrid_Bristol'
