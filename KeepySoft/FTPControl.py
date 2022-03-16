import ftplib

try:
    filename= "NetworkConfig.zip"

    ftp= ftplib.FTP('win5146.site4now.net')
    ftp.login('keepener-001', 'Keepener.15zz,')
    ftp.cwd('/FTPCacao/')

    #ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)

    #uploadfile= open('/etc/wpa_supplicant/wpa_supplicant.conf', 'rb')
    uploadfile = open('C:/Users/RENE/Documents/DeleteduplicatedValues.zip', 'rb')

    ftp.storbinary('STOR ' + filename, uploadfile)

    #ftp.delete("elemsa.txt")

except Exception as e:
    print(e)