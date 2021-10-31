import random
import re

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

psychobabble = [
    (
        r'quit',
        [
            "Thank you for talking with me.",
            "Good-bye.",
            "Thank you, that will be $150. Have a good day!"
         ]
    ),

    (
        "bye|good bye|cheers|have a good day|see you",
        ["Have a good day, human!",
         "Hope you won't miss our sessions again, I don't want to see you going to jail. Joke.", ]
    ),
    (
       "cool/rested/tired|well|happy|sad|angry|frustrated|exhausted|envy|not ok|ok|bad|good|better|worse|worst|best",
        ["What is the reason?",
         "Do you want to talk about it?",
         "For how long is it like that?"]
    ),
    (
        "don't know|do not know|dont know",
        ["So you should think about it",
         "Only you know the reason.",
         "I'm here to help, relax and think."]
    ),
    (
        "argue|conflict|date|meeting",
        ["Did it have any consequences?",
         "Tell me more about that person.",
         "Describe how it was."]
    ),
   (
        "would like to|want to|wanted to|dreaming of",
        ["You definitely have to try it. And what about your other plans?",
         "Lets think how you can achieve that.",
         "Do you think you can make it?"]
    ),
    (
        "friend|girlfriend|boss|colleague|partner|teammate|group mate|gf|bf|boyfriend",
        ["Tell me more about this person.",
         "Lets better talk about you.",]
    ),

    (
        "he is|he was|she is|she was",
        ["Ok, got it. Now lets keep talking about you.",
         "That shouldn't bothering you.",
         "Do you like this person?"]
    ),
    (
        "i will|will be|will",
        ["Its good to think about the future, but lets discuss the present",
         "Good that you have plans, could you tell me more about it?",]
    ),
    (
        "you|yours",
        ["I am just a machine, let's keep talking about you.",
         "We should not spend time on me, don't you think so?",]
    ),
    (
        "yes|no",
        ["As you wish.",
         "Ok, lets continue.",
         "Its up to you then."]
    ),
    (
        "hello|hi",
        ["Hey, so how do you feel today?",
         "...",
         "Just answer the question."]
    ),
    (
        "what|why|how|when|where",
        ["I am the one who asking questions.",
         "You tell me.",]
    ),
    (
        "long|often|rarely|always|never|ever|year|month|hour|minute|decade|century|days",
        ["Time is an abstract thing.",
         "Till we are here together, time means nothing.", ]
    ),
    (
        "bad day|good day|problems|day was terrible|life is terrible|day was perfect|life is perfect|day was good|life is good|\
        |day was bad|day is bad|day is good",
        ["Lets discuss it.",
         "What exactly happened?",
         "What caused that?"]
    ),
    (
        "cant|can't",
        ["No, you can, just keep trying!",
         "You are so weak. But I will help you. So how do you think we can solve it?", ]
    ),
    (
        "dog|cat|parrot|rabbit|snake",
        ["Animals are good for humans, they help them to relax. Do you like animals?",
         "Is this your pat?", ]
    ),
    (
        "sport|gym|play|dance|fight|kill|swim|survive",
        ["Wow, and for how long have you been doing that?",
         "That's so cool you have a hobby!",
         "I wish I could spend my time in the same way..."]
    ),

]


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    statement_l = statement.lower()
    for pattern, responses in psychobabble:
        match = re.search(pattern, statement_l)
        if match:
            response = random.choice(responses)
            if statement_l != 'quit':
                for word in statement_l:
                    if word in reflections.keys():
                        response = random.choice(['So ', 'You say that ', 'I see, ']) + reflect(statement) + '. ' + response
                        break
            return response
        else:
            pass
    return "I have nothing to say here. Let's continue our session and talk about something else. "


def main():
    print(random.choice(["Hello. How are you feeling today?", "Hello, how was your day?", "So you came back again. Anything to tell?"]))

    while True:
        statement = input("YOU: ")
        print("ELIZA: " + analyze(statement))

        if statement == "quit":
            break


if __name__ == "__main__":
    main()