# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Snippet to generate a cookie for Tornado.
"""

import base64
import uuid

base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

