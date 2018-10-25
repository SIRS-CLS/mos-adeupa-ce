# -*- coding: utf-8 -*-
def classFactory(iface):
    from socle_mos_plugin import SocleMos
    return SocleMos(iface)
