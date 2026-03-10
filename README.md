# Simulation und Optimierung einer Verpackungsstation mit genetischem Algorithmus

Dieses Projekt simuliert eine Verpackungsstation eines Logistiksystems und optimiert deren 
Ressourcenkonfiguration mithilfe eines genetischen Algorithmus.

Ziel ist es, eine möglichst effiziente Kombination aus Personal, Packstationen und Prozessparametern zu finden, 
unter Berücksichtigung von:

- Durchsatz
- Wartezeiten
- Ressourcenauslastung 
- Gesamtkosten

Die Simulation basiert auf einer diskreten Ereignissimulation mit der Python-Bibliothek **SimPy**.

---

# Projektidee

Produktions- und Logistiksysteme bestehen aus vielen miteinander verbundenen Prozessen. Entscheidungen über 
Ressourcen wie Personal oder Maschinen beeinflussen stark:

- Durchsatz  
- Wartezeiten  
- Systemauslastung  
- Betriebskosten  

In diesem Projekt wird eine vereinfachte Verpackungsstation modelliert und anschließend mit einem genetischen 
Algorithmus optimiert.

---

# Modell des Systems

Die Simulation bildet einen typischen Ablauf in einem Logistiksystem ab.
Pakete durchlaufen folgende Stationen:

Wareneingang → Lager → Pick-Zone → Puffer → Packstation → Versand

Dabei werden folgende Ressourcen modelliert:

- Picker (Mitarbeiter für Kommissionierung)
- Packstationen
- Transportwege zwischen Stationen
- Warteschlangen vor Ressourcen

Pakete können unterschiedliche Typen haben:
- Small
- Large
Diese unterscheiden sich in der Anzahl der benötigten Picks.

---

# Optimierungsproblem

Die Aufgabe besteht darin, eine optimale Konfiguration der Fabrik zu finden.

Optimierte Parameter:

- Anzahl Picker
- Anzahl Packstationen
- Geschwindigkeit im System
- Packdauer

Bewertet wird jede Konfiguration anhand von:

- Gesamtkosten der Ressourcen
- durchschnittlicher Durchlaufzeit
- Wartezeiten
- Kosten-Penalty für lange Durchlaufzeiten

Das Optimierungsziel ist:

**Minimierung der Gesamtkosten pro Schicht inklusive Durchlaufzeit-Penalty.**

---

# Genetischer Algorithmus

Der genetische Algorithmus arbeitet mit folgenden Schritten:

1. Erzeugung einer zufälligen Population von Fabrikkonfigurationen  
2. Bewertung jeder Konfiguration durch Simulation  
3. Auswahl der besten Konfigurationen  
4. Kreuzung (Crossover) der Parameter  
5. Mutation einzelner Parameter  
6. Wiederholung über mehrere Generationen  

Dadurch entwickelt sich schrittweise eine bessere Lösung.

---

# Simulation

Die Simulation basiert auf diskreter Ereignissimulation mit **SimPy**.
Jedes Paket wird als Prozess modelliert und durchläuft das System mit:

- Transportzeiten  
- Bearbeitungszeiten  
- Warteschlangen an Ressourcen  

Mehrere Simulationen werden pro Konfiguration ausgeführt, um stabilere Ergebnisse zu erhalten.

---

# Beispielergebnisse

Der genetische Algorithmus entwickelt über mehrere Generationen bessere Fabrikkonfigurationen.

Jede Generation testet mehrere mögliche Konfigurationen und bewertet diese anhand eines Kosten (Panelty Score)- 
und Leistungsmodells.

## Beispiel Run 1

Generationen:

Generation 1  
Generation 2  
Generation 3  
Generation 4  
Generation 5  

Beste Konfiguration:

ANZAHL_PICKER: 3  
PACKSTATION_KAPAZITAET: 1  
PACKING_DURATION_EINHEITEN: 1.141988625103981  
GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT: 9.75533047510753  

Ergebnisse:

avg_wait_picker: 0.753578824696148  
avg_wait_pack: 0.40965844678459346  
avg_cycle: 18.305308120386442  
total_score: 22884.99817603668  
finished: 226  

---

## Beispiel Run 2

Generationen:

Generation 1  
Generation 2  
Generation 3  
Generation 4  
Generation 5  

Beste Konfiguration:

ANZAHL_PICKER: 4  
PACKSTATION_KAPAZITAET: 2  
PACKING_DURATION_EINHEITEN: 1.1407077936684606  
GESCHWINDIGKEIT_M_PRO_ZEITEINHEIT: 8.125614910498204  

Ergebnisse:

avg_wait_picker: 0.4302639354954214  
avg_wait_pack: 0.02209976468423689  
avg_cycle: 20.213358506241303  
total_score: 26845.3622821775  
finished: 230  

---

# Interpretation

Die beiden Runs zeigen, dass unterschiedliche Ressourcenkonfigurationen zu unterschiedlichen 
Systemverhalten führen.

Zum Beispiel:

- Mehr Ressourcen reduzieren Wartezeiten  
- Höherer Durchsatz kann höhere Kosten verursachen  
- Der genetische Algorithmus sucht eine Balance zwischen Effizienz und Kosten  

---

# Speicherung der Ergebnisse

Nach jeder Ausführung des Programms werden automatisch neue Ergebnisordner erstellt.
In diesen Ordnern werden gespeichert:

- Diagramme des Optimierungsverlaufs  
- Grafiken der Generationenentwicklung  
- Ergebnisse der besten Konfiguration  

Dadurch können mehrere Simulationen miteinander verglichen werden.



# Technologien

Python  
SimPy  
Matplotlib  
Random  

---

# Installation

Repository klonen:

https://github.com/FranciscoFoese/packaging-station-optimization.git

In das Projektverzeichnis wechseln:

cd packaging-station-optimization

Abhängigkeiten installieren:

pip install -r requirements.txt

---

# Ausführung

Simulation starten mit:

pack_optimization.py

Der genetische Algorithmus optimiert automatisch mehrere Generationen von Fabrikkonfigurationen.

Am Ende werden ausgegeben:

- beste Konfiguration  
- Kosten  
- Durchlaufzeiten  
- Ressourcenauslastung  

Zusätzlich wird der Optimierungsverlauf grafisch dargestellt.

---

# Motivation des Projekts

Das Projekt entstand aus dem Interesse zu verstehen, wie sich datengetriebene 
Optimierungsverfahren auf Produktions- und Logistiksysteme anwenden lassen.

Insbesondere sollte untersucht werden, wie sich

- Simulation  
- Warteschlangenmodelle  
- genetische Algorithmen  

kombinieren lassen, um komplexe Systeme zu analysieren und zu verbessern.

---

# Autor

Francisco Föse

Bachelor: Architektur

Masterstudium: Klimagerechtes Bauen und Betreiben. 

Bachelorstudium: Künstliche Intelligenz.


Interessen:

-Smart City
-Simulation  
-Optimierung  
-Energieeffizienz  
-Produktionssysteme  
-Künstliche Intelligenz
-Datengetriebene Entscheidungsmodelle
