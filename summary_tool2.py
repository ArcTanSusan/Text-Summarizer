# coding=UTF-8

from __future__ import division
import re
import nltk
from nltk.tag.simplify import simplify_wsj_tag

# This is a naive text summarization algorithm
# Created by Shlomi Babluki
# April, 2013
# And then modified by Susan Tan


class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):
        value1 = set(sent1.values()[0])
        value2 = set(sent2.values()[0])
        # If there is not intersection, just return 0
        if (len(value1) + len(value2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return (len(value1.intersection(value2))) / (len(value1) + len(value2) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.split(r'\W+', sentence)
        return sentence

    def stem_sentences(self, content):
        stemmed_dict = dict()
        stemmed_text_dict = []
        sentences = self.split_content_to_sentences(content)
        for sentence in sentences:
            tokenized_sentence = self.format_sentence(sentence)
            tagged_sent = nltk.pos_tag(tokenized_sentence)
            relevant_words_in_sentence = []
            # Use built-in simplified tags.
            simplified = [(word, simplify_wsj_tag(tag)) for word, tag in tagged_sent]
            for toople in simplified:
                if toople[1]  in ['V', 'VD', 'VG', 'VN', 'ADJ', 'NP', 'N']:
                    relevant_words_in_sentence.append(toople[0])
            # Get the stems of each sentence
            wnl = nltk.WordNetLemmatizer()
            stemmed_sent = [wnl.lemmatize(word) for word in relevant_words_in_sentence]
            stemmed_dict[sentence] = stemmed_sent
            stemmed_text_dict.append(stemmed_dict)
            relevant_words_in_sentence = []
            stemmed_dict = dict()
        return stemmed_text_dict

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_sentences_ranks(self, content):

        stemmed_text_dict = self.stem_sentences(content)
        # Calculate the intersection of every two sentences
        n = len(stemmed_text_dict)
        values = [[0 for x in xrange(n)] for x in xrange(n)]

        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(stemmed_text_dict[i], stemmed_text_dict[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[stemmed_text_dict[i].keys()[0]] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):
        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
                if sentences_dic[s] > max_value:
                    max_value = sentences_dic[s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)


# Main method, just run "python summary_tool.py"
def main():
    # Read sample Input text, which is a collection of 4 different biographies.
    text_name = 'fran_allen'
    with open(text_name + '.txt', 'r') as f:
        read_data = f.read()
    f.closed
    title = text_name

    # Create a SummaryTool object
    st = SummaryTool()
    # # Build the sentences dictionary
    sentences_dic = st.get_sentences_ranks(read_data)
    # # Build the summary with the sentences dictionary
    summary = st.get_summary(title, read_data, sentences_dic)

    # # Write the summary into a text file.
    f = open(text_name + '_summary.txt', 'w')
    f.write(summary)
    f.closed

    # # Print the ratio between the summary length and the original length
    print "Original Length %s" % (len(title) + len(read_data))
    print "Summary Length %s" % len(summary)
    print "Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(read_data)))))


if __name__ == '__main__':
    main()
