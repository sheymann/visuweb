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
from logger import Logger


class PersistantQueue(object):
    """
    File d'attente persistante.
    Une file d'attente est un dossier système dont chaque fichier contient le nom d'un élément.
    Ces fichiers ont pour nom le numéro correspond au nième élément ajouté par un producteur.
    Un consommateur supprime le fichier de plus petit numéro et retourne son contenu.
    """
    def __init__(self):
        self.__logger__ = Logger(self.__class__.__name__)
        self.__queueCopy__ = dict()
        queue = os.listdir(self.__dir__);
        if queue:
            for number in queue:
                with open(os.path.join(self.__dir__, str(number)), 'r') as f:
                    item = f.read()
                    self.__queueCopy__[item] = 0
    
    def __len__(self):
        return len(self.__queueCopy__ )
    
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

    def isLocked(self):
        return os.path.exists(self.__lock__)

    def put(self, item):
        """Add a item and give it a queue number"""
        #ignore request if the item is in the queue and if a gexf exists.
        #note that it is not reliable (many queues can be used in parallel)
        gexf = item.lower()+".gexf"
        path = os.path.join("static", gexf)
        if self.__queueCopy__.has_key(item) and os.path.exists(path):
            return
        self.__createLock__()
        self.__queueCopy__[item] = 0
        queue = os.listdir(self.__dir__)
        queue.sort(reverse=True)
        number = 0
        if queue:
            number = int(queue[0]) + 1
        with open(os.path.join(self.__dir__, str(number)), 'w') as f:
            f.write(item)
        self.__logger__.info("put: %s, %s", str(number), item)
        self.__removeLock__()

    def get(self):
        """Delete the item with the smallest queue number"""
        self.__createLock__()
        queue = os.listdir(self.__dir__)
        if not queue:
            self.__removeLock__()
            raise self.EmptyException("No item to get.")
        queue.sort()
        number = queue[0]
        filepath = os.path.join(self.__dir__, number)
        if not os.path.exists(filepath):
            self.__removeLock__()
            raise self.StorageException("No file "+filepath+" is associated to the item number "+number)
        with open(filepath) as f:
            item = f.read()
            os.remove(filepath)
            if self.__queueCopy__.has_key(item):
                del self.__queueCopy__[item]
            self.__logger__.info("get: %s, %s", str(number), item)
        self.__removeLock__()
        return item

    class EmptyException(Exception):
        pass
    class StorageException(Exception):
        pass

