import ftplib
import logging
import os
from datetime import datetime

try:
    cntTry = 0

    ftp = ftplib.FTP('win5146.site4now.net')
    ftp.login('keepener-001', 'Keepener.15zz,')
    ftp.cwd('/FTPCacao/')

    while cntTry < 5:
        try:
            lzf = os.listdir('C:/Users/RENE/Documents/RRRFiles/ArchRen/Montecitos/Coriolis/KeepySoft/ZipFiles')[:10]

            if len(lzf) > 0:

                for fn in lzf:
                    filenameL = 'C:/Users/RENE/Documents/RRRFiles/ArchRen/Montecitos/Coriolis/KeepySoft/ZipFiles/' + fn
                    uploadfile = open(filenameL, 'rb')
                    ftp.storbinary('STOR ' + fn, uploadfile)

                cntTry += 1
            else:
                cntTry = 10

        except Exception as e:
            logging.info("Error SendZipFilesFTP: %s, %s" % (e, datetime.today()))

except Exception as e:
    logging.info("Error SendZipFilesFTP: %s, %s" % (e, datetime.today()))