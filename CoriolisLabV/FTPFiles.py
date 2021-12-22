import ftplib

#import os
#os.system('sudo reboot now')

try:
    filename= "elemsa.txt"

    ftp= ftplib.FTP('ftp.smarterasp.net')
    ftp.login('keepener-001', 'Admin.15zz,')
    ftp.cwd('/site12/ftpTest/')

    ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)

    uploadfile= open('C:/Users/RENE/Documents/RRRFiles/prueba.txt', 'rb')

    ftp.storlines('STOR ' + filename, uploadfile)

except Exception as e:
    print(e)
