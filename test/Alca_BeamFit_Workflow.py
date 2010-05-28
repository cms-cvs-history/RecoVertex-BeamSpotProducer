import FWCore.ParameterSet.Config as cms

process = cms.Process("alcaBeamSpotWorkflow")
# initialize MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport  = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(1000000),
)

process.load("RecoVertex.BeamSpotProducer.AlcaBeamSpotProducer_cfi")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    '/store/express/Commissioning10/StreamExpress/ALCARECO/v9/000/135/149/F053205D-8E5B-DF11-803D-000423D9997E.root',
    '/store/express/Commissioning10/StreamExpress/ALCARECO/v9/000/135/149/F038B0BE-3A5B-DF11-B94E-000423D98750.root',
    '/store/express/Commissioning10/StreamExpress/ALCARECO/v9/000/135/149/F03560AE-165B-DF11-AE55-0030486780EC.root',
    '/store/express/Commissioning10/StreamExpress/ALCARECO/v9/000/135/149/F03169C7-935B-DF11-A59F-001D09F28D54.root',
    '/store/express/Commissioning10/StreamExpress/ALCARECO/v9/000/135/149/EE15D8B9-1E5B-DF11-8205-003048D2BC30.root'
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(3000) #1500
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# this is for filtering on L1 technical trigger bit
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND ( 40 OR 41 )')
##
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR10_P_V5::All' #'GR_R_35X_V8::All'
process.load("Configuration.StandardSequences.Geometry_cff")


## reco PV
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi")
process.offlinePrimaryVertices.TrackLabel = cms.InputTag("ALCARECOTkAlMinBias") 

#### remove beam scraping events
process.noScraping= cms.EDFilter("FilterOutScraping",
                                 applyfilter = cms.untracked.bool(True),
                                 debugOn = cms.untracked.bool(False), ## Or 'True' to get some per-event info
                                 numtrack = cms.untracked.uint32(10),
                                 thresh = cms.untracked.double(0.20)
)


process.MessageLogger.debugModules = ['AlcaBeamSpotProducer']

################### Primary Vertex
process.offlinePrimaryVertices.PVSelParameters.maxDistanceToBeam = 2
process.offlinePrimaryVertices.TkFilterParameters.maxNormalizedChi2 = 20
process.offlinePrimaryVertices.TkFilterParameters.minSiliconLayersWithHits = 6
process.offlinePrimaryVertices.TkFilterParameters.maxD0Significance = 100
process.offlinePrimaryVertices.TkFilterParameters.minPixelLayersWithHits = 1
process.offlinePrimaryVertices.TkClusParameters.TkGapClusParameters.zSeparation = 1


#######################
process.alcaBeamSpotProducer.BeamFitter.TrackCollection = 'ALCARECOTkAlMinBias'
process.alcaBeamSpotProducer.BeamFitter.MinimumTotalLayers = 6
process.alcaBeamSpotProducer.BeamFitter.MinimumPixelLayers = -1
process.alcaBeamSpotProducer.BeamFitter.MaximumNormChi2 = 10
process.alcaBeamSpotProducer.BeamFitter.MinimumInputTracks = 2
process.alcaBeamSpotProducer.BeamFitter.MinimumPt = 1.0
process.alcaBeamSpotProducer.BeamFitter.MaximumImpactParameter = 1.0
process.alcaBeamSpotProducer.BeamFitter.TrackAlgorithm =  cms.untracked.vstring()
process.alcaBeamSpotProducer.BeamFitter.InputBeamWidth = -1 # 0.0400
#process.alcaBeamSpotProducer.BeamFitter.Debug = True

process.alcaBeamSpotProducer.PVFitter.Apply3DFit = True
process.alcaBeamSpotProducer.PVFitter.minNrVerticesForFit = 10 
#########################


# fit as function of lumi sections
process.alcaBeamSpotProducer.AlcaBeamSpotProducerParameters.fitEveryNLumi = 1
process.alcaBeamSpotProducer.AlcaBeamSpotProducerParameters.resetEveryNLumi = 1

process.out = cms.OutputModule( "PoolOutputModule",
                                fileName = cms.untracked.string( 'AlcaBeamSpot.root' ),
                                outputCommands = cms.untracked.vstring("keep *")
                              )


process.e = cms.EndPath( process.out )

process.p = cms.Path(process.hltLevel1GTSeed +
                     process.offlineBeamSpot +
#                     process.TrackRefitter +
                     process.offlinePrimaryVertices+
#                     process.noScraping +
                     process.alcaBeamSpotProducer)
