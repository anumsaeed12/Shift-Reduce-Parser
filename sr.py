# Le Duyen Sandra Vu
# 768693
# sr.py
# 
# Schema-basierte Implementierung eines Shift-Reduce-Erkenners
#
# Python Version 2.7.10
# NLTK 3.0
# MacOS 10.11.1

import nltk
from nltk.grammar import Nonterminal
from collections import deque
# wichtig fuer NLTK 3.0
from nltk import CFG 


class ShiftReduceParser:
	agenda = deque()		   # Die Agenda (eine Queue von noch unverarbeiteten Items)
	chart = set()              # Die Chart (Set von allen Items, die wir schon mal gesehen haben)
	chart_incoming = set()     # Hilfs-Datenstruktur

    # Traegt ein Item in die Chart und die Agenda ein, falls es noch nicht
    # schon vorher in der Chart war. Die Items werden zunaechst nicht in die
    # Chart selbst eingetragen, sondern in die Hilfsmenge "chart_incoming",
    # weil wir "enqueue" unten aus dem Inneren einer Schleife ueber die
    # Elemente von "chart" aufrufen. Dort darf man nicht direkt Elemente
    # zu chart hinzufuegen.				
	def enqueue(self,item):
		if not(item in self.chart) and not(item in self.chart_incoming):
			print "   enqueue: ", item
			self.agenda.append(item)
			self.chart_incoming.add(item)
	
	# Uebertraegt die Elemente aus dem temporaeren chart_incoming in die
    # richtige Chart. Soll jedesmal aufgerufen werden, wenn wir eine Parser-Regel
    # fertig angewendet haben und die Schleife ueber chart beendet ist.
	def update_chart(self):
	    self.chart.update(self.chart_incoming)
	    self.chart_incoming = set()

    # Parst den angegebenen Satz mit der Grammatik. Gibt True zurueck gdw
    # der Satz in der Sprache ist.
  	def parse(self, grammar, words):
  		n = len(words)		
  		startitem = (0, "")		
  		self.enqueue(startitem)
  		self.update_chart()
  		
  		# so lange die Agenda nicht leer ist:	 
  		while len(self.agenda) > 0:
  			# Items von der Agenda nehmen	
  			item = self.agenda.popleft() 	
  			index = item[0]			
  			stack = item[1]	
  		
  			# SHIFT
  			# Die Woerter werden hier auf einen (temporaeren) Stack gelegt und die Items
  			# bestehen aus dem jeweiligen Index und dem neuen Stack mit dem hinzu-
  			# gefuegtem Wort, wobei der Index erhoeht wird
  			if index < n:		
  				nextIndex = index + 1			
  				newStack = tuple(stack) 		
  				newStack = newStack + (words[index], )	
  				newItem = (nextIndex, newStack)	
  				self.enqueue(newItem)	
  		
  			# REDUCE
  			# Der originale Stack wird durchgegangen und wenn es eine Regel gibt
  			# dessen rechte Regelseite Elemente mit dem der auf dem Stack 
  			# liegenden Elemente uebereinstimmt, dann wird ein neues Item
  			# mit dem jeweiligen Index und dem Stack bis k (den Rest verwerfen wir)
  			# und der linken Regelseite generiert dh. rechte Regelseite wird durch
  			# linke ersetzt.
  			for k in range(len(stack)): 
  				rhs = tuple(stack[k : ])  
  				for rule in grammar.productions():
  					if rule.rhs() == rhs:
						newStack = stack[ : k] 
  						newStack = newStack + (rule.lhs(), )	
  						newItem = (index, newStack)	
  						self.enqueue(newItem)

  						  
  			self.update_chart()	
  			
  			# Wenn am Ende auf dem Stack (kompletter Durchlauf bis index = n) 
  			# das Startsymbol steht, dann ist der Satz in der Grammatik
  			if index == n and len(stack) == 1 and stack[0] == grammar.start():
  				return True 
  		
  		# Wenn die Schleife komplett durchlaufen ist und das Startsymbol nicht am
  		# Ende des Stacks ist, dann ist der Satz nicht in der Grammatik
  		return False 
  		
  	# Funktion zum Ausgeben der chart
  	def printchart(self):
  		print self.chart


# Ein Demo-Programm zum Ausprobieren (nach Koller, aber modifiziert auf NLTK3)
# nltk.parse_cfg() wurde hier mit CFG.fromstring() ausgetauscht
if __name__ == "__main__":
	grammar = CFG.fromstring("""
 S -> NP VP
 PP -> P NP
 NP -> Det N | Det N | 'I'
 VP -> V NP | VP PP
 Det -> 'an' | 'my'
 N -> 'elephant' | 'pajamas'
 V -> 'shot'
 P -> 'in'
 """)

	# Shift-Reduce-Parser wird hier aufgerufen
	p = ShiftReduceParser()

	result = p.parse(grammar, ["I", "shot", "an", "elephant", "in", "my", "pajamas"])

	if result:
		print "\n\n--> Sentence is in language!\n"
	else:
		print "\n\n--> Sentence is not in language!\n"
		
	
	print "\nChart:\n"
	p.printchart()