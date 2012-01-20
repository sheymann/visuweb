# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
File d'attente des notifications de création de visualisation.
Key = référence de la map
Value = Twitter username

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

from multimap import PersistantMultimap


class NotificationMultimap(PersistantMultimap):
    """
    Mémoire clé-valeur persistante basée sur le système de fichiers.
    On stocke les valeurs de chaque clé dans un fichier du nom de la clé.
    """
    __lock__ = "notification_map.lock"
    __dir__ = "notification_map"


if __name__ == "__main__":
    nm = NotificationMultimap()
    while nm.isLocked():
        sleep(0.1)
    
    nm.put("twitter.com/jacomyal", "mentatseb")
    nm["twitter.com/jacomyal"] = "mentatseb2"
    
    values = nm.getAll("twitter.com/jacomyal")
    values2 = nm["twitter.com/jacomyal"]
    
    #nm.remove("twitter.com/jacomyal")
    del nm["twitter.com/jacomyal"]
    
    assert values == values2
    print(values)

