### List / Dictionary ###
hesitation_list = \
[# from /home/alta/BLTSpeaking/convert-v2/tools/word_map/hesitation_token.py
    'UH','UMS','UM','UUUHHHH','HUH','HUM',
    'AH','AA','AAAHHH','AAM','AMM','AAMMM',
    'MM','HMM','ER','ERM','ERR','ERRR','EHM',
    'EH','EM','AHEM',
# additional hesitation found in the AMI corpus
    'HM', 'UMM', 'MM-HMM', 'UH-HUH', 'MH',
# additional hesitation found in the Fisher CTS corpus
    'OH', 'UH-HUH', 'UH-OH',
    'ACH', 'EEE', 'EW', 'HEE', 'HA'
]
special_tokens = \
[
"<other>", "<hesitation>", "<disfluency>", "<laugh>",
"<gap>", "<cough>", "<vocal>", "<sigh>", "<singing>",
"<sound>", "<noise>", "<unknown>"
]

special_tokens_cts = \
[
"[noise]", "[laughter]", "[vocalized-noise]"
]

short_form_dict = \
{
    "\\'kay": "okay",
    "\\'em": "them",
    "\\'s": "it's", # note that this could be that's, let's etc as well
                    # but it's seems to be most common in the AMI corpus
    "\\'til": "until",
    "\\'till": "until",
    "\\'cause": "because",
    "\\'ll": "'ll",
    "\\'bout": "about",
    "\\'ve": "'ve",
    "\\'specially": "especially",
    "\\'scuse": "excuse",
    "\\'tis": "it's",
    "\\'fraid": "afraid",
    "\\'round": "around",
    "\\'d": "'d"
}

pw_fisher = \
{
    "-kay": "okay",
    "-em": "them",
    "-bout": "about",
    "-cause": "because",
    "-til": "until",
    "-till": "until",
    "-scuse": "excuse",

}


# ------ US => UK spelling ------ #
path_to_us = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/wlists/us_spellings.txt"
path_to_uk = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/wlists/uk_spellings.txt"
us_to_uk_dict = {}
uk_to_us_dict = {}
with open(path_to_us, 'r') as file:
    us_wlist = file.readlines()
with open(path_to_uk, 'r') as file:
    uk_wlist = file.readlines()
for us_word, uk_word in zip(us_wlist, uk_wlist):
    us_to_uk_dict[us_word.strip()] = uk_word.strip()
for us_word, uk_word in zip(us_wlist, uk_wlist):
    uk_to_us_dict[uk_word.strip()] = us_word.strip()


def is_hesitation(token):

    if token.upper() in hesitation_list:
        return True
    else:
        return False

def is_special_token(token):

    if token in special_tokens:
        return True
    else:
        return False

def convert_short_form(token):
    if token not in short_form_dict:
        return "<unknown>"
    else:
        return short_form_dict[token]

def us_to_uk_spelling(word):
    if word in us_to_uk_dict:
        print("US_to_UK: {} => {}".format(word, us_to_uk_dict[word]))
        return us_to_uk_dict[word]
    else:
        return word

def split_word(word):
    if "'" in word:
        if "n't" in word:
            i = word.index("'") - 1
            w1 = word[:i]
            w2 = word[i:]
            return [w1,w2]
        else:
            i = word.index("'")
            w1 = word[:i]
            w2 = word[i:]
            if w1 != "'" and w2 != "'":
                return [w1,w2]
            else:
                return word.strip("'")
    else:
        return




#### CTS Functions ####
def is_special_token_cts(token):

    if token in special_tokens_cts:
        return True
    else:
        return False

#### Fisher Functions ####
def keep_pw_fisher(token):
    if token in pw_fisher:
        return pw_fisher[token]
    else:
        return "<partial>"
