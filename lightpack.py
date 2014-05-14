# pylint: disable=C0103,C0301

import socket, time, imaplib, re, sys

class lightpack(object):
    '''Python API for the lightpack software'''

    def __init__(self, _host, _port, _apikey, _ledMap):
        '''
        _host = '127.0.0.1'              # The remote host
        _port = 3636                     # The same port as used by the server
        _ledmap = [1,2,3,4,5,6,7,8,9,10] # mapped LEDs
        '''
        self.host = _host
        self.port = _port
        self.apikey = _apikey
        self.ledMap = _ledMap
        self.connection = ""

    def connect(self):
        '''Connect to the lightpack server API'''

        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.host, self.port))
            self.__readResult()
            cmd = 'apikey:' + self.apikey + '\n'
            self.connection.send(cmd)
            self.__readResult()
            return 0
        except:
            print 'Lightpack API server is missing'
            return -1

    def disconnect(self):
        '''Disconnect from the lightpack server API'''

        self.unlock()
        self.connection.close()

    def __readResult(self):
        '''Return last-command API answer (call in every local method)'''

        total_data = []
        data = self.connection.recv(8192)
        total_data.append(data)
        return ''.join(total_data)

    def getProfiles(self):
        '''Get the list of available profiles'''

        cmd = 'getprofiles\n'
        self.connection.send(cmd)
        profiles = self.__readResult()
        return profiles.split(':')[1].rstrip(';\n').split(';')

    def getProfile(self):
        '''Get the current profile'''

        cmd = 'getprofile\n'
        self.connection.send(cmd)
        profile = self.__readResult()
        profile = profile.split(':')[1]
        return profile

    def getStatus(self):
        '''Get the current status'''

        cmd = 'getstatus\n'
        self.connection.send(cmd)
        status = self.__readResult()
        status = status.split(':')[1]
        return status

    def getAPIStatus(self):
        '''Get the current API status'''

        cmd = 'getstatusapi\n'
        self.connection.send(cmd)
        status = self.__readResult()
        status = status.split(':')[1]
        return status

    def setColor(self, num, red, green, blue):
        '''Set color to the define LED'''

        cmd = 'setcolor:{0}-{1},{2},{3}\n'. \
            format(self.ledMap[num-1], red, green, blue)
        self.connection.send(cmd)
        self.__readResult()

    def setColorToAll(self, red, green, blue):
        '''Set one color to all LEDs'''

        cmdstr = ''
        for i in self.ledMap:
            cmdstr = str(cmdstr) + str(i) + '-{0},{1},{2};'. \
                format(red, green, blue)
        cmd = 'setcolor:' + cmdstr + '\n'
        self.connection.send(cmd)
        self.__readResult()

    def setGamma(self, gamma):
        '''Control the level of saturation'''

        cmd = 'setgamma:{0}\n'.format(gamma)
        self.connection.send(cmd)
        self.__readResult()

    def setSmooth(self, steps):
        '''Define how many steps the color will be changed'''

        cmd = 'setsmooth:{0}\n'.format(steps)
        self.connection.send(cmd)
        self.__readResult()

    def setProfile(self, p):
        '''Set the current running profile'''

        cmd = 'setprofile:%s\n' % p
        self.connection.send(cmd)
        self.__readResult()

    def lock(self):
        '''Lock'''

        cmd = 'lock\n'
        self.connection.send(cmd)
        self.__readResult()

    def unlock(self):
        '''Unlock'''

        cmd = 'unlock\n'
        self.connection.send(cmd)
        self.__readResult()

    def turnOn(self):
        '''Turn on the lights'''

        cmd = 'setstatus:on\n'
        self.connection.send(cmd)
        self.__readResult()

    def turnOff(self):
        '''Turn off the lights'''

        cmd = 'setstatus:off\n'
        self.connection.send(cmd)
        self.__readResult()
