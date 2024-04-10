print ("hello world")
print("bonjouuur")
print("Hola")
print("Python")

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import numpy as np
import os

class backtester:
    # Initialisation de la classe
    def __init__(self, strategy):
        self.strategy = strategy
        self.positions = []
        
    # Récupération des données et application, à chaque titre, de la stratégie fournie par l'utilisateur
    def compute(self, symbols, start_date, end_date):
        self.df = {}
        for symbol in symbols:
            # Récupération des données et stockage local des données
            #Si le fichier existe déjà
            file_name = f"{symbol, start_date, end_date}_data.csv"
            if os.path.exists(file_name):
                data = pd.read_csv(file_name, index_col=0)
                print(f"Données de {symbol} chargées à partir du fichier : {file_name}")
            else:
                # Récupération des données si elles ne sont pas déjà stockées localement
                data = yf.download(symbol, start=start_date, end=end_date)
                data.to_csv(file_name)
                print(f"Données de {symbol} téléchargées et sauvegardées localement dans le fichier : {file_name}")
            self.df[symbol] = pd.DataFrame(data)
            # Calcul des résultats pour la stratégie
            position = self.strategy(self.df[symbol])
            self.df[symbol]['position'] = position
            self.positions.append((symbol, position))
            #print(self.df[symbol])
        return self.positions
      
            

