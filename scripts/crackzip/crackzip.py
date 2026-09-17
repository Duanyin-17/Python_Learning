import zipfile

def extractFile(z, password):
    try:
        z.extractall(pwd=password)
        print(f'[+] Found password {password}')
    except:
        pass

def main():
    zname = 'tesez.zip'
    dname = 'dpassword.txt'
    zfile = zipfile.ZipFile(zname,'a')
    passFile = open(dname)
    for line in passFile.readlines():
        password = line.strip('\n').encode('utf-8')
        extractFile(zfile, password)

if __name__ == '__main__':
    main()