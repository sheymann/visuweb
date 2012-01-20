# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
File d'attente persistante.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import os.path
import re
from logger import Logger


class PersistantMultimap(object):
    """
    Mémoire clé-valeur persistante basée sur le système de fichiers.
    On stocke les valeurs de chaque clé dans un fichier du nom de la clé.
    Aucun cache n'est implémenté.
    Classe générique.
    """
    def __init__(self):
        self.__logger__ = Logger(self.__class__.__name__)
    
    def __len__(self):
        return len(os.listdir(self.__dir__))
    
    def __getitem__(self, key):
        self.__createLock__()
        values = list()
        filepath = os.path.join(self.__dir__, self.__cleanName__(key))
        if os.path.exists(filepath):
            with open(filepath) as f:
                values = filter(None, f.read().splitlines())
        self.__logger__.info("get: %s", key)
        self.__removeLock__()
        return values
    
    def __setitem__(self, key, value):
        self.__createLock__()
        path = os.path.join(self.__dir__, self.__cleanName__(key))
        f = open(path, 'a')
        f.write(value+"\n")
        f.close()
        self.__logger__.info("put: %s, %s", key, value)
        self.__removeLock__()
    
    def __delitem__(self, key):
        self.__createLock__()
        filepath = os.path.join(self.__dir__, self.__cleanName__(key))
        if os.path.exists(filepath):
            os.remove(filepath)
        self.__removeLock__()
    
    def __has_key__(self, key):
        filepath = os.path.join(self.__dir__, self.__cleanName__(key))
        return os.path.exists(filepath)
    
    def __createLock__(self):
        if not os.path.exists(self.__lock__):
            f = open(self.__lock__, 'w')
            f.close()
        else:
            self.__logger__.warn("Lock requested but a lock already exists.")

    def __removeLock__(self):
        if os.path.exists(self.__lock__):
            os.remove(self.__lock__)
        else:
            self.__logger__.warn("Unlock requested but no lock is found.")

    def __cleanName__(self, url):
        fname = re.sub('^https?://','',url.lower())
        fname = re.sub('[^A-Za-z0-9]', '_', fname)
        return fname
    
    def isLocked(self):
        return os.path.exists(self.__lock__)

    def put(self, key, value):
        self.__setitem__(key, value)

    def getAll(self, key):
        """
        Get the list of values for a specified key.
        The returned list may contain duplicates.
        """
        return self.__getitem__(key)

    def remove(self, key):
        self.__delitem__(key)

    class StorageException(Exception):
        pass

