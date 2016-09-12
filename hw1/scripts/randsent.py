#!/usr/bin/env python
import re, os, argparse, sys, math, warnings, subprocess, random
from collections import defaultdict
class sent_generator:
	def __init__ (self, grammar_file, verbose = False):
		if not os.path.isfile(grammar_file):
			sys.exit("Expect grammer file {0} exist".format(grammar_file))
		self.verbose = verbose
		self.counts = defaultdict(dict)
		self.prob = defaultdict(list)
		# This set store terminal symbols
		self.nonterminals = set([])
		# Start collecting grammer together with its weight
		with open(grammar_file,'r') as f:
			for line in f:
				if not line or line[0] == '#' or line[0] == '\n':
					continue
				# We split the line in suitable format (note that they are separated by tab)
				# Also make sure that RHS should be a tuple consist with terminal/nonterminal syms
				# But not comment (start either by '#' or '(')
				weight, LHS, RHS = line.strip().split('\t')

				RHS = RHS.strip().split()
				for idx in range( len(RHS) ):
					if RHS[idx][0] == '(' or RHS[idx][0] == '#':
						idx -= 1
						break
				RHS = RHS[:idx+1]
				if tuple(RHS) in self.counts[LHS]:
					sys.stderr.write("the line:\n {0} \n is duplicated,"
						"try delete one or merge the weight\n".format(line) )
				self.counts[LHS][tuple(RHS)] = float(weight)
		self.normalize()

	# We will normlize those 'int' count to 'float' probability
	def normalize(self):
		# symbol is nonterminal symbols, and dic stores all the way that a
		# nonterminal symbol can be re-written
		for symbol, dic in self.counts.items():
			self.nonterminals.add(symbol)
			summing = float( sum(dic.values()) )
			accumulated_prob = 0.0
			for RHS, count in dic.items():
				accumulated_prob += count / summing
				self.prob[symbol].append([RHS, accumulated_prob])

	# We will call this 'rewrite' function recursively to rewrite a sentence
	# according to pre-computed probability
	def rewrite(self, syms):
		res = []
		for sym in syms:
			if sym in self.nonterminals:
				rn = random.random()
				for RHS, prob in self.prob[sym]:
					if prob > rn:
						if self.verbose:
							info = "{0} -> {1} ".format(sym, str(RHS) )
							print info
						res += self.rewrite(RHS)
						break
			else:
				res.append(sym)
		return res





parser = argparse.ArgumentParser(description = "The script read grammar file and "
								 "produce random generated sentences. e.g.: "
								 "randsent.py [-n 10] <grammar-file> (default num of "
								 "sentences is 1) ")

parser.add_argument("-n", "--num-sentences", default = 1,
					help = "Specify num of sentences want to be generated")
parser.add_argument("-v", action = "store_true", default = False,
					help = "this option can print some information for insight or debug")
parser.add_argument("grammar_file",
					help = "Speicify the grammar file")

args = parser.parse_args()
my_generator = sent_generator(args.grammar_file, verbose = args.v)

for num_sen in range(int(args.num_sentences)):
	print " ".join( my_generator.rewrite(['ROOT']) )








