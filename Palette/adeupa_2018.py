DEBUGMODE = True
# -*- coding: utf-8 -*-
"""
Les formulaires QGIS peuvent avoir une fonction Python qui sera appelée à l'ouverture du formulaire.

Utilisez cette fonction pour ajouter plus de fonctionnalités à vos formulaires.

Entrez le nom de la fonction dans le champ "Fonction d'initialisation Python".
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTextEdit, QFont, QTextDocument, QBrush, QColor, QTextCharFormat, QTextTable, QTextTableFormat
from qgis.gui import QgsMessageBar
from PyQt4.QtGui import QProgressBar
from ConfigParser import SafeConfigParser
import ConfigParser
import sys
import os
from qgis.gui import QgsAttributeDialog


from qgis.PyQt.QtWidgets import QWidget

def ouvrir_formulaire_adeupa(dialog, layer, feature):
    global myDialog
    myDialog = dialog
    
    global lay
    lay = layer

    global booedition
    booedition = False

    global buttonBox
    buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")


    # Disconnect the signal that QGIS has wired up for the dialog to the button box.
    buttonBox.accepted.disconnect(myDialog.accept)
    
    # Wire up our own signals.
    buttonBox.accepted.connect(validate)
    #buttonBox.rejected.connect(myDialog.reject)
    
    buttonBox.rejected.connect(ne_pas_valider)



    global nomchamp_code4_2005, nomchamp_code4_2012, nomchamp_code4_2018, nomchamp_subdi_sirs, nomchamp_revise, nomchamp_control
    global control_classe1, control_classe2, control_classe3, control_classe4, control_classe5, control_classe6, control_classe7, control_classe8, control_classe9, control_classe10
    global control_classe11, control_classe12, control_classe13, control_classe14, control_classe15, control_classe16, control_classe17, control_classe18, control_classe19, control_classe20
    global control_classe21, control_classe22, control_classe23, control_classe24, control_classe25, control_classe26, control_classe27, control_classe28, control_classe29, control_classe30
    global control_classe31, control_classe32, control_classe33, control_classe34, control_classe35, control_classe36, control_classe37, control_classe38

    global control_classe39, control_classe40, control_classe41, control_classe42, control_classe43, control_classe44  # subdi_sirs = a, b, c, d, e ou f

    global control_pushButtonSurface

    global control_code4_2005, control_code4_2012, control_code4_2018, control_subdi_sirs
    global control_surface, control_remarque_2018, control_remarque_2012, control_remarque_2005
    global control_rb2005, control_rb2012, control_rb2018

    


    
    nomchamp_code4_2005 = "code4_2005"
    nomchamp_code4_2012 = "code4_2012"
    nomchamp_code4_2018 = "code4_2018"
    nomchamp_subdi_sirs = "subdi_sirs"
    nomchamp_remarque_2018 = "remarque_2018"
    nomchamp_remarque_2012 = "remarque_2012"
    nomchamp_remarque_2005 = "remarque_2005"
    


    #geom = feature.geometry()
    

    
    # definition des variables qui pointent vers les textboxes des codes par annee . Attention, il faut que le nom des controles soient le meme que le nom des champs attributaires
    
    control_code4_2005 = myDialog.findChild(QWidget, nomchamp_code4_2005)
    control_code4_2012 = myDialog.findChild(QWidget, nomchamp_code4_2012)
    control_code4_2018 = myDialog.findChild(QWidget, nomchamp_code4_2018)
    control_subdi_sirs = myDialog.findChild(QWidget, nomchamp_subdi_sirs)
    control_remarque_2018= myDialog.findChild(QWidget, nomchamp_remarque_2018)
    control_remarque_2012= myDialog.findChild(QWidget, nomchamp_remarque_2012)
    control_remarque_2005= myDialog.findChild(QWidget, nomchamp_remarque_2005)

    
    control_surface = myDialog.findChild(QWidget, 'surf_m2')
    
    
    
    # definition des variables qui pointent vers les radio boutons par annee
    
    control_rb2005 = myDialog.findChild(QWidget, "rb2005")
    control_rb2012 = myDialog.findChild(QWidget, "rb2012")
    control_rb2018 = myDialog.findChild(QWidget, "rb2018")

           

    control_classe1 = myDialog.findChild(QWidget, "classe1")
    control_classe2 = myDialog.findChild(QWidget, "classe2")
    control_classe3 = myDialog.findChild(QWidget, "classe3")
    control_classe4 = myDialog.findChild(QWidget, "classe4")
    control_classe5 = myDialog.findChild(QWidget, "classe5")
    control_classe6 = myDialog.findChild(QWidget, "classe6")
    control_classe7 = myDialog.findChild(QWidget, "classe7")
    control_classe8 = myDialog.findChild(QWidget, "classe8")
    control_classe9 = myDialog.findChild(QWidget, "classe9")
    control_classe10 = myDialog.findChild(QWidget, "classe10")
    control_classe11 = myDialog.findChild(QWidget, "classe11")
    control_classe12 = myDialog.findChild(QWidget, "classe12")
    control_classe13 = myDialog.findChild(QWidget, "classe13")
    control_classe14 = myDialog.findChild(QWidget, "classe14")
    control_classe15 = myDialog.findChild(QWidget, "classe15")
    control_classe16 = myDialog.findChild(QWidget, "classe16")
    control_classe17 = myDialog.findChild(QWidget, "classe17")
    control_classe18 = myDialog.findChild(QWidget, "classe18")
    control_classe19 = myDialog.findChild(QWidget, "classe19")
    control_classe20 = myDialog.findChild(QWidget, "classe20")
    control_classe21 = myDialog.findChild(QWidget, "classe21")
    control_classe22 = myDialog.findChild(QWidget, "classe22")
    control_classe23 = myDialog.findChild(QWidget, "classe23")
    control_classe24 = myDialog.findChild(QWidget, "classe24")
    control_classe25 = myDialog.findChild(QWidget, "classe25")
    control_classe26 = myDialog.findChild(QWidget, "classe26")
    control_classe27 = myDialog.findChild(QWidget, "classe27")
    control_classe28 = myDialog.findChild(QWidget, "classe28")
    control_classe29 = myDialog.findChild(QWidget, "classe29")
    control_classe30 = myDialog.findChild(QWidget, "classe30")
    control_classe31 = myDialog.findChild(QWidget, "classe31")
    control_classe32 = myDialog.findChild(QWidget, "classe32")
    control_classe33 = myDialog.findChild(QWidget, "classe33")
    control_classe34 = myDialog.findChild(QWidget, "classe34")
    control_classe35 = myDialog.findChild(QWidget, "classe35")
    control_classe36 = myDialog.findChild(QWidget, "classe36")
    control_classe37 = myDialog.findChild(QWidget, "classe37")
    control_classe38 = myDialog.findChild(QWidget, "classe38")

    control_classe39 = myDialog.findChild(QWidget, "classe39")
    control_classe40 = myDialog.findChild(QWidget, "classe40")
    control_classe41 = myDialog.findChild(QWidget, "classe41")
    control_classe42 = myDialog.findChild(QWidget, "classe42")
    control_classe43 = myDialog.findChild(QWidget, "classe43")
    control_classe44 = myDialog.findChild(QWidget, "classe44")

    # control_pushButtonSurface = myDialog.findChild(QWidget, "pushButtonSurface")
    

    


    
    #qgis.utils.iface.messageBar().pushMessage("Erreur", u"Vous devez sélectionner une couche vecteur dans la TOC", level=QgsMessageBar.CRITICAL, duration=8)
    lst = [layer,feature]

    affichesurface(lst) # affiche la surface en mètre carré dans le formulaire
    
    if layer.isEditable():
        booedition = True
        control_classe1.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe1]))
        control_classe2.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe2]))
        control_classe3.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe3]))
        control_classe4.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe4]))
        control_classe5.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe5]))
        control_classe6.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe6]))
        control_classe7.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe7]))
        control_classe8.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe8]))
        control_classe9.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe9]))
        control_classe10.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe10]))
        control_classe11.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe11]))
        control_classe12.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe12]))
        control_classe13.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe13]))
        control_classe14.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe14]))
        control_classe15.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe15]))
        control_classe16.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe16]))
        control_classe17.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe17]))
        control_classe18.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe18]))
        control_classe19.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe19]))
        control_classe20.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe20]))
        control_classe21.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe21]))
        control_classe22.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe22]))
        control_classe23.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe23]))
        control_classe24.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe24]))
        control_classe25.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe25]))
        control_classe26.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe26]))
        control_classe27.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe27]))
        control_classe28.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe28]))
        control_classe29.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe29]))
        control_classe30.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe30]))
        control_classe31.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe31]))
        control_classe32.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe32]))
        control_classe33.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe33]))
        control_classe34.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe34]))
        control_classe35.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe35]))
        control_classe36.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe36]))
        control_classe37.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe37]))
        control_classe38.clicked.connect(lambda checked: on_buttonx(checked, [layer,feature,control_classe38]))

        control_classe39.clicked.connect(lambda checked: on_button39(checked, lst))
        control_classe40.clicked.connect(lambda checked: on_button40(checked, lst))
        control_classe41.clicked.connect(lambda checked: on_button41(checked, lst))
        control_classe42.clicked.connect(lambda checked: on_button42(checked, lst))
        control_classe43.clicked.connect(lambda checked: on_button43(checked, lst))
        control_classe44.clicked.connect(lambda checked: on_button44(checked, lst))

        
    

def applique_style_gras_et_couleur_rouge_au_texte(ct):
    #applique le style GRAS(bold) sur le texte dans la QTextEdit
    ct.setTextColor(Qt.red)
    ct.setFontWeight(QtGui.QFont.Bold)




def renseignement_multiple(layer):
    
    nF = layer.selectedFeatureCount()
    if nF > 1:
        
        # prov = layer.dataProvider()
        # nomchamp = prov.fields().field(idx).name()
        # if (nomchamp  == nomchamp_code4_2005r) or (nomchamp  == nomchamp_code_2012e):
        #     qgis.utils.iface.messageBar().pushMessage("Information", u"Le codage multiple sur les dates 2000 ou 2009 n'est pas autorisé.", level=QgsMessageBar.CRITICAL, duration=5)
        #     return

        reply = QMessageBox.question(myDialog, "Message", "Voulez-vous renseigner les " + str(nF) + " polygones selectionnes?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        selectFeats = layer.selectedFeatures()
        
        editCommand = QtCore.QCoreApplication.translate("editcommand", u"Renseignement multiple")
        layer.beginEditCommand(editCommand)
        for f in selectFeats:
            feat = f.id()
            # if control_rb2005.isChecked() is True:
            #     idchampcode4_2005 = layer.fieldNameIndex(nomchamp_code4_2005)
            #     val_code4_2005 = control_code4_2005.toPlainText()
            #     layer.changeAttributeValue(feat, idchampcode4_2005, val_code4_2005)
            if control_rb2018.isChecked() is True:    
                idchampcode4_2018 = layer.fieldNameIndex(nomchamp_code4_2018)
                val_code4_2018 = control_code4_2018.toPlainText()
                layer.changeAttributeValue(feat, idchampcode4_2018, val_code4_2018)
            #idchampsubdi_sirs = layer.fieldNameIndex(nomchamp_subdi_sirs)
            #val_subdi_sirs = control_subdi_sirs.toPlainText()
            #layer.changeAttributeValue(feat, idchampsubdi_sirs, val_subdi_sirs)
            # idchampremarque2005 = layer.fieldNameIndex(nomchamp_remarque_2005)
            # val_remarque2005 = control_remarque_2005.toPlainText()
            # layer.changeAttributeValue(feat, idchampremarque2005, val_remarque2005)
            # idchampremarque2018 = layer.fieldNameIndex(nomchamp_remarque_2018)
            # val_remarque2018 = control_remarque_2018.toPlainText()
            # layer.changeAttributeValue(feat, idchampremarque2018, val_remarque2018)
            

            #layer.triggerRepaint()
        layer.endEditCommand()
        #fermer la fenetre
        #myDialog.parent().close()
    # else :
    #     a =1
    #     print "nF pas superieur a 1"

    layer.removeSelection()



def on_buttonx(checked, lst):
    
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre
    control_classe_x = lst[2]

    if control_rb2005.isChecked() is True:
        idx = layer.fieldNameIndex(nomchamp_code4_2005)
        applique_style_gras_et_couleur_rouge_au_texte(control_code4_2005)
        control_code4_2005.setText(control_classe_x.text())

    if control_rb2012.isChecked() is True:
        idx = layer.fieldNameIndex(nomchamp_code4_2012)
        applique_style_gras_et_couleur_rouge_au_texte(control_code4_2012)
        control_code4_2012.setText(control_classe_x.text())
    
    if control_rb2018.isChecked() is True:
        idx = layer.fieldNameIndex(nomchamp_code4_2018)
        applique_style_gras_et_couleur_rouge_au_texte(control_code4_2018)
        control_code4_2018.setText(control_classe_x.text())

    
    val = control_classe_x.text()
    
    
    #feature = lst[1]
    # renseignement_multiple(layer, idx, valocs, valrevise)
    #layer.removeSelection()
    


    
    

def on_button39(checked, lst):
    
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre

    idx = layer.fieldNameIndex(nomchamp_subdi_sirs)
    applique_style_gras_et_couleur_rouge_au_texte(control_subdi_sirs)
    control_subdi_sirs.setText(control_classe39.text())
    
    val = control_classe39.text()
    
    #feature = lst[1]
    #renseignement_multiple(layer, idx, val)
    #layer.removeSelection()
    
    
def on_button40(checked, lst):
    
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre

    idx = layer.fieldNameIndex(nomchamp_subdi_sirs)
    applique_style_gras_et_couleur_rouge_au_texte(control_subdi_sirs)
    control_subdi_sirs.setText(control_classe40.text())
    
    val = control_classe40.text()
    
    #feature = lst[1]
    #renseignement_multiple(layer, idx, val)
    #layer.removeSelection()
    
def on_button41(checked, lst):
    
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre

    idx = layer.fieldNameIndex(nomchamp_subdi_sirs)
    applique_style_gras_et_couleur_rouge_au_texte(control_subdi_sirs)
    control_subdi_sirs.setText(control_classe41.text())
    

    val = control_classe41.text()
    
    #feature = lst[1]
    #renseignement_multiple(layer, idx, val)
    #layer.removeSelection()


def on_button42(checked, lst):
    
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre

    idx = layer.fieldNameIndex(nomchamp_subdi_sirs)
    applique_style_gras_et_couleur_rouge_au_texte(control_subdi_sirs)
    control_subdi_sirs.setText(control_classe42.text())


    val = control_classe42.text()
    
    #feature = lst[1]
    #renseignement_multiple(layer, idx, val)
    #layer.removeSelection()
    
    

def on_button43(checked, lst):
    
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre

    idx = layer.fieldNameIndex(nomchamp_subdi_sirs)
    applique_style_gras_et_couleur_rouge_au_texte(control_subdi_sirs)
    control_subdi_sirs.setText(control_classe43.text())


    val = control_classe43.text()
    
    #feature = lst[1]
    #renseignement_multiple(layer, idx, val)
    #layer.removeSelection()
    
    

def on_button44(checked, lst):
    
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre

    idx = layer.fieldNameIndex(nomchamp_subdi_sirs)
    applique_style_gras_et_couleur_rouge_au_texte(control_subdi_sirs)
    control_subdi_sirs.setText(control_classe44.text())


    val = control_classe44.text()
    
    #feature = lst[1]
    #renseignement_multiple(layer, idx, val)
    #layer.removeSelection()
    



def affichesurface(lst):
    layer = lst[0]  #premier element dans la liste passe en parametre
    feat = lst[1] #second element dans la liste passe en parametre
    if type(feat.geometry()) != type(None): # pour eviter une erreur lorsqu'on ouvre la table attributaire
        surf = feat.geometry().area()
        st = '%*.*f' % (15, 2, surf)    # formate la surface avec 2 chiffres après la virgule
        control_surface.setText(str(st).strip())
    


def validate():
    # Return the form as accepted to QGIS.
    # myDialog.accept()
    
    deconnexions()

    

    myDialog.parent().accept()

    renseignement_multiple(lay)

    if lay.isEditable():
        enregistrer_mises_a_jour_et_projet(lay)

    #remettreLesVariablesAplat()
    

def ne_pas_valider():

    if booedition == True:
        
        deconnexions()
    myDialog.parent().reject()
    #remettreLesVariablesAplat()

def enregistrer_mises_a_jour_et_projet(layer):
    layer.commitChanges()
    layer.startEditing()
    qgis.utils.iface.actionSaveProject().trigger()

def deconnexions():
       
    control_classe1.clicked.disconnect()
    control_classe2.clicked.disconnect()
    control_classe3.clicked.disconnect()
    control_classe4.clicked.disconnect()
    control_classe5.clicked.disconnect()
    control_classe6.clicked.disconnect()
    control_classe7.clicked.disconnect()
    control_classe8.clicked.disconnect()
    control_classe9.clicked.disconnect()
    control_classe10.clicked.disconnect()
    control_classe11.clicked.disconnect()
    control_classe12.clicked.disconnect()
    control_classe13.clicked.disconnect()
    control_classe14.clicked.disconnect()
    control_classe15.clicked.disconnect()
    control_classe16.clicked.disconnect()
    control_classe17.clicked.disconnect()
    control_classe18.clicked.disconnect()
    control_classe19.clicked.disconnect()
    control_classe20.clicked.disconnect()
    control_classe21.clicked.disconnect()
    control_classe22.clicked.disconnect()
    control_classe23.clicked.disconnect()
    control_classe24.clicked.disconnect()
    control_classe25.clicked.disconnect()
    control_classe26.clicked.disconnect()
    control_classe27.clicked.disconnect()
    control_classe28.clicked.disconnect()
    control_classe29.clicked.disconnect()
    control_classe30.clicked.disconnect()
    control_classe31.clicked.disconnect()
    control_classe32.clicked.disconnect()
    control_classe33.clicked.disconnect()
    control_classe34.clicked.disconnect()
    control_classe35.clicked.disconnect()
    control_classe36.clicked.disconnect()
    control_classe37.clicked.disconnect()
    control_classe38.clicked.disconnect()
    control_classe39.clicked.disconnect()
    control_classe40.clicked.disconnect()
    control_classe41.clicked.disconnect()
    control_classe42.clicked.disconnect()
    control_classe43.clicked.disconnect()
    control_classe44.clicked.disconnect()
    