#!/usr/bin/env python3

# Caminho para o arquivo de log
LOG_FILE = "network.log"

def analyzeFile():
    f = open(LOG_FILE, "r")
    print(f.read())
    f.close()

if __name__ == "__main__":
    analyzeFile()
