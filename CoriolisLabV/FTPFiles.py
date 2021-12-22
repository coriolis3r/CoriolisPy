import ftplib

try:
    filename= "NetworkConfig.conf"

    ftp= ftplib.FTP('win5146.site4now.net')
    ftp.login('keepener-001', 'Keepener.15zz,')
    ftp.cwd('/site12/ftpTest/')

    #ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)

    uploadfile= open('/etc/wpa_supplicant/wpa_supplicant.conf', 'rb')

    ftp.storbinary('STOR ' + filename, uploadfile)

    ftp.delete("elemsa.txt")

except Exception as e:
    print(e)
