# -*- coding: utf-8 -*-
def classFactory(iface):
    from .socle_mos_plugin import Mos_Adeupa
    return Mos_Adeupa(iface)
