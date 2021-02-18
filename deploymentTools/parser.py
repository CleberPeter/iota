import os
import argparse
import datetime

def parseFileExtension(file, desiredExtension):
    fileSplitted = file.split(".")
    extension = fileSplitted[len(fileSplitted)-1]
    if extension == desiredExtension:
        return True
    else:
        return False

class _parser:
    def __init__(self):
        self.debug = True
        parser = argparse.ArgumentParser(description = 'python tool for iota deployment')
        parser.add_argument('-uuidProject', action = 'store', dest = 'uuidProject', required = True,
                                help = 'universal unique identifier (uuid) of project')
        parser.add_argument('-files', action = 'store', dest = 'files', required = True,
                            help = 'files to deploy (.bin or .py)')
        parser.add_argument('-type', action = 'store', dest = 'type', required = True,
                            help = 'type of update (bin or py)')
        parser.add_argument('-version', action = 'store', dest = 'version', required = True,
                            help = 'version to deploy')
        parser.add_argument('-hostnameBroker', action = 'store',  dest = 'hostnameBroker', required = False, 
                             help = 'hostname broker', default = 'localhost')
        parser.add_argument('-portBroker', action = 'store',  dest = 'portBroker', required = False, 
                             help = 'port broker', default = 1883)
        parser.add_argument('-dateExpiration', action = 'store',  dest = 'dateExpiration', required = True, 
                             help = 'date expiration')
        parser.add_argument('-debug', action = 'store',  dest = 'debug', required = False, 
                             help = 'debug', default = "False")
        parser.add_argument('-authorPrivateKey', action = 'store',  dest = 'authorPrivateKey', required = False, 
                             help = 'ECDSA-256b private key from author', default = False)
        parser.add_argument('-projectPublicKey', action = 'store',  dest = 'projectPublicKey', required = False, 
                             help = 'RSA-2048b public key from project', default = False)
        self.arguments = parser.parse_args()
        
        if not self.doParse():
            raise Exception("can't parse parameters.")
    
    def printDebug(self, msg):
        if self.debug:
            print('parseArguments: ',  msg)

    def doParse(self):
        self.arguments.filesData = []
        self.arguments.filesSizes = []
        self.arguments.filesNames = []

        if self.arguments.debug.lower() == 'true':
            self.debug = True
        elif self.arguments.debug.lower() == 'false':
            self.debug = False
        else:
            print("debug need to be true or false.")
            return False
        
        self.arguments.debug = self.debug
        self.printDebug("parsing parameters ...")
        self.printDebug("Project: " + self.arguments.uuidProject)

        self.printDebug("parsing file ...")
        if self.arguments.type == "bin":
            if parseFileExtension(self.arguments.files, "bin"):
                try:
                    if file_name[0] == "/":
                        dirPath = ""
                    else:
                        dirPath = os.path.dirname(os.path.realpath(__file__)) + "/"
                    file = open(dirPath+self.arguments.files, "rb")
                except:
                    print("can't open file.")
                    return False
                
                data = file.read()
                self.arguments.filesNames.append("firmware")
                self.arguments.filesData.append(data)
                self.arguments.filesSizes.append(len(data))
                file.close()
            else:
                print("extension file not supported.")
                return False 
        elif self.arguments.type == "py":

            self.arguments.files = self.arguments.files.split(",") # can be multiple files
            
            for file_name in self.arguments.files:

                if not parseFileExtension(file_name, "py"):
                    print("extension file not supported.")
                    return False

                try:
                    if file_name[0] == "/":
                        dirPath = ""
                    else:
                        dirPath = os.path.dirname(os.path.realpath(__file__)) + "/"
                    file = open(dirPath+file_name, "rb")
                except:
                    print("can't open file.")
                    return False
                
                data = file.read()

                file_name_splitted = file_name.split('/') # a/b/file.py
                
                self.arguments.filesNames.append(file_name_splitted[-1])
                self.arguments.filesData.append(data)
                self.arguments.filesSizes.append(len(data))
                file.close()

        else:
            print("type of update not supported.")
            return False

        self.printDebug("files: " + str(self.arguments.filesNames))
        self.printDebug("files size: " + str(self.arguments.filesSizes))
        
        try:
            self.arguments.version = int(self.arguments.version)
        except:
            print("version need to be an integer.")
            return False
        
        self.printDebug("version: " + str(self.arguments.version))
        self.printDebug("hostnameBroker: " + self.arguments.hostnameBroker)
        
        try:
            self.arguments.portBroker = int(self.arguments.portBroker)
        except:
            print("port broker need to be an integer.")
            return False
        
        self.printDebug("portBroker: " + str(self.arguments.portBroker))

        try:
            datetime.datetime.strptime(self.arguments.dateExpiration, '%Y-%m-%d')
        except ValueError:
            print("incorrect data expiration format, should be YYYY-MM-DD.")
            return False

        self.printDebug("dateExpiration: " + str(self.arguments.dateExpiration))
        
        if not self.arguments.authorPrivateKey == False:

            if len(self.arguments.authorPrivateKey) == 64: # ECDSA SECP256k1 private key size
                self.printDebug("authorPrivateKey: " + str(self.arguments.authorPrivateKey))
                self.arguments.authorPrivateKey = bytes.fromhex(self.arguments.authorPrivateKey)

                if not self.arguments.projectPublicKey == False:
                    if len(self.arguments.projectPublicKey) == 540: # RSA-2048 public key size
                        self.printDebug("projectPublicKey: " + str(self.arguments.projectPublicKey))
                        self.arguments.projectPublicKey = bytes.fromhex(self.arguments.projectPublicKey)
                    else:
                        print("invalid RSA project public key size.")
                        return False
                else:
                    print("missing RSA project public key.")
                    return False

            else:
                print("invalid ECDSA author private key size.")
                return False

        return True        
        