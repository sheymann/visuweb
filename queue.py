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


class Queue:
    """
    File d'attente persistante.
    Une file d'attente est un dossier système dont chaque fichier contient le nom d'un élément.
    Ces fichiers ont pour nom le numéro correspond au nième élément ajouté par un producteur.
    Un consommateur supprime le fichier de plus petit numéro et retourne son contenu.
    """
    __lock__ = "queue.lock"
    __logger__ = Logger("Queue")
    
    def __init__(self):
        self.__queueCopy__ = dict()
        queue = os.listdir("queue");
        if len(queue) != 0:
            for number in queue:
                f = open(os.path.join("queue", str(number)), 'r')
                element = f.read()
                self.__queueCopy__[element] = 0
    
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

    def product(self, element):
        """Add a element and give it a queue number"""
        #ignore request if the element is in the queue and if a gexf exists.
        #note that it is not reliable (many queues can be used in parallel)
        gexf = element.lower()+".gexf"
        path = os.path.join("static", gexf)
        if self.__queueCopy__.has_key(element) and os.path.exists(path):
            return
        self.__createLock__()
        self.__queueCopy__[element] = 0
        queue = os.listdir("queue")
        queue.sort(reverse=True)
        number = 0
        if len(queue) != 0:
            number = int(queue[0]) + 1
        f = open(os.path.join("queue", str(number)), 'w')
        f.write(element)
        f.close
        self.__logger__.info("produced: %s, %s", str(number), element)
        self.__removeLock__()

    def consume(self):
        """Delete the element with the smallest queue number"""
        self.__createLock__()
        queue = os.listdir("queue")
        if len(queue) == 0:
            self.__removeLock__()
            raise Exception("No element in queue to consume.")
        queue.sort()
        number = queue[0]
        filepath = os.path.join("queue", number)
        if not os.path.exists(filepath):
            self.__removeLock__()
            raise Exception("The queue element number "+number+" has no file "+filepath+".")
        f = open(filepath)
        element = f.read()
        f.close()
        os.remove(filepath)
        if self.__queueCopy__.has_key(element):
            del self.__queueCopy__[element]
        self.__logger__.info("consumed: %s, %s", str(number), element)
        self.__removeLock__()
        return element


if __name__ == "__main__":
    U = ["a", "a", "b", "c", "d", "e"]
    V = ["http://twitter.com/mentatseb", "http://twitter.com/Gephi", "http://twitter.com/mathieubastian", "fail", "\"#!\""]
    try:
        queue = Queue()
        queue.product("twitter.com/jacomyal")
        #for element in V:
        #    if not queue.isLocked():
        #        queue.product(element)
        #if not queue.isLocked():
            #queue.consume()
            #queue.consume()    
            #queue.consume()
            #queue.consume()
            #queue.consume()
            #queue.consume()
    except Exception as e:
        Logger("Main").error(e)

