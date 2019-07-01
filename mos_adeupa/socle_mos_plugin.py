# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qgis.core import *
import os
from .resources import *
from .create_socle import *

class Mos_Adeupa:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Acsio_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Adeupa-MoS')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Adeupa-MoS', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):

        icon_path = ':plugins/mos_adeupa/icons/icon_socle.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Réaliser un socle'),
            callback=self.run,
            parent=self.iface.mainWindow())

      

        # iconCreateSocle = QIcon(os.path.dirname(__file__) + "/icon_socle.png")
        # self.createSocle = QAction(iconCreateSocle, u"Réaliser un socle", self.interface.mainWindow())
        # QObject.connect(self.createSocle, SIGNAL("triggered()"), self.gereActionCreate)

        # iconCompare = QIcon(os.path.dirname(__file__) + "/compare.png")
        # self.compareSocle = QAction(iconCompare, u"Comparer les socles", self.interface.mainWindow())
        # QObject.connect(self.compareSocle, SIGNAL("triggered()"), self.gereActionCompare)

        # iconanalyse = QIcon(os.path.dirname(__file__) + "/analyse.png")
        # self.analyseSocle = QAction(iconanalyse, u"Réaliser une rétroévolution", self.interface.mainWindow())
        # QObject.connect(self.analyseSocle, SIGNAL("triggered()"), self.gereActionAnalyse)
        
        # iconRepair = QIcon(os.path.dirname(__file__) + "/repair.png")
        # self.repairSocle = QAction(iconRepair, u"Réparer les géométries", self.interface.mainWindow())
        # QObject.connect(self.repairSocle, SIGNAL("triggered()"), self.gereActionRepair)
        
        # iconEvol = QIcon(os.path.dirname(__file__) + "/evol.png")
        # self.evolSocle = QAction(iconEvol, u"Réaliser une évolution attributaire", self.interface.mainWindow())
        # QObject.connect(self.evolSocle, SIGNAL("triggered()"), self.gereActionEvol)

        # iconEvol = QIcon(os.path.dirname(__file__) + "/geomevol.png")
        # self.evolGeomSocle = QAction(iconEvol, u"Réaliser une évolution géométrique", self.interface.mainWindow())
        # QObject.connect(self.evolGeomSocle, SIGNAL("triggered()"), self.gereActionEvolGeom)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Adeupa-MoS'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started

        self.dlg = Create_mos()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass