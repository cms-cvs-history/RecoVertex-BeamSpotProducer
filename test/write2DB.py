import FWCore.ParameterSet.Config as cms


process = cms.Process("write2DB")
process.load("FWCore.MessageLogger.MessageLogger_cfi")


process.load("CondCore.DBCommon.CondDBCommon_cfi")

#################################
# Produce a SQLITE FILE
#
process.CondDBCommon.connect = "sqlite_file:EarlyCollision.db"
process.CondDBCommon.DBParameters.authenticationPath = '/afs/cern.ch/cms/DB/conddb'
#################################
#
# upload conditions to orcon
#
#process.CondDBCommon.connect = "oracle://cms_orcon_prod/CMS_COND_21X_BEAMSPOT"
#process.CondDBCommon.DBParameters.authenticationPath = '/nfshome0/xiezhen/conddb'
#################################

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
                                          process.CondDBCommon,
                                          toPut = cms.VPSet(cms.PSet(
    record = cms.string('BeamSpotObjectsRcd'),
    tag = cms.string('Early900GeVCollision_7p4cm_V1_IDEAL_V10')
))
)



process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32(1)
                    )
process.beamspot = cms.EDFilter("BeamSpotWrite2DB",
                                OutputFileName = cms.untracked.string('EarlyCollision.txt')
                                )



#process.CondDBCommon.connect = 'oracle://cms_orcoff_int2r/CMS_COND_BEAMSPOT'
#process.CondDBCommon.DBParameters.authenticationPath = '/afs/cern.ch/cms/DB/conddb'

process.p = cms.Path(process.beamspot)
