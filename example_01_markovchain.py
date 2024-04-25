import random

def print_chain(chain):
    """
    Print the eight longest entries from the markov chain dictionary in a human readable form. 
    """
    top = sorted(chain.items(), key=lambda x: -len(x[1]))[:8]
    top = [f"{k} : {v[:5]+["..."]}" for k,v in top]
    print()
    print(*top, sep="\n")
    print()


def fill_chain_1(chain, text):
    """
    Fill the markov chain dictionary "chain" from a source text. 
    This function looks only at the single last token.

    TODO: unify the fill_chain functions into a single flexible one
    """
    words = text.split()
    for i in range(len(words)-1):
        word = words[i]
        next = words[i+1]

        if word in chain:
            chain[word].append(next)
        else:
            chain[word] = [next]
    

def fill_chain_2(chain, text):
    """
    Fill the markov chain dictionary "chain" from a source text. 
    This function looks at two preceding tokens.

    TODO: unify the fill_chain functions into a single flexible one
    """
    words = text.split()
    for i in range(1, len(words)-1):
        prev = words[i-1]
        word = words[i]
        next = words[i+1]

        key = (prev,word)
        if key in chain:
            chain[key].append(next)
        else:
            chain[key] = [next]


def fill_chain_3(chain, text):
    """
    Fill the markov chain dictionary "chain" from a source text. 
    This function looks at three preceding tokens.

    TODO: unify the fill_chain functions into a single flexible one
    """
    words = text.split()
    for i in range(2, len(words)-1):
        pprev = words[i-2]
        prev = words[i-1]
        word = words[i]
        next = words[i+1]

        key = (pprev,prev,word)
        if key in chain:
            chain[key].append(next)
        else:
            chain[key] = [next]


def fetch_main_from_gutenberg(filename):
    """
    Extract the main body of a Project Gutenberg text file, stripping the boilerplate text before and after.
    """
    text = []
    in_main_text = False
    with open(filename) as f:
        for line in f:
            if line.startswith("*** START"):
                in_main_text = True
                continue
            
            if line.startswith("*** END"):
                in_main_text = False
                continue
            
            if in_main_text:
                text.append(line)

    return "".join(text)


print("Building markov chain")
# we could use just one dictionary for all three token options, 
# but to give us flexibility, let us fill separate ones
chain_1 = {}
chain_2 = {}
chain_3 = {}
files = [
    "proj_gutenberg_books/odyssey.txt", 
    "proj_gutenberg_books/alice.txt", 
    "proj_gutenberg_books/timemachine.txt",
    # "proj_gutenberg_books/gatsby.txt",
    # "proj_gutenberg_books/beowulf.txt",
    # "proj_gutenberg_books/prince.txt",
    # ## Jane Austen ##
    # "proj_gutenberg_books/persuasion.txt",
    # "proj_gutenberg_books/mansfield.txt",
    # "proj_gutenberg_books/emma.txt",
    # "proj_gutenberg_books/pride.txt",
    # "proj_gutenberg_books/northanger.txt",
    # "proj_gutenberg_books/sense.txt",
    # #################
]
for filename in files:
    text = fetch_main_from_gutenberg(filename)
    fill_chain_1(chain_1, text)
    fill_chain_2(chain_2, text)
    fill_chain_3(chain_3, text)
print("Model training is done")


print_chain(chain_1)
print_chain(chain_2)
print_chain(chain_3)


pprev, prev, word = "Alice", "was", "beginning"
# pprev, prev, word = "I", "do", "not"

print(f"Starting a chain on '{pprev} {prev} {word}'")
print("====")
remaining_output = 200
print(f"{pprev} {prev} {word}", end=" ")
while remaining_output: # while not token.endswith("."):
    if remaining_output % 12 == 0:
        # naive line break every 12 tokens
        print()

    # choose the next word based on just the current token
    cand_1 = random.choice(chain_1[word])

    # if we have no two-token match, fall back to the single token candidate
    cand_2 = random.choice(chain_2.get((prev, word), [cand_1]))

    # if we have no three-token match, fall back to the two-token candidate
    cand_3 = random.choice(chain_3.get((pprev, prev, word), [cand_2]))

    # choose the three-token candidate with high preference, 
    # but sometimes pick one of the others for variety
    cand = random.choices([cand_1, cand_2, cand_3],weights=[4,16,80])

    # shift the token window by one position
    pprev, prev, word = prev, word, cand[0]
    print(word, end=" ")

    remaining_output -= 1


print("\n====")
