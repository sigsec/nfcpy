# -*- coding: latin-1 -*-
# -----------------------------------------------------------------------------
# Copyright 2014 Stephen Tiedemann <stephen.tiedemann@gmail.com>
#
# Licensed under the EUPL, Version 1.1 or - as soon they 
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# http://www.osor.eu/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# -----------------------------------------------------------------------------

import logging
log = logging.getLogger(__name__)

import os

from . import tt1

def activate(clf, target):
    hrom = clf.exchange("\x78\x00\x00\x00\x00\x00\x00", timeout=0.01)[0:2]
    if hrom == "\x11\x48":
        return Topaz96(clf, target)
    if hrom == "\x12\x4C":
        return Topaz512(clf, target)
    return None

class Topaz96(tt1.Type1Tag):
    def __init__(self, clf, target):
        super(Topaz96, self).__init__(clf, target)
        self._product = "Topaz-96 (IRT-5011)"

    def dump(self):
        return super(Topaz96, self)._dump(stop=15)

    def _format(self, version, wipe):
        tag_memory = tt1.Type1TagMemoryReader(self)
        tag_memory[8:14] = "\xE1\x10\x0E\x00\x03\x00"
        if wipe is not None:
            tag_memory[14:104] = 90 * chr(wipe & 0xFF)
        tag_memory.synchronize()

class Topaz512(tt1.Type1Tag):
    def __init__(self, clf, target):
        super(Topaz512, self).__init__(clf, target)
        self._product = "Topaz-512 (TPZ-505-016)"

    def dump(self):
        return super(Topaz96, self)._dump(stop=64)
        
    def _format(self, version, wipe):
        tag_memory = tt1.Type1TagMemoryReader(self)
        tag_memory[ 8:16] = ("E1103F00" "0103F230").decode("hex")
        tag_memory[16:24] = ("330203F0" "02030300").decode("hex")
        if wipe is not None:
            tag_memory[ 24:104] =  80 * chr(wipe & 0xFF)
            tag_memory[128:512] = 384 * chr(wipe & 0xFF)
        tag_memory.synchronize()

