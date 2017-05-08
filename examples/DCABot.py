#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Made by Jean-Baptiste Pleynet
# Dollar cost averaging strategy : Use this to regularly buy or sell, in buy & hold objective



import krakenex
import sys

texte_key_file = "KEY FILE:"
texte_pair = "PAIR:"
texte_type = "TYPE:"
texte_volume = "VOLUME:"
succed_string = "result"
error_string_title = "\n**** ERROR ****"

#print('Argument List:' + str(sys.argv))
assert len(sys.argv) == 2

fichier_config = sys.argv[1]

file = open(fichier_config, "r") 
data = file.readlines() 

trouve_key_file = False
trouve_pair = False
trouve_type = False
trouve_volume = False

chaine_erreur = ""

for ligne in data:
    #print(ligne)
    
    if ligne[:len(texte_key_file)] == texte_key_file:
        trouve_key_file = True
        key_file = ligne[len(texte_key_file):(len(ligne)-1)]
        
    if ligne[:len(texte_pair)] == texte_pair:
        trouve_pair = True
        pair = ligne[len(texte_pair):(len(ligne)-1)]
        
    if ligne[:len(texte_type)] == texte_type:
        trouve_type = True
        typ = ligne[len(texte_type):(len(ligne)-1)]
        
    if ligne[:len(texte_volume)] == texte_volume:
        trouve_volume = True
        volume = ligne[len(texte_volume):(len(ligne)-1)]
        
    if trouve_key_file and trouve_pair and trouve_type and trouve_volume:
        k = krakenex.API()
        k.load_key(key_file)

        res = k.query_private('AddOrder', {'pair': pair,
                             'type': typ,
                             'ordertype': 'market',
                             'oflags': 'viqc',
                             'volume': volume})
        
        print(res)
        
        trouve_key_file = False
        trouve_pair = False
        trouve_type = False
        trouve_volume = False
        
        if not succed_string in res:
            chaine_erreur = chaine_erreur + "pair : " + pair + ", type : " + typ + ", volume : " + volume + ", result : '" + str(res) + "\n"
                              
                              
if chaine_erreur != "":
    print(error_string_title)
    print(chaine_erreur)
    input("Error, press Enter to close...")
