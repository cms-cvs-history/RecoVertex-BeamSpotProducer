#!/usr/bin/env python
#____________________________________________________________
#
#  
#
# A very simple script to read beam spot DB payloads
#
# Francisco Yumiceva
# yumiceva@fnal.gov
#
# Fermilab, 2009
#
#____________________________________________________________



import sys,os
import commands

def main():

    if len(sys.argv) < 2:
	print "\n [usage] getBeamSpotDB <tag name> <run number = 1> <destDB = frontier://PromptProd/CMS_COND_31X_BEAMSPOT >\n"
	print " e.g. getBeamSpotDB First900GeVCollision_3p9cm_v3_mc_STARTUP \n\n"
        print "      destDB options \"oracle://cms_orcon_prod/CMS_COND_31X_BEAMSPOT\""
        print "                     \"sqlite_file:mysqlitefile.db\" \n"
	sys.exit()

    
    tagname = sys.argv[1]
    iov_since = ''
    iov_till = ''
    destDB = 'frontier://PromptProd/CMS_COND_31X_BEAMSPOT'
    run = '1'
    if len(sys.argv) > 3:
        destDB = sys.argv[3]
    if len(sys.argv) > 2:
        run = sys.argv[2]
    
    #sqlite_file = "sqlite_file:"+ tagname +".db"

    
    ##### READ 

    #print "read back sqlite file to check content ..."
    
    readdb_out = "readDB_"+tagname+".py"
    
    rnewfile = open(readdb_out,'w')

    rnewfile.write('''
import FWCore.ParameterSet.Config as cms

process = cms.Process("readDB")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.BeamSpotDBSource = cms.ESSource("PoolDBESSource",
                                        process.CondDBSetup,
                                        toGet = cms.VPSet(cms.PSet(
    record = cms.string('BeamSpotObjectsRcd'),
''')
    rnewfile.write('tag = cms.string(\''+tagname+'\')\n')
    rnewfile.write(')),\n')
    rnewfile.write('connect = cms.string(\''+destDB+'\')\n')
    
    #connect = cms.string('sqlite_file:Early900GeVCollision_7p4cm_STARTUP_mc.db')
    #connect = cms.string('oracle://cms_orcoff_prod/CMS_COND_31X_BEAMSPOT')
    #connect = cms.string('frontier://PromptProd/CMS_COND_31X_BEAMSPOT')
    rnewfile.write('''
                                        )

process.source = cms.Source("EmptySource",
        numberEventsInRun = cms.untracked.uint32(1),
''')
    rnewfile.write('  firstRun = cms.untracked.uint32('+ run + ')\n')
    rnewfile.write('''               
)

process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32(1)
)
process.beamspot = cms.EDFilter("BeamSpotFromDB")


process.p = cms.Path(process.beamspot)

''')
        
    rnewfile.close()
    status_rDB = commands.getstatusoutput('cmsRun '+ readdb_out)
    
    outtext = status_rDB[1]
    print outtext

    #### CLEAN up
    os.system("rm "+ readdb_out)

    print "DONE.\n"
    
#_________________________________    
if __name__ =='__main__':
        sys.exit(main())
        