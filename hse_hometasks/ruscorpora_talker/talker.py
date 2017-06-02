import sys
import random
from pymorphy2 import MorphAnalyzer

def collect_inf_tags(analyze, pos_tag, lemmas, morph):
	pos_variants = {'n': ['NOUN'], 'v': ['VERB', 'INFN', 'PRTF', 'PRTS', 'GRND'], \
		'adj': ['ADJF', 'ADJS', 'COMP'], 'num': ['NUMR']}

	bare_word = random.choice(lemmas).strip('\n')
	new_analyze = morph.parse(bare_word)[0]
	
	inf_tags = set()

	if pos_tag in pos_variants['n']:
		while analyze.tag.gender != new_analyze.tag.gender and analyze.tag.animacy != new_analyze.tag.animacy:
			bare_word = random.choice(lemmas).strip('\n')
			new_analyze = morph.parse(bare_word)[0]
		
	if pos_tag in pos_variants['n'] or pos_tag in pos_variants['adj'] or pos_tag in pos_variants['num']:
		if analyze.tag.case != None:
			inf_tags.add(analyze.tag.case)

	if pos_tag in pos_variants['v']:
		if analyze.tag.person != None:
			inf_tags.add(analyze.tag.person)

	if pos_tag in pos_variants['v']:
		if analyze.tag.mood != None:
			inf_tags.add(analyze.tag.mood)
		if analyze.tag.transitivity != None:
			inf_tags.add(analyze.tag.transitivity)
		if analyze.tag.aspect != None:
			inf_tags.add(analyze.tag.aspect)
		if analyze.tag.tense != None:
			inf_tags.add(analyze.tag.tense)

	if pos_tag in pos_variants['v'] or pos_tag in pos_variants['adj']:
		if analyze.tag.gender != None:
			inf_tags.add(analyze.tag.gender)

	if analyze.tag.number != None and new_analyze.tag.number != None:
		inf_tags.add(analyze.tag.number)

	return new_analyze, inf_tags

def generate_answer(input_sentence):
	morph = MorphAnalyzer()

	words = input_sentence.split()
	answer = ''

	for word in words:
		analyze = morph.parse(word)[0]
		
		pos_tag = analyze.tag.POS
		filename = str(pos_tag) + '.txt'

		with open (filename, 'r', encoding = 'utf-8') as file:
			lemmas = file.readlines()

		changed_word = None

		while changed_word == None:
			new_analyze, inf_tags = collect_inf_tags(analyze, pos_tag, lemmas, morph)
			changed_word = new_analyze.inflect(inf_tags)

		answer = answer + changed_word.word + ' '

	print(answer)

def main():
	input_sentence = sys.argv[1]
	generate_answer(input_sentence)

if __name__ == '__main__':
	main()