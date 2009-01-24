#!/usr/bin/env python
# Copyright 2004-2008 Roman Joost <roman@bromeco.de> - Rotterdam, Netherlands
# this file is part of the python-wifi package - a python wifi library
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import errno
import unittest
import types
from pythonwifi.iwlibs import Wireless, getNICnames
from pythonwifi.flags import modes, IW_ENCODE_RESTRICTED

class TestWireless(unittest.TestCase):

    def setUp(self):
        ifnames = getNICnames()
        self.wifi = Wireless(ifnames[0])
        
    def test_wirelessMethods(self):
        # test all wireless methods that they don't return an error
        # 'getBitrates' and 'getChannelInfo' are not tested here,
        # because they return tuples as a normal result
        methods = ['getAPaddr',
                   'getBitrate',
                   'getEssid',
                   'getFragmentation',
                   'getFrequency',
                   'getMode',
                   'getWirelessName',
                   'getPowermanagement',
                   'getQualityMax',
                   'getQualityAvg',
                   'getRetrylimit',
                   'getRTS',
                   'getSensitivity',
                   'getTXPower',
                   'getStatistics']

        # None of the methods should return a tuple
        for m in methods:
            result = getattr(self.wifi, m)()
            self.assert_(type(result) is not types.TupleType,
                         '%s is a TupleType: %s' % (m, result))
        
        # tuple-returning methods
        methods = ['getBitrates',
                   'getChannelInfo',
                   'getNwids',
                   'commit']

        for m in methods:
            result = getattr(self.wifi, m)()
            self.failIf(len(result) == 2 and result[0] == errno.EINVAL, 
                            "%s: %s" % (m, result[1]))
        # the user is not allowed to run this method
        result = self.wifi.getEncryption()
        
        self.assert_(result[0] == 1)
        # test setMode
        old_mode = self.wifi.getMode()                    # save current mode for later restoration
        self.wifi.setMode('Monitor')
        self.assert_(self.wifi.getMode() == 'Monitor')
        self.wifi.setMode(old_mode)                       # restore mode
        
        # test setEssid
        old_essid = self.wifi.getEssid()                  # save current ESSID for later restoration
        self.wifi.setEssid('Joost')
        self.assert_(self.wifi.getEssid() == 'Joost')
        self.wifi.setEssid(old_essid)                     # restore ESSID
        
        # test setFrequency
        old_freq = self.wifi.getFrequency()               # save current frequency for later restoration
        self.wifi.setFrequency('2.462GHz')
        self.assert_(self.wifi.getFrequency() == '2.462GHz')
        self.wifi.setFrequency(old_freq)                  # restore frequency

        # test setAPaddr - does not work unless AP is real and available
        #old_mac = self.wifi.getAPaddr()                   # save current mac for later restoration
        #self.wifi.setAPaddr('61:62:63:64:65:66')
        #time.sleep(3)                                     # 3 second delay between set and get required
        #self.assert_(self.wifi.getAPaddr() == '61:62:63:64:65:66')
        #self.wifi.setAPaddr(old_mac)                      # restore mac

        # test setEncryption
        old_enc = self.wifi.getEncryption()               # save current encryption for later restoration
        status, result = self.wifi.setEncryption('restricted')
        self.assert_(self.wifi.getEncryption() == 'restricted')
        self.assert_(self.wifi.getEncryption(symbolic=False) \
                        == IW_ENCODE_RESTRICTED+1)
        self.wifi.setEncryption(old_enc)                  # restore encryption

    def test_wirelessWithNonWifiCard(self):
        self.wifi.ifname = 'eth0'
        methods = ['getAPaddr',
                   'getBitrate',
                   'getBitrates',
                   'getChannelInfo',
                   'getEssid',
                   'getFragmentation',
                   'getFrequency',
                   'getMode',
                   'getNwids',
                   'getWirelessName',
                   'getPowermanagement',
                   'getQualityMax',
                   'getQualityAvg',
                   'getRetrylimit',
                   'getRTS',
                   'getSensitivity',
                   'getTXPower',
                   'commit']
    
        for m in methods:
            result = getattr(self.wifi, m)()
            self.assert_(type(result) is types.TupleType)
            self.assertEquals(result[0], errno.EINVAL)
        
        # test setMode
        result = self.wifi.setMode('Monitor')
        self.assertEquals(result[0], errno.EINVAL)
        # test setEssid
        result = self.wifi.setEssid('Joost')
        self.assertEquals(result[0], errno.EINVAL)
        
        # test setFrequency
        result = self.wifi.setFrequency('2.462GHz')
        self.assertEquals(result[0], errno.EINVAL)

        # test setEncryption
        result = self.wifi.setEncryption('restricted')
        self.assertEquals(result[0], errno.EINVAL)

    
    def test_wirelessWithNonExistantCard(self):
        self.wifi.ifname = 'eth5'
        methods = ['getAPaddr',
                   'getBitrate',
                   'getBitrates',
                   'getChannelInfo',
                   'getEssid',
                   'getFragmentation',
                   'getFrequency',
                   'getMode',
                   'getNwids',
                   'getWirelessName',
                   'getPowermanagement',
                   'getQualityMax',
                   'getQualityAvg',
                   'getRetrylimit',
                   'getRTS',
                   'getSensitivity',
                   'getTXPower',
                   'commit']
    
        for m in methods:
            result = getattr(self.wifi, m)()
            self.assert_(type(result) is types.TupleType, 
                         "%s returns not a TupleType: %s" %(m, result))
            self.assertEquals(result[0], errno.ENODEV)
        
        # test setMode
        result = self.wifi.setMode('Monitor')
        self.assertEquals(result[0], errno.ENODEV)
        # test setEssid
        result = self.wifi.setEssid('Joost')
        self.assertEquals(result[0], errno.ENODEV)
        
        # test setFrequency
        result = self.wifi.setFrequency('2.462GHz')
        self.assertEquals(result[0], errno.ENODEV)

        # test setEncryption
        result = self.wifi.setEncryption('restricted')
        self.assertEquals(result[0], errno.ENODEV)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestWireless))
unittest.TextTestRunner(verbosity=2).run(suite)
