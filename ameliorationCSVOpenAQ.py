# -*- coding: utf-8 -*-
"""
Created on Fri May 23 01:01:36 2025

@author: Cytech
"""
import pandas as pd
import time  # pour éviter de surcharger l'API
import requests

def get_nearest_station_measurements(lat, lon, radius=10000, parameters=["pm10", "pm25", "no2", "o3"], api_key=None, verbose=False):
    """
    Étape 1 : Trouve la station OpenAQ la plus proche autour des coordonnées.
    Étape 2 : Récupère ses dernières mesures (PM10, PM25, etc.)
    
    Args:
        lat, lon (float): coordonnées GPS
        radius (int): rayon de recherche en mètres
        parameters (list): polluants à extraire
        api_key (str): clé API OpenAQ
        verbose (bool): afficher détails

    Returns:
        dict: {polluant: valeur} (ou None si non mesuré)
    """
    headers = {"x-api-key": api_key} if api_key else {}

    # Étape 1 : Trouver la station la plus proche
    #coordinates = f"{float(lat):.6f},{float(lon):.6f}"
    loc_url = f"https://api.openaq.org/v3/locations?coordinates={lat},{lon}&radius={radius}&limit=1"

    
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        if verbose:
            print(f"Coordonnées invalides : lat={lat}, lon={lon}")
        return {param: None for param in parameters}


    try:
        loc_resp = requests.get(loc_url, headers=headers, timeout=5)
        if loc_resp.status_code != 200:
            if verbose:
                print(f" Erreur API (locations) : {loc_resp.status_code}")
            return {param: None for param in parameters}

        locations = loc_resp.json().get("results", [])
        if not locations:
            if verbose:
                print(" Aucune station trouvée à proximité.")
            return {param: None for param in parameters}

        location_id = locations[0]["id"]
        location_name = locations[0]["name"]
        if verbose:
            print(f" Station trouvée : {location_name} (ID {location_id})")

        # Étape 2 : Récupérer les dernières mesures de cette station
        latest_url = f"https://api.openaq.org/v3/measurements?location_id={location_id}&limit=100"
        latest_resp = requests.get(latest_url, headers=headers, timeout=5)

        if latest_resp.status_code != 200:
            if verbose:
                print(f" Erreur API (latest) : {latest_resp.status_code}")
            return {param: None for param in parameters}

        results = latest_resp.json().get("results", [])
        measurements = {}

        for m in results:
            param = m["parameter"]
            if param in parameters and param not in measurements:
                measurements[param] = m["value"]
                if verbose:
                    print(f"  → {param.upper()} = {m['value']} {m['unit']}")


        # Remplir les polluants manquants avec None
        for param in parameters:
            measurements.setdefault(param, None)

        return measurements

    except Exception as e:
        if verbose:
            print(" Exception :", e)
        return {param: None for param in parameters}



API_KEY = "7257e184009771ccd706f6be7de546d06c875e48e1d61ab4fad2ad2d6d52760b"
# Exemple : Paris centre
pollution = get_nearest_station_measurements(48.8700, 2.3540, api_key=API_KEY, verbose=True)
print(pollution)






