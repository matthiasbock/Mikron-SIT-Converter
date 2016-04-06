#!/usr/bin/python

import sys
from sit import SIT

sit = SIT(sys.argv[1])
sit.saveas(sys.argv[1][:-3]+".png", "PNG")
