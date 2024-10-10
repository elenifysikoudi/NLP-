Assignment 1: “counting, frequencies, and probabilities”

Introduction
In this assignment, you will apply basic computational linguistic techniques to analyze a given text corpus. The assignment focuses on counting, frequency analysis, and probability estimation, providing you with a foundational understanding of text analysis. This assignment will provide you with a more comprehensive understanding of text analysis such as 1-gram, 2-gram, and N-gram analysis.

Preparation
For this assignment, you will need a machine with Python that you can access from the command line — be it your own laptop, or one of the department servers like eduserv and mltgpu.

Download A1.zip. Unzip the file. You will find the directory (folder) A1 containing several files and subdirectories. Two of the Python files, part1.py and load.py, are what you’re going to be editing in this assignment.

A1
├── genres
│   ├── Metal
│   └── Pop
├── loader.py
├── part1.py


part1.py uses the genres directory to obtain instances documents that contain metal and pop lyrics.  You can see how these are loaded into data structures via the load_data function in part1.py and the load_dir function in loader.py. They are tokenized and lowercased. You can investigate the code yourself to see how they are represented.

Your task in this part of the assignment is to modify the calc_prob function in part1.py so that it returns the empirical estimate, where (in this case) the classes are “Pop” or “Rock”, and the features are words as given by the data loading functions. (We will test your code with a different set of classes and documents). That is, your code is to estimate from the data the probability that a document might belong to a class if it has at least one mention of a given word.

Task 1: Counting Words

Write a Python program to count the total number of words in the corpus.
Calculate and report the total number of unique words (vocabulary) in the corpus.
Provide a list of the 10 most frequent words in the corpus, along with their counts.

Task 2: 2-gram Analysis

Calculate the frequency of 2-grams (pairs of consecutive words) in the corpus.
Report a frequency distribution of the top 20 2-grams.

Task 3: N-gram Analysis (Variable N)

Implement a flexible N-gram analysis function that can calculate the frequency of N-grams for any given value of N.

Task 4: Probability Estimation

Choose a specific word from the corpus and calculate its probability of occurrence within the text.
Estimate the conditional probability of a specific word occurring after another word.

The script is to be run like this:

$ python3 part1.py genres/ Pop love
Loading from genres/Pop.
Loading from genres/Metal.
Number of classes in corpus: 2
Looking up probability of class Pop given word love.
-log2 p(Pop|love) is undefined.

Provide a brief written analysis of the findings, including any insights gained from the probability estimation (Task 4).

VG Part

Implement the “most likely tag” baseline. Find a POS-tagged training set (there is one in NLTK), and use it to compute for each word the tag that maximizes p(t|w).  Start by assuming that all unknown words are NN and compute accuracy on a test set.

Further clarification: You are supposed to write a script (program) to compute most likely tag of each word (token) given in a small separate test set. The most likely tag is to computed from a training data set (i.e. an already tagged data). You can use one of POS-tagged data set provided in NLTK (see Chapter 5 section 2.2). From the training set compute probability p(t|w), where t is the tag and w is the word. Your script should chose the most probable tag for a given test word. Compute the accuracy of your tagger on a separate small test set (Hint: Use 80% of the tagged data for training and 20% to test your tagger).   

Submission Guidelines:

You are welcomed to have your own implementation for this assignment, you can have your own tokenization or use NLTK available options.
Submit your Python code for each task along with any necessary comments and explanations.
Submit the assignment as a python files(comprassed) or a Jupyter Notebook.

Note:
You are encouraged to use libraries like NLTK, spaCy, or any other text analysis libraries to simplify the tasks.
When implementing the N-gram analysis (Task 3), make sure to make N flexible, allowing for easy testing of different N-gram sizes
