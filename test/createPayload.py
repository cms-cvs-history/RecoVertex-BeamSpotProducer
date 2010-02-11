#!/usr/bin/env python
#____________________________________________________________
#
#  createPayload
#
# A very simple way to create condition DB payloads
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
	print "\n [usage] createPayload <beamspot file> <tag name> <IOV since> <IOV till=-1=inf> <IOV comment> <destDB=oracle://cms_orcon_prod/CMS_COND_31X_BEAMSPOT>"
	print " e.g. createPayload BeamFitResults_template.txt BeamSpotObjects_2009_v1_express 122745 \"\" \"beam spot for early collisions\" \"oracle://cms_orcon_prod/CMS_COND_31X_BEAMSPOT\"\n"
	sys.exit()

    beam_file = sys.argv[1]
    tagname = sys.argv[2]
    iov_since = ''
    iov_till = ''
    iov_comment = ''
    destDB = 'oracle://cms_orcon_prod/CMS_COND_31X_BEAMSPOT'
    if len(sys.argv) > 3:
        iov_since = sys.argv[3]
    if len(sys.argv) > 4:
        iov_till = sys.argv[4]
        if sys.argv[4] == "-1":
            iov_till = ""
    if len(sys.argv) > 5:
        iov_comment = sys.argv[5]
    if len(sys.argv) > 6:
        destDB = sys.argv[6]
    
    writedb_template = "write2DB_template.py"
    readdb_template = "readDB_template.py"
    sqlite_file = "sqlite_file:"+ tagname +".db"

    #### WRITE sqlite file
    
    print "read input beamspot file: " + beam_file
    
    writedb_out = "write2DB_"+tagname+".py"

    wfile = open(writedb_template)
    wnewfile = open(writedb_out,'w')

    writedb_tags = [('SQLITEFILE',sqlite_file),
                    ('TAGNAME',tagname),
                    ('BEAMSPOTFILE',beam_file)]
    
    for line in wfile:

        for itag in writedb_tags:

            line = line.replace(itag[0],itag[1])

        wnewfile.write(line)

    wnewfile.close()
    print "write sqlite file ..."
    #os.system("cmsRun "+ writedb_out)
        
    status_wDB = commands.getstatusoutput('cmsRun '+ writedb_out)
    #print status_wDB[1]
    
    ##### READ and check sqlite file

    print "read back sqlite file to check content ..."
    
    readdb_out = "readDB_"+tagname+".py"
    
    rfile = open(readdb_template)
    rnewfile = open(readdb_out,'w')
    
    readdb_tags = [('SQLITEFILE',sqlite_file),
                   ('TAGNAME',tagname)]

    for line in rfile:

        for itag in readdb_tags:

            line = line.replace(itag[0],itag[1])

        rnewfile.write(line)

    rnewfile.close()
    status_rDB = commands.getstatusoutput('cmsRun '+ readdb_out)
    
    outtext = status_rDB[1]
    print outtext

    #### CREATE payload files for dropbox
    
    print "create payload card for dropbox ..."

    dropbox_file = tagname+".txt"
    dfile = open(dropbox_file,'w')

    dfile.write('destDB '+ destDB +'\n')
    dfile.write('inputtag' +'\n')
    dfile.write('tag '+ tagname +'\n')
    dfile.write('since ' + iov_since +'\n')
    dfile.write('till ' + iov_till +'\n')
    dfile.write('usertext ' + "\""+ iov_comment +"\"" +'\n')

    dfile.close()

    uuid = commands.getstatusoutput('uuidgen -t')[1]

    commands.getstatusoutput('mv '+tagname+".db "+tagname+"@"+uuid+".db")
    commands.getstatusoutput('mv '+tagname+".txt "+tagname+"@"+uuid+".txt")

    #### CLEAN up
    os.system("rm "+ writedb_out)
    os.system("rm "+ readdb_out)

    print "DONE.\n"
    print "Files ready to be move to beamspot dropbox:"
    print tagname+"@"+uuid+".db"
    print tagname+"@"+uuid+".txt"
    
#_________________________________    
if __name__ =='__main__':
        sys.exit(main())
        
