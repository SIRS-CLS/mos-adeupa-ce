# -*- coding: utf-8 -*-
def classFactory(iface):
    from socle_mos_plugin import socle_mos
    return socle_mos(iface)
