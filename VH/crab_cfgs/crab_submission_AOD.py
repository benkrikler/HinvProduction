from CRABClient.UserUtilities import config, getUsernameFromSiteDB


def auto_find_request_name(directory, name, index=1):
    import os
    full = "{}_{}".format(name, index)
    if not os.path.isdir(os.path.join(directory, "crab_" + full)):
        return full
    return auto_find_request_name(directory, name, index + 1)


config = config()
config.General.workArea        = 'crab_%%KERNEL%%'
requestName     = auto_find_request_name(config.General.workArea,'%%KERNEL%%_AOD')
config.General.requestName     = requestName
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName   = '%%DRIVER%%'
config.JobType.outputFiles = ['output_premix.root']
config.JobType.numCores = 1

config.Data.inputDataset         = '%%INPUT_DATASET%%' # Update this
config.Data.inputDBS             = 'phys03'
config.Data.splitting            = 'FileBased'
config.Data.unitsPerJob          = 1
config.Data.totalUnits           = -1
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = requestName

config.Site.storageSite = 'T2_UK_London_IC'
#config.Site.storageSite = 'T2_UK_SGrid_Bristol'
