import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#import fitz  # for PDF
from docx import Document  # for DOCX
from nltk.corpus import wordnet

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Define the function to extract words from a file and their meanings
def extract_complicated_words_meanings(file_path):
    complicated_words = set()
    meanings = {}

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # Process PDF file
    if file_path.endswith(".pdf"):
        pdf_document = fitz.open(file_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            sentences = sent_tokenize(text)
            for sentence in sentences:
                words = word_tokenize(sentence)
                for word in words:
                    word = re.sub(r'\W+', '', word)  # Remove non-word characters
                    word = word.lower()
                    if word not in stop_words and word.isalpha():
                        lemmatized_word = lemmatizer.lemmatize(word)
                        complicated_words.add(lemmatized_word)

    # Process DOCX file
    elif file_path.endswith(".docx"):
        from docx import Document
        import os
        doc = open('gmp.docx', encoding="ISO-8859-1")
        #doc = open('gmp.docx', encoding="UTF-8")
        dr = doc.read()
        da = dr.split(".")

        print(da)
        #doc = Document('gmp.docx')
        for paragraph in da:
            sentences = sent_tokenize(paragraph)
            for sentence in sentences:
                words = word_tokenize(sentence)
                for word in words:
                    word = re.sub(r'\W+', '', word)  # Remove non-word characters
                    word = word.lower()
                    if word not in stop_words and word.isalpha():
                        lemmatized_word = lemmatizer.lemmatize(word)
                        if len(lemmatized_word) > 5:
                            complicated_words.add(lemmatized_word)
                        else:
                            continue


        meanings_dict = {}
        for word in complicated_words:
            synsets = wordnet.synsets(word)
            meanings = [syn.definition() for syn in synsets]
            meanings_dict[word] = meanings
            # Define meanings for the complicated words

        ''' 
        for word in complicated_words:
            meanings[word] = "Define meaning for " + word
        '''

    return complicated_words, meanings_dict


# Example usage
file_path = "/home/box/Downloads/gmp.docx"  # Replace with the path to your input file
complicated_words, meanings = extract_complicated_words_meanings(file_path)


# Save meanings to a separate file
with open("complicated_words_meanings.txt", "w") as file:
    for word, meaning in meanings.items():
        file.write(f"{word}: {meaning}\n")
       
