import os
import pandas as pd
import math
import pyomo.environ
import shutil
import urbs
from datetime import datetime
from pyomo.opt.base import SolverFactory
import xlrd
from xlrd import XLRDError

# SCENARIOS
def scenario_base(data):

    year=2017

    pro = data['process']

    pro.loc[('Augsburg', 'Wind'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Wind'), 'cap-up'] = 0

    inv_costs, fix_costs = Wind(year=year)
    pro.loc[('Augsburg', 'Wind'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Wind'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'PV Freiflaeche'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'PV Freiflaeche'), 'cap-up'] = 0

    inv_costs, fix_costs = PV_Freiflaeche(year=year)
    pro.loc[('Augsburg', 'PV Freiflaeche'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'PV Freiflaeche'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'PV Dach'), 'inst-cap'] = 19.961 #https://www.pro-e-augsburg.de/902.php
    pro.loc[('Augsburg', 'PV Dach'), 'cap-up'] = 19.961

    inv_costs, fix_costs = PV_Dach(year=year)
    pro.loc[('Augsburg', 'PV Dach'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'PV Dach'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Laufwasser'), 'inst-cap'] = 15.961 #http://www.erneuerbare-energien.augsburg.de/index.php?id=31919
    pro.loc[('Augsburg', 'Laufwasser'), 'cap-up'] = 15.961

    inv_costs, fix_costs = Laufwasser(year=year)
    pro.loc[('Augsburg', 'Laufwasser'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Laufwasser'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Gasturbine'), 'inst-cap'] = (100*0.3) # Richter, Stephan (2004): Entwicklung einer Methode zur integralen Beschreibung und Optimierung urbaner Energiesysteme. Erste Anwendung am Beispiel Augsburg. Dissertation. Universität Augsburg, Augsburg. Online verfügbar unter opus.bibliothek.uni-augsburg.de, zuletzt geprüft am 13.03.2017.
    pro.loc[('Augsburg', 'Gasturbine'), 'cap-up'] = (100*0.3)

    inv_costs, fix_costs = Gasturbine(year=year)
    pro.loc[('Augsburg', 'Gasturbine'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gasturbine'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'GuD'), 'inst-cap'] = (299.5*0.184) # Richter, Stephan (2004)
    pro.loc[('Augsburg', 'GuD'), 'cap-up'] = (299.5*0.184)

    inv_costs, fix_costs = GuD(year=year)
    pro.loc[('Augsburg', 'GuD'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'GuD'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Heizwerk'), 'inst-cap'] = (99*0.94) # Richter, Stephan (2004)
    pro.loc[('Augsburg', 'Heizwerk'), 'cap-up'] = (99*0.94)

    inv_costs, fix_costs = Heizwerk(year=year)
    pro.loc[('Augsburg', 'Heizwerk'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Heizwerk'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Biogas KWK'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Biogas KWK'), 'cap-up'] = 0

    inv_costs, fix_costs = Biogas_KWK(year=year)
    pro.loc[('Augsburg', 'Biogas KWK'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Biogas KWK'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'inst-cap'] = (34618/8000) #https://www.ava-augsburg.de/die-ava/zahlen-fakten/  Annahme 8000 VLS
    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'cap-up'] = (34618/8000)

    inv_costs, fix_costs = Biogas_Aufbereitung(year=year)
    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Abfall KWK'), 'inst-cap'] = (34*0.25)  # Richter, Stephan (2004)
    pro.loc[('Augsburg', 'Abfall KWK'), 'cap-up'] = (34*0.25)

    inv_costs, fix_costs = Abfall_KWK(year=year)
    pro.loc[('Augsburg', 'Abfall KWK'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Abfall KWK'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Solar dez'), 'inst-cap'] = 6 #http://www.erneuerbare-energien.augsburg.de/index.php?id=31991 Annahme: 500 W/m^2
    pro.loc[('Augsburg', 'Solar dez'), 'cap-up'] = 6

    inv_costs, fix_costs = Solar_dez(year=year)
    pro.loc[('Augsburg', 'Solar dez'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Solar dez'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Solar zentr'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Solar zentr'), 'cap-up'] = 0

    inv_costs, fix_costs = Solar_zentr(year=year)
    pro.loc[('Augsburg', 'Solar zentr'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Solar zentr'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Biomasse KWK'), 'inst-cap'] = 7.66 #https://www.kraftanlagen.com/projekte/biomasseheizkraftwerk-augsburg/
    pro.loc[('Augsburg', 'Biomasse KWK'), 'cap-up'] = 7.66

    inv_costs, fix_costs = Biomasse_KWK(year=year)
    pro.loc[('Augsburg', 'Biomasse KWK'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Biomasse KWK'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Oelkessel'), 'inst-cap'] = 271 # Richter, Stephan (2004) 29% Wäremenachfrage wird gedeckt
    pro.loc[('Augsburg', 'Oelkessel'), 'cap-up'] = 271

    inv_costs, fix_costs = Oelkessel(year=year)
    pro.loc[('Augsburg', 'Oelkessel'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Oelkessel'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Holzkessel'), 'inst-cap'] = 9 # Richter, Stephan (2004) 1% Wäremenachfrage wird gedeckt
    pro.loc[('Augsburg', 'Holzkessel'), 'cap-up'] = 9

    inv_costs, fix_costs = Holzkessel(year=year)
    pro.loc[('Augsburg', 'Holzkessel'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Holzkessel'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Gaskessel'), 'inst-cap'] = 468 # Richter, Stephan (2004) 50% Wäremenachfrage wird gedeckt
    pro.loc[('Augsburg', 'Gaskessel'), 'cap-up'] = 468

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Gaskessel PV'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Gaskessel PV'), 'cap-up'] = 0

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel PV'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel PV'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'inst-cap'] = (4/0.7) #Deckungsgrad GWWP 70%
    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'cap-up'] = (4/0.7)

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'Gaskessel Solar'), 'inst-cap'] = (6/0.3) #Deckungsgrad GWWP 30%
    pro.loc[('Augsburg', 'Gaskessel Solar'), 'cap-up'] = (6/0.3)

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel Solar'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel Solar'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'GWWP'), 'inst-cap'] = 4 #   323 Wasser-Wärmepumpen, Wasser-Wasser Wärmepumpen bei 12,5kW, Leistungszahl 4 http://www.erneuerbare-energien.augsburg.de/index.php?id=31977; http://www.geothermie-zentrum.de/fileadmin/media/geothermiezentrum/Projekte/WP-Studie/Abschlussbericht_WP-Marktstudie_Mar2010.pdfhttp://www.geothermie-zentrum.de/fileadmin/media/geothermiezentrum/Projekte/WP-Studie/Abschlussbericht_WP-Marktstudie_Mar2010.pdf
    pro.loc[('Augsburg', 'GWWP'), 'cap-up'] = 4

    inv_costs, fix_costs = GWWP(year=year)
    pro.loc[('Augsburg', 'GWWP'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'GWWP'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'P2H dez'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'P2H dez'), 'cap-up'] = 0

    inv_costs, fix_costs = P2H_dez(year=year)
    pro.loc[('Augsburg', 'P2H dez'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'P2H dez'), 'fix-cost'] = fix_costs


    pro.loc[('Augsburg', 'P2H zentr'), 'inst-cap'] = 10
    pro.loc[('Augsburg', 'P2H zentr'), 'cap-up'] = 10


    '''
    pro.loc[('Augsburg', 'Slack powerplant'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Netzeinspeisung'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Netzbezug'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'P2H (dez.) Waerme'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'GWWP Waerme'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Solar (dez.) Waerme'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'PV Einspeisung'), 'inst-cap'] = 0
    
    
    
    pro.loc[('Augsburg', 'P2H (zentr.) Waerme'), 'inst-cap'] = 0

    '''
    sto = data['storage']

    inv_costs_p, fix_costs_p, inv_costs_e = Puffer_dez(year=year)

    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H dez'), 'inv_costs_p'] = 0 # Kosten für Heizschwert bereits in Process P2H (dez.) und Gaskssel (PV)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H dez'), 'fix_costs_p'] = 0 # Kosten für Heizschwert bereits in Process P2H (dez.) und Gaskssel (PV)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H dez'), 'inv_costs_c'] = inv_costs_e


    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme Solar dez'), 'inv_costs_p'] = 0 # Kosten für Leistung bereits in Process  Solar (dez.) und Gaskssel (Solar)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme Solar dez'), 'fix_costs_p'] = 0  # Kosten für Leistung bereits in Process Solar (dez.) und Gaskssel (Solar) enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme Solar dez'), 'inv_costs_c'] = inv_costs_e

    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme GWWP'), 'inv_costs_p'] = 0  # Kosten für Leistung bereits in Process  GWWP und Gaskssel (GWWP)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme GWWP'), 'fix_costs_p'] = 0  # Kosten für Leistung bereits in Process GWWP und Gaskssel (GWWP)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme GWWP'), 'inv_costs_c'] = inv_costs_e


    inv_costs_p, fix_costs_p, inv_costs_e = Puffer_zentr(year=year)

    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H zentr'), 'inv_costs_p'] = inv_costs_p
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H zentr'), 'fix_costs_p'] = fix_costs_p
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H zentr'), 'inv_costs_c'] = inv_costs_e


    inv_costs_p, fix_costs_p, inv_costs_e = Batterie(year=year)

    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'inv_costs_p'] = inv_costs_p
    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'fix_costs_p'] = fix_costs_p
    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'inv_costs_c'] = inv_costs_e


    inv_costs_p, fix_costs_p = Waermenetz(year=year)

    sto.loc[('Augsburg', 'Waermenetz', 'Fernwaerme'), 'inv_costs_p'] = inv_costs_p
    sto.loc[('Augsburg', 'Waermenetz', 'Fernwaerme'), 'fix_costs_p'] = fix_costs_p



    return data


def scenario_2017(data):
    global_prop = data['global_prop']
    global_prop.loc['CO2 limit', 'value'] = 1000000



    year = 2017
    dif=0
    file= 'result/Augsburg-20171114T2323/scenario_base.xlsx'


    xls = pd.ExcelFile(file)  # read resultfile
    cpro = xls.parse('Process caps', index_col=[0, 1])


    pro = data['process']

    pro.loc[('Augsburg', 'Wind'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Wind'), 'cap-up'] = 32

    inv_costs, fix_costs = Wind(year=year)
    pro.loc[('Augsburg', 'Wind'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Wind'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'PV Freiflaeche'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'PV Freiflaeche'), 'cap-up'] = math.inf

    inv_costs, fix_costs = PV_Freiflaeche(year=year)
    pro.loc[('Augsburg', 'PV Freiflaeche'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'PV Freiflaeche'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'PV Dach'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'PV Dach'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'PV Dach'), 'depreciation']))/(pro.loc[('Augsburg', 'PV Dach'), 'depreciation']))) # https://www.pro-e-augsburg.de/902.php
    pro.loc[('Augsburg', 'PV Dach'), 'cap-up'] = 380

    inv_costs, fix_costs = PV_Dach(year=year)
    pro.loc[('Augsburg', 'PV Dach'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'PV Dach'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg',
             'Laufwasser'), 'inst-cap'] = 15.961  # http://www.erneuerbare-energien.augsburg.de/index.php?id=31919
    pro.loc[('Augsburg', 'Laufwasser'), 'cap-up'] = 15.961

    inv_costs, fix_costs = Laufwasser(year=year)
    pro.loc[('Augsburg', 'Laufwasser'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Laufwasser'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Gasturbine'), 'inst-cap'] = (
    100 * 0.3)  # Richter, Stephan (2004): Entwicklung einer Methode zur integralen Beschreibung und Optimierung urbaner Energiesysteme. Erste Anwendung am Beispiel Augsburg. Dissertation. Universität Augsburg, Augsburg. Online verfügbar unter opus.bibliothek.uni-augsburg.de, zuletzt geprüft am 13.03.2017.
    pro.loc[('Augsburg', 'Gasturbine'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Gasturbine(year=year)
    pro.loc[('Augsburg', 'Gasturbine'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gasturbine'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'GuD'), 'inst-cap'] = (299.5 * 0.184)  # Richter, Stephan (2004)
    pro.loc[('Augsburg', 'GuD'), 'cap-up'] = math.inf

    inv_costs, fix_costs = GuD(year=year)
    pro.loc[('Augsburg', 'GuD'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'GuD'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Heizwerk'), 'inst-cap'] = (99 * 0.94)  # Richter, Stephan (2004)
    pro.loc[('Augsburg', 'Heizwerk'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Heizwerk(year=year)
    pro.loc[('Augsburg', 'Heizwerk'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Heizwerk'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Biogas KWK'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Biogas KWK'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Biogas_KWK(year=year)
    pro.loc[('Augsburg', 'Biogas KWK'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Biogas KWK'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'inst-cap'] = (
    34618 / 8000)  # https://www.ava-augsburg.de/die-ava/zahlen-fakten/  Annahme 8000 VLS
    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Biogas_Aufbereitung(year=year)
    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Biogas Aufbereitung'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Abfall KWK'), 'inst-cap'] = (34 * 0.25)  # Richter, Stephan (2004)
    pro.loc[('Augsburg', 'Abfall KWK'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Abfall_KWK(year=year)
    pro.loc[('Augsburg', 'Abfall KWK'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Abfall KWK'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg',
             'Solar dez'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'Solar dez'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'Solar dez'), 'depreciation']))/(pro.loc[('Augsburg', 'Solar dez'), 'depreciation'])))
    pro.loc[('Augsburg', 'Solar dez'), 'cap-up'] = 652

    inv_costs, fix_costs = Solar_dez(year=year)
    pro.loc[('Augsburg', 'Solar dez'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Solar dez'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Solar zentr'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Solar zentr'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Solar_zentr(year=year)
    pro.loc[('Augsburg', 'Solar zentr'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Solar zentr'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg',
             'Biomasse KWK'), 'inst-cap'] = 7.66  # https://www.kraftanlagen.com/projekte/biomasseheizkraftwerk-augsburg/
    pro.loc[('Augsburg', 'Biomasse KWK'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Biomasse_KWK(year=year)
    pro.loc[('Augsburg', 'Biomasse KWK'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Biomasse KWK'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Oelkessel'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'Oelkessel'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'Oelkessel'), 'depreciation']))/(pro.loc[('Augsburg', 'Oelkessel'), 'depreciation'])))
    pro.loc[('Augsburg', 'Oelkessel'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Oelkessel(year=year)
    pro.loc[('Augsburg', 'Oelkessel'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Oelkessel'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Holzkessel'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'Holzkessel'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'Holzkessel'), 'depreciation']))/(pro.loc[('Augsburg', 'Holzkessel'), 'depreciation'])))
    pro.loc[('Augsburg', 'Holzkessel'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Holzkessel(year=year)
    pro.loc[('Augsburg', 'Holzkessel'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Holzkessel'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Gaskessel'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'Gaskessel'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'Gaskessel'), 'depreciation']))/(pro.loc[('Augsburg', 'Gaskessel'), 'depreciation'])))
    pro.loc[('Augsburg', 'Gaskessel'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Gaskessel PV'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'Gaskessel PV'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'Gaskessel PV'), 'depreciation']))/(pro.loc[('Augsburg', 'Gaskessel PV'), 'depreciation'])))
    pro.loc[('Augsburg', 'Gaskessel PV'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel PV'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel PV'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'Gaskessel GWWP'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'Gaskessel GWWP'), 'depreciation']))/(pro.loc[('Augsburg', 'Gaskessel GWWP'), 'depreciation'])))
    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel GWWP'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'Gaskessel Solar'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'Gaskessel Solar'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'Gaskessel Solar'), 'depreciation']))/(pro.loc[('Augsburg', 'Gaskessel Solar'), 'depreciation'])))
    pro.loc[('Augsburg', 'Gaskessel Solar'), 'cap-up'] = math.inf

    inv_costs, fix_costs = Gaskessel(year=year)
    pro.loc[('Augsburg', 'Gaskessel Solar'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'Gaskessel Solar'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg',
             'GWWP'), 'inst-cap'] = ((cpro.loc[('Augsburg', 'GWWP'),'Total'])* ((-dif+(pro.loc[('Augsburg', 'GWWP'), 'depreciation']))/(pro.loc[('Augsburg', 'GWWP'), 'depreciation'])))
    pro.loc[('Augsburg', 'GWWP'), 'cap-up'] = math.inf

    inv_costs, fix_costs = GWWP(year=year)
    pro.loc[('Augsburg', 'GWWP'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'GWWP'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'P2H dez'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'P2H dez'), 'cap-up'] = math.inf

    inv_costs, fix_costs = P2H_dez(year=year)
    pro.loc[('Augsburg', 'P2H dez'), 'inv-cost'] = inv_costs
    pro.loc[('Augsburg', 'P2H dez'), 'fix-cost'] = fix_costs

    pro.loc[('Augsburg', 'P2H zentr'), 'inst-cap'] = 10
    pro.loc[('Augsburg', 'P2H zentr'), 'cap-up'] = math.inf

    '''
    pro.loc[('Augsburg', 'Slack powerplant'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Netzeinspeisung'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Netzbezug'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'P2H (dez.) Waerme'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'GWWP Waerme'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'Solar (dez.) Waerme'), 'inst-cap'] = 0
    pro.loc[('Augsburg', 'PV Einspeisung'), 'inst-cap'] = 0



    pro.loc[('Augsburg', 'P2H (zentr.) Waerme'), 'inst-cap'] = 0

    '''
    sto = data['storage']

    inv_costs_p, fix_costs_p, inv_costs_e = Puffer_dez(year=year)

    sto.loc[('Augsburg', 'Pufferspeicher',
             'Waerme P2H dez'), 'inv_costs_p'] = 0  # Kosten für Heizschwert bereits in Process P2H (dez.) und Gaskssel (PV)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher',
             'Waerme P2H dez'), 'fix_costs_p'] = 0  # Kosten für Heizschwert bereits in Process P2H (dez.) und Gaskssel (PV)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H dez'), 'inv_costs_c'] = inv_costs_e

    sto.loc[('Augsburg', 'Pufferspeicher',
             'Waerme Solar dez'), 'inv_costs_p'] = 0  # Kosten für Leistung bereits in Process  Solar (dez.) und Gaskssel (Solar)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher',
             'Waerme Solar dez'), 'fix_costs_p'] = 0  # Kosten für Leistung bereits in Process Solar (dez.) und Gaskssel (Solar) enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme Solar dez'), 'inv_costs_c'] = inv_costs_e

    sto.loc[('Augsburg', 'Pufferspeicher',
             'Waerme GWWP'), 'inv_costs_p'] = 0  # Kosten für Leistung bereits in Process  GWWP und Gaskssel (GWWP)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher',
             'Waerme GWWP'), 'fix_costs_p'] = 0  # Kosten für Leistung bereits in Process GWWP und Gaskssel (GWWP)enthalten
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme GWWP'), 'inv_costs_c'] = inv_costs_e

    inv_costs_p, fix_costs_p, inv_costs_e = Puffer_zentr(year=year)

    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H zentr'), 'inv_costs_p'] = inv_costs_p
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H zentr'), 'fix_costs_p'] = fix_costs_p
    sto.loc[('Augsburg', 'Pufferspeicher', 'Waerme P2H zentr'), 'inv_costs_c'] = inv_costs_e


    inv_costs_p, fix_costs_p, inv_costs_e = Batterie(year=year)

    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'inv_costs_p'] = inv_costs_p
    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'fix_costs_p'] = fix_costs_p
    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'inv_costs_c'] = inv_costs_e

    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'inst-cap-c'] = 0
    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'inst-cap-p'] = 0

    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'cap-up-c'] = math.inf
    sto.loc[('Augsburg', 'Batterie', 'Elec'), 'cap-up-p'] = math.inf

    inv_costs_p, fix_costs_p = Waermenetz(year=year)

    sto.loc[('Augsburg', 'Waermenetz', 'Fernwaerme'), 'inv_costs_p'] = inv_costs_p
    sto.loc[('Augsburg', 'Waermenetz', 'Fernwaerme'), 'fix_costs_p'] = fix_costs_p















    return data


def scenario_stock_prices(data):
    # change stock commodity prices
    co = data['commodity']
    stock_commodities_only = (co.index.get_level_values('Type') == 'Stock')
    co.loc[stock_commodities_only, 'price'] *= 1.5
    return data


def scenario_co2_limit(data):
    # change global CO2 limit
    global_prop = data['global_prop']
    global_prop.loc['CO2 limit', 'value'] *= 0.05
    return data


def scenario_co2_tax_mid(data):
    # change CO2 price in Mid
    co = data['commodity']
    co.loc[('Mid', 'CO2', 'Env'), 'price'] = 50
    return data


def scenario_north_process_caps(data):
    # change maximum installable capacity
    pro = data['process']
    pro.loc[('North', 'Hydro plant'), 'cap-up'] *= 0.5
    pro.loc[('North', 'Biomass plant'), 'cap-up'] *= 0.25
    return data


def scenario_no_dsm(data):
    # empty the DSM dataframe completely
    data['dsm'] = pd.DataFrame()
    return data


def scenario_all_together(data):
    # combine all other scenarios
    data = scenario_stock_prices(data)
    data = scenario_co2_limit(data)
    data = scenario_north_process_caps(data)
    return data


def prepare_result_directory(result_name):
    """ create a time stamped directory within the result folder """
    # timestamp for result directory
    now = datetime.now().strftime('%Y%m%dT%H%M')

    # create result directory if not existent
    result_dir = os.path.join('result', '{}-{}'.format(result_name, now))
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    return result_dir


def setup_solver(optim, logfile='solver.log'):
    """ """
    if optim.name == 'gurobi':
        # reference with list of option names
        # http://www.gurobi.com/documentation/5.6/reference-manual/parameters
        optim.set_options("logfile={}".format(logfile))
        optim.set_options("timelimit=7200")  # seconds
        optim.set_options("mipgap=1e-4")  # default = 1e-4
    elif optim.name == 'glpk':
        # reference with list of options
        # execute 'glpsol --help'
        optim.set_options("log={}".format(logfile))
        # optim.set_options("tmlim=7200")  # seconds
        # optim.set_options("mipgap=.0005")
    else:
        print("Warning from setup_solver: no options set for solver "
              "'{}'!".format(optim.name))
    return optim


def run_scenario(input_file, timesteps, scenario, result_dir,
                 plot_tuples=None, plot_periods=None, report_tuples=None):
    """ run an urbs model for given input, time steps and scenario

    Args:
        input_file: filename to an Excel spreadsheet for urbs.read_excel
        timesteps: a list of timesteps, e.g. range(0,8761)
        scenario: a scenario function that modifies the input data dict
        result_dir: directory name for result spreadsheet and plots
        plot_tuples: (optional) list of plot tuples (c.f. urbs.result_figures)
        plot_periods: (optional) dict of plot periods (c.f. urbs.result_figures)
        report_tuples: (optional) list of (sit, com) tuples (c.f. urbs.report)

    Returns:
        the urbs model instance
    """

    # scenario name, read and modify data for scenario
    sce = scenario.__name__
    data = urbs.read_excel(input_file)
    data = scenario(data)

    # create model
    prob = urbs.create_model(data, timesteps)

    # refresh time stamp string and create filename for logfile
    now = prob.created
    log_filename = os.path.join(result_dir, '{}.log').format(sce)

    # solve model and read results
    optim = SolverFactory('gurobi')  # cplex, glpk, gurobi, ...
    optim = setup_solver(optim, logfile=log_filename)
    result = optim.solve(prob, tee=True)

    # save problem solution (and input data) to HDF5 file
    #urbs.save(prob, os.path.join(result_dir, '{}.h5'.format(sce)))

    # write report to spreadsheet
    urbs.report(
        prob,
        os.path.join(result_dir, '{}.xlsx').format(sce),
        report_tuples=report_tuples)

    # result plots
    urbs.result_figures(
        prob,
        os.path.join(result_dir, '{}'.format(sce)),
        plot_title_prefix=sce.replace('_', ' '),
        plot_tuples=plot_tuples,
        periods=plot_periods,
        figure_size=(24, 9))
    return prob



def Wind(year):

    inv_costs = (6.089e+11)*math.exp((year*(-0.006443)))
    fix_costs = inv_costs*(2/100)

    return inv_costs,fix_costs


def PV_Freiflaeche(year):
    inv_costs = ( 3.185e+24) * math.exp((year * (-0.021)))
    fix_costs = inv_costs * (1.5 / 100)

    return inv_costs, fix_costs

def PV_Dach(year):
    inv_costs = (4.432e+15) * math.exp((year * (-0.01092)))
    fix_costs = inv_costs * (2 / 100)

    return inv_costs, fix_costs

def Laufwasser(year):
    inv_costs = (2.17e+06) * math.exp((year * (0.0004661)))
    fix_costs = inv_costs * (4.5 / 100)

    return inv_costs, fix_costs

def Gasturbine(year):
    inv_costs = (9.088e+06) * math.exp((year * (-0.001092)))
    fix_costs = inv_costs * (5.2 / 100)

    return inv_costs, fix_costs

def GuD(year):
    inv_costs = (2.03e+06 ) * math.exp((year * (0)))
    fix_costs = inv_costs * (5.2 / 100)

    return inv_costs, fix_costs

def Heizwerk(year):

    inv_costs = (153400/0.94) * (year **(0))
    fix_costs = inv_costs * (2 / 100)

    return inv_costs, fix_costs

def Biogas_KWK(year):
    inv_costs = (1.358e+19) * math.exp((year * (-0.01437)))
    fix_costs = inv_costs * (6.1 / 100)

    return inv_costs, fix_costs


def Biogas_Aufbereitung(year):
    inv_costs = (1.458e+14) * math.exp((year * (-0.009123)))
    fix_costs = inv_costs * (6 / 100)

    return inv_costs, fix_costs

def Abfall_KWK(year):
    inv_costs = (3.993e+13) * math.exp((year * (-0.007803)))
    fix_costs = inv_costs * (4.5/ 100)

    return inv_costs, fix_costs

def Solar_dez(year):
    inv_costs = (300000) * math.exp((year * (0)))
    fix_costs = inv_costs * (1.3/ 100)

    return inv_costs, fix_costs

def Solar_zentr(year):
    inv_costs = (190000) * math.exp((year * (0)))
    fix_costs = inv_costs * (1.4/ 100)

    return inv_costs, fix_costs

def Biomasse_KWK(year):
    inv_costs = (4.911e+15) * math.exp((year * (-0.01056)))
    fix_costs = inv_costs * (3.3/ 100)

    return inv_costs, fix_costs

def Oelkessel(year):

    inv_costs = (863000) * (year **(0))
    fix_costs = inv_costs * (1/ 100)

    return inv_costs, fix_costs

def Holzkessel(year):
    inv_costs = (2.528e+11) * math.exp((year *(-0.006021)))
    fix_costs = inv_costs * (2/ 100)

    return inv_costs, fix_costs

def Gaskessel(year):

    inv_costs = (660000) * (year **(0))
    fix_costs = inv_costs * (1/ 100)

    return inv_costs, fix_costs

def GWWP(year):
    inv_costs = (1.218e+11) * math.exp((year * (-0.005767)))
    fix_costs = inv_costs * (4/ 100)

    return inv_costs, fix_costs

def Batterie(year):

    inv_costs_p = (3.47e+55) * math.exp((year * (-0.05709)))
    fix_costs_p = inv_costs_p * (1.4/ 100)
    inv_costs_e = (1.357e+49) * math.exp((year * (-0.04957)))


    return inv_costs_p, fix_costs_p,inv_costs_e


def Waermenetz(year):

    inv_costs_p = (1.044e+09) * math.exp((year * (-0.00354)))
    fix_costs_p = inv_costs_p * (3/ 100)

    return inv_costs_p, fix_costs_p


def Puffer_zentr(year):

    inv_costs_p = (200000) * (year **(0))
    fix_costs_p = inv_costs_p * (1/ 100)
    inv_costs_e = (3869) * (year **(0))


    return inv_costs_p, fix_costs_p,inv_costs_e

def Puffer_dez(year):

    inv_costs_p = (150000) * (year **(0))
    fix_costs_p = inv_costs_p * (1/ 100)
    inv_costs_e = (42992) * (year **(0))

    return inv_costs_p, fix_costs_p,inv_costs_e

def P2H_dez(year):
    inv_costs = (150000) * (year ** (0))
    fix_costs = inv_costs * (1 / 100)



    return inv_costs, fix_costs

if __name__ == '__main__':
    input_file = 'Augsburg.xlsx'
    result_name = os.path.splitext(input_file)[0]  # cut away file extension
    result_dir = prepare_result_directory(result_name)  # name + time stamp
    runme = 'runme.py'

    # copy input file to result directory
    shutil.copyfile(input_file, os.path.join(result_dir, input_file))
    # copy runme.py to result directory
    shutil.copyfile(runme, os.path.join(result_dir, runme))

    # simulation timesteps
    (offset, length) = (0, 100)  # time step selection
    timesteps = range(offset, offset+length+1)

    # plotting commodities/sites
    plot_tuples = [
        ('Augsburg', 'Elec'),
        ('Augsburg', 'Fernwaerme'),
        ('Augsburg', 'Waerme dez'),
        ('Augsburg', 'Waerme Solar dez'),
        ('Augsburg', 'Waerme GWWP'),
        ('Augsburg', 'Waerme P2H zentr'),
        ('Augsburg', 'Elec PV'),
        ('Augsburg', 'Waerme P2H dez'),
        ]

    # detailed reporting commodity/sites
    report_tuples = [
        ('Augsburg', 'Elec'),
        ('Augsburg', 'Fernwaerme'),
        ('Augsburg', 'Waerme dez'),
        ('Augsburg', 'Waerme Solar dez'),

        ('Augsburg', 'Waerme GWWP'),
        ('Augsburg', 'Waerme P2H zentr'),
        ('Augsburg', 'Elec PV'),
        ('Augsburg', 'Waerme P2H dez'),
        ('Augsburg', 'CO2')
        ]

    # plotting timesteps
    plot_periods = {
        'all': timesteps[1:]
    }

    # add or change plot colors
    my_colors = {
        'Augsburg': (230, 200, 200),
        }
    for country, color in my_colors.items():
        urbs.COLORS[country] = color

    # select scenarios to be run
    scenarios = [
        #scenario_base]
        scenario_2017]
        #scenario_co2_limit,
        #scenario_co2_tax_mid,
        #scenario_no_dsm,
        #scenario_north_process_caps,
        #scenario_all_together]

    for scenario in scenarios:
        prob = run_scenario(input_file, timesteps, scenario, result_dir,
                            plot_tuples=plot_tuples,
                            plot_periods=plot_periods,
                            report_tuples=report_tuples)

