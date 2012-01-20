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

from queue import PersistantQueue


class JobQueue(PersistantQueue):
    """
    File d'attente persistante des jobs de crawl.
    """
    __lock__ = "job_queue.lock"
    __dir__ = "job_queue"
    

if __name__ == "__main__":
    U = ["a", "a", "b", "c", "d", "e"]
    V = ["http://twitter.com/mentatseb", "http://twitter.com/Gephi", "http://twitter.com/mathieubastian", "fail", "\"#!\""]
    queue = JobQueue()
    queue.put("twitter.com/jacomyal")
    for element in V:
        if not queue.isLocked():
            queue.put(element)
    if not queue.isLocked():
        print queue.get()
        print queue.get()    
        print queue.get()
        print queue.get()
        print queue.get()
        print queue.get()
        print queue.get()

