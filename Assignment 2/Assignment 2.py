import re 
import inflect
p = inflect.engine()
import nltk
from nltk.corpus import treebank
nltk.download('treebank')

def regex_parsing():
    pois = [ 'Indian restaurants', 'Italian restaurants',
    'Starbucks', 'bakeries', 'banks', 'bus stops', 'butchers',
    'camp sites', 'cemeteries', 'charging stations', 'fire brigades',
    'fire hydrants', 'helipads', 'hiking maps', 'hospitals', 'kindergartens',
    'museums', 'peaks', 'playgrounds', 'post offices', 'schools', 'supermarkets']

    locations = ['Edinburgh', 'Heidelberg', 'Paris', 'Berlin']

    pois_categories= {"amenity" : ["banks", "post offices", "schools", "kindergartens", "fire brigades", "charging stations", "hospitals"] ,
                "shop": [ "bakeries", "butchers", "supermarkets"] ,
                "tourism" : ["museums", "camp sites"] ,
                "cuisine" : ["Indian restaurants", "Italian restaurants"] ,
                "landuse" : ["cemeteries"] ,
                "aeroway": ["helipads"] ,
                "emergency" : ["fire hydrants"] ,
                "information" : ["hiking maps"] ,
                "natural" : ["peaks"] ,
                "leisure" : ["playgrounds"] ,
                "highway": ["bus stops"] ,
                 "name" : ["Starbucks"] }

    test_queries = [f"Where are {poi} in {loc}?" for poi in pois for loc in locations]

    reg_exp = r"^Where are (\w+)(?: (\w+))? in (\w+)\?$"
    mac_read_repr = []
    querries =[]
    for loc in locations:
        for poi in pois:
            query = f"Where are {poi} in {loc}?"
            querries.append(query)
            result = re.match(reg_exp, query)
            words = poi.split()
            if result:
                machine_category = None
                for category,place in pois_categories.items():
                    if poi in place:
                        machine_category=category
                        if len(words) > 1 :
                            singular = p.singular_noun("{}_{}".format(result.group(1).lower(), result.group(2).lower()))
 
                        else:
                            singular = p.singular_noun(result.group(1).lower())

                        if machine_category == "cuisine":
                            singular = result.group(1).lower()
                        
                        elif result.group(1).lower() == "Starbucks":
                            singular = result.group(1)

                        mrl = "query(area(keyval('name','{}')),nwr(keyval('{}','{}')),qtype(latlong))".format(result.group(3),machine_category,singular)    
                        mac_read_repr.append(mrl)
                        #print(f"{query}\t{mrl}")


    
    nlmaps_mrls = []
    file = 'nlmaps_new-1.tsv'
    with open (file,encoding='utf-8') as nlmaps_file:
        nlmaps_file_contents = nlmaps_file.readlines()
        for mrls in nlmaps_file_contents:
            mrl=mrls.split('\t')
            nlmaps_mrls.append(mrl[1].strip())
        
    correct_mrls = 0
    for mrl in nlmaps_mrls:
        if mrl in mac_read_repr:
            #print("These are correct",mrl)
            correct_mrls+=1
    print(correct_mrls)


    #checking which mrl are incorrect to better the code:
    for mrl in mac_read_repr:
        if mrl not in nlmaps_mrls:
            print(mrl)

    nlmaps_querries =[]
    gold = 0
    with open (file,encoding='utf-8') as nlmaps_file:
        nlmaps_file_contents = nlmaps_file.readlines()
        for mrls in nlmaps_file_contents:
            mrl=mrls.split('\t')
            nlmaps_querries.append(mrl[0].strip())
    for querry in querries:
        if querry in nlmaps_querries:
            gold+=1

    accuracy = correct_mrls/gold
    return accuracy

def PCFG_grammar():
    productions = []
    frequencies = {}
    for tree in treebank.parsed_sents()[:100]:
        tree.chomsky_normal_form()
        productions_trees = tree.productions()
        for tree in productions_trees:
            productions.append(tree)
    lhs_counts = {}
    lhs_rhs_counts = {}
    for rules in productions:
        lhs = rules.lhs()
        rhs = rules.rhs()
        if lhs in lhs_counts:
            lhs_counts[lhs]+=1
        else:
            lhs_counts[lhs]=1

        lhs_rhs = (lhs,rhs)
        if lhs_rhs in lhs_rhs_counts:
            lhs_rhs_counts[lhs_rhs]+=1
        else:
            lhs_rhs_counts[lhs_rhs] = 1
     
    for lhs in lhs_counts.keys():   
        for lhs_rhs in lhs_rhs_counts.keys():
            if lhs == lhs_rhs[0]:
                if lhs_rhs not in frequencies:
                    frequencies[lhs_rhs] = lhs_rhs_counts[lhs_rhs] / lhs_counts[lhs]
    
    production_rules =[]
    for lhs_rhs,prob in frequencies.items():
        lhs = lhs_rhs[0]
        rhs = lhs_rhs[1]
        rule = nltk.grammar.ProbabilisticProduction(lhs=lhs,rhs=rhs,prob=prob)
        production_rules.append(rule)
    
    start = nltk.Nonterminal("S")
    grammar = nltk.PCFG(start,production_rules)
    
    viterbi_parser = nltk.ViterbiParser(grammar)
    for test_sentence in treebank.sents()[:5]:
        for tree in viterbi_parser.parse(test_sentence):
            print(tree)

if __name__ == '__main__':
    print(regex_parsing())
    print(PCFG_grammar())
