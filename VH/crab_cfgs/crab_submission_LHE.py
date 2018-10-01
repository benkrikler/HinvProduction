from CRABClient.UserUtilities import config, getUsernameFromSiteDB


def auto_find_request_name(directory, name, index=1):
    import os
    full = "{}_{}".format(name, index)
    if not os.path.isdir(os.path.join(directory, "crab_" + full)):
        return full
    return auto_find_request_name(directory, name, index + 1)


config = config()
config.General.workArea        = 'crab_%%KERNEL%%'
requestName     = auto_find_request_name(config.General.workArea,'%%KERNEL%%_LHE')
config.General.requestName     = requestName
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = '%%DRIVER%%'
config.JobType.outputFiles = ['output_lhe.root']

config.Data.outputPrimaryDataset = '%%KERNEL%%'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 100
config.Data.totalUnits           = %%TOTAL_EVENTS%%
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = requestName

config.Site.storageSite = 'T2_UK_London_IC'
#config.Site.storageSite = 'T2_UK_SGrid_Bristol'
