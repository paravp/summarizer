#Author: Parav Patel
# This program utilizes the basics of the nltk (NLP) library to create a text summarizer which outputs a summary for a given text
# (article, story, blog posts etc..).

from __future__ import print_function
import array
import string
import operator

#Natural Language Processing Libraries
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from flask import Flask, render_template, request #Used to render .html templates

#Webscrapping using BeautifulSoup, not yet implemented
import bs4 as bs #beautifulsource4
import urllib2
from urllib2 import urlopen

class summarize:

	def get_summary(self, input, max_sentences):
		sentences_original = sent_tokenize(input)

		#Remove all tabs, and new lines
		if (max_sentences > len(sentences_original)):
			print ("Error, number of requested sentences exceeds number of sentences inputted")
			#Should implement error schema to alert user.
		s = input.strip('\t\n')
		
		#Remove punctuation, tabs, new lines, and lowercase all words, then tokenize using words and sentences 
		words_chopped = word_tokenize(s.lower())
		
		sentences_chopped = sent_tokenize(s.lower())

		stop_words = set(stopwords.words("english"))
		punc = set(string.punctuation)

		#Remove all stop words and punctuation from word list. 
		filtered_words = []
		for w in words_chopped:
			if w not in stop_words and w not in punc:
				filtered_words.append(w)
		total_words = len(filtered_words)
		
		#Determine the frequency of each filtered word and add the word and its frequency to a dictionary (key - word,value - frequency of that word)
		word_frequency = {}
		output_sentence = []

		for w in filtered_words:
			if w in word_frequency.keys():
				word_frequency[w] += 1.0 #increment the value: frequency
			else:
				word_frequency[w] = 1.0 #add the word to dictionary

		#Weighted frequency values - Assign weight to each word according to frequency and total words filtered from input:
		for word in word_frequency:
			word_frequency[word] = (word_frequency[word]/total_words)

		#Keep a tracker for the most frequent words that appear in each sentence and add the sum of their weighted frequency values. 
		#Note: Each tracker index corresponds to each original sentence.
		tracker = [0.0] * len(sentences_original)
		for i in range(0, len(sentences_original)):
			for j in word_frequency:
				if j in sentences_original[i]:
					tracker[i] += word_frequency[j]

		#Get the highest weighted sentence and its index from the tracker. We take those and output the associated sentences.
		
		for i in range(0, len(tracker)):
			
			#Extract the index with the highest weighted frequency from tracker
			index, value = max(enumerate(tracker), key = operator.itemgetter(1))
			if (len(output_sentence)+1 <= max_sentences) and (sentences_original[index] not in output_sentence): 
				output_sentence.append(sentences_original[index])
			if len(output_sentence) > max_sentences:
				break
			
			#Remove that sentence from the tracker, as we will take the next highest weighted freq in next iteration
			tracker.remove(tracker[index])
		
		sorted_output_sent = self.sort_sentences(sentences_original, output_sentence)
		return (sorted_output_sent)

	# @def sort_senteces:
	# From the output sentences, sort them such that they appear in the order the input text was provided.
	# Makes it flow more with the theme of the story/article etc..
	def sort_sentences (self, original, output):
		sorted_sent_arr = []
		sorted_output = []
		for i in range(0, len(output)):
			if(output[i] in original):
				sorted_sent_arr.append(original.index(output[i]))
		sorted_sent_arr = sorted(sorted_sent_arr)

		for i in range(0, len(sorted_sent_arr)):
			sorted_output.append(original[sorted_sent_arr[i]])
		print (sorted_sent_arr)
		return sorted_output



#------------Flask Application---------------#

app = Flask(__name__)
@app.route('/templates', methods=['POST'])
def original_text_form():
	title = "Summarizer"
	text = request.form['input_text'] #Get text from html
	max_value = sent_tokenize(text)
	num_sent = int(request.form['num_sentences']) #Get number of sentence required in summary
	sum1 = summarize()
	summary = sum1.get_summary(text, num_sent)
	print (summary)
	return render_template("index.html", title = title, original_text = text, output_summary = summary, num_sentences = max_value)
@app.route('/')
def homepage():
	title = "Text Summarizer"
	return render_template("index.html", title = title)
	
if __name__ == "__main__":
	app.debug = True
	app.run()
