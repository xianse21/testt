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


# Exemple de stratégie
def simple_strategy(data):
    # Exemple de stratégie simple : achat lorsque la moyenne mobile sur 50 jours est supérieure à la moyenne mobile sur 200 jours, et vente dans le cas contraire
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()
    data['Position'] = 0
    data.loc[data['50_MA'] > data['200_MA'], 'Position'] = 1  # Achat
    data.loc[data['50_MA'] < data['200_MA'], 'Position'] = -1  # Vente
    return data['Position']

# Exemple d'utilisation du backtester avec la stratégie simple
backtester = backtester(strategy=simple_strategy)
backtester.compute(["MSFT", "AAPL"], "2021-01-01","2023-12-31")

            

