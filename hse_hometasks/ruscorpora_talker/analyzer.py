import sys
from pymorphy2 import MorphAnalyzer


def create_dictionary(text_file):
	with open (text_file, 'r', encoding = 'utf-8') as file:
		lines = file.readlines()

		pos_dictionary = {'NOUN': set(), 'ADJF': set(), 'ADJS': set(), 'COMP': set(), 'VERB': set(), \
		'INFN': set(), 'PRTF': set(), 'PRTS': set(), 'GRND': set(), 'NUMR': set(), 'ADVB': set(), \
		'NPRO': set(), 'PRED': set(), 'PREP': set(), 'CONJ': set(), 'PRCL': set(), 'INTJ': set(), 'None': set()}

		morph = MorphAnalyzer()

		for elem in lines:
			word = elem.split('\t')[1]
			word = word.strip('\n')

			analyze = morph.parse(word)[0]
			pos_tag = str(analyze.tag.POS)
			lemma = analyze.normal_form

			pos_dictionary[pos_tag].add(lemma)
	
	return pos_dictionary

def save_dictionary(pos_dictionary):
	for key, value in pos_dictionary.items():
		filename = key + '.txt'

		with open(filename, 'w', encoding = 'utf-8') as file:
			for word in value:
				file.write('%s%s' % (word, '\n'))

def main():
	text_file = sys.argv[1]

	pos_dictionary = create_dictionary(text_file)
	save_dictionary(pos_dictionary)

if __name__ == '__main__':
	main()