import nltk

#I don't seem to be able to see the results of the code but there are no errors. It is my attempt for the VG  part.
#I run it once overnight but it still didn't work.

class ShiftReduceParser:
    def __init__(self, grammar, sentence):
        self.stack = []
        self.buffer = sentence.split()
        self.grammar = grammar
 
    def shift(self):
        while len(self.buffer) > 0:
               token=self.buffer.pop(0)
               self.stack.append(token)
               
 
    def reduce(self):
        for production_rules in self.grammar.productions():
               rhs = production_rules.rhs()
               if self.stack[-len(rhs):] == list(rhs):
                    self.stack = self.stack[:-len(rhs)]
                    self.stack.append(production_rules.lhs())
        return 
 
    def parse(self):
        while self.buffer or len(self.stack) >1:
                self.reduce()
                if not self.reduce():
                    self.shift()
                    if len(self.buffer) == 0 and "S" in self.stack:
                        return "successful parsing"
 
if __name__ == "__main__":
    # Provided CFG grammar
    grammar1 = nltk.CFG.fromstring("""
        S -> NP VP
        VP -> V NP | V NP PP
        PP -> P NP
        V -> "saw" | "ate" | "walked"
        NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
        Det -> "a" | "an" | "the" | "my"
        N -> "man" | "dog" | "cat" | "telescope" | "park"
        P -> "in" | "on" | "by" | "with"
    """)
 
    # Example sentence to parse
    sentence = "the dog saw a man"
 
    parser = ShiftReduceParser(grammar1, sentence)
    result=parser.parse()
    print(result)