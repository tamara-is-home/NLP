from input import test
from expected_out import out

class Stemmer:

    def __init__(self, input):
        self.input = [input] if type(input) != list else input
        self.word = ''
        self.output = []

    def stem(self, log=False):
        for w in self.input:
            self.word = w.lower()
            self.step1a()
            if log:
                print('after step1a')
                print(self.word)
            self.step1b()
            if log:
                print('after step1b')
                print(self.word)
            self.step1c()
            if log:
                print('after step1c')
                print(self.word)
            self.step2()
            if log:
                print('after step2')
                print(self.word)
            self.step3()
            if log:
                print('after step3')
                print(self.word)
            self.step4()
            if log:
                print('after step4')
                print(self.word)
            self.step5a()
            if log:
                print('after step5a')
                print(self.word)
            self.step5b()
            self.output.append(self.word)
        return self.output

    def condition_o(self, ending_to_cut=None):  # *o checks if given base w\o ending ends with cvc
        word = self.word if not ending_to_cut else self.word[:-len(ending_to_cut)]
        bad_list = ['w', 'x', 'y']
        cvc_cond = len(word) >= 3 and self.is_consonant(word[-3]) and self.is_vowel(word[-2]) and self.is_consonant(word[-1])
        return True if cvc_cond and word[-1] not in bad_list else False

    def condition_d(self, bad_cases=None):  # *d checks if has double consonant ending with given anti-matches
        if len(self.word) < 3:
            return False
        last_l = self.word[-1]
        before_last_l = self.word[-2]
        if bad_cases and last_l in bad_cases:
            return False
        elif last_l == before_last_l and self.is_consonant(last_l) and self.is_consonant(before_last_l):
            return True
        return False

    def condition_v(self, ending_to_cut):  # *v* checks if contains any vowel before given ending
        for i in self.word[:-len(ending_to_cut)]:
            if self.is_vowel(i):
                return True
        return False

    def step1a(self):
        maps = {'sses': 'ss', 'ies': 'i', 'ss': 'ss', 's': ''}

        for k, v in maps.items():
            if self.word.endswith(k):
                self.word = self.word[:-len(k)] + v
                break
            else:
                continue

    def step1b(self):
        second_or_third_rule = False

        if self.word.endswith('eed') and self.m_split(ending_to_cut='eed')[1] > 0:
            self.word = self.word[:-len('eed')] + 'ee'

        elif self.word.endswith('ed') and self.condition_v('ed'):
            self.word = self.word[:-len('ed')]
            second_or_third_rule = True

        elif self.word.endswith('ing') and self.condition_v('ing'):
            self.word = self.word[:-len('ing')]
            second_or_third_rule = True

        if second_or_third_rule:

            if True in [self.word.endswith(i) for i in ['at', 'bl', 'iz']]:
                self.word = self.word + 'e'

            elif self.condition_d(bad_cases=['l', 's', 'z']):
                self.word = self.word[:-1]

            elif self.m_split()[1] == 1 and self.condition_o():
                self.word += 'e'

    def step1c(self):
        if self.word.endswith('y') and self.condition_v('y'):
            self.word = self.word[:-1] + 'i'

    def step2(self):
        maps = {'ational': 'ate', 'tional': 'tion', 'enci': 'ence', 'anci': 'ance', 'izer': 'ize', 'abli': 'able',
                'alli': 'al', 'entli': 'ent', 'eli': 'e', 'ously': 'ous', 'ization': 'ize', 'ation': 'ate',
                'ator': 'ate',
                'alism': 'al', 'iveness': 'ive', 'fulness': 'ful', 'ousness': 'ous', 'aliti': 'al', 'iviti': 'ive',
                'biliti': 'ble'}

        for k, v in maps.items():
            if self.word.endswith(k) and self.m_split(ending_to_cut=k)[1] > 0:
                self.word = self.word[:-len(k)] + v
                break
            else:
                continue

    def step3(self):
        maps = {'icate': 'ic', 'ative': '', 'alize': 'al', 'iciti': 'ic', 'ical': 'ic', 'ful': '', 'ness': ''}
        for k, v in maps.items():
            if self.word.endswith(k) and self.m_split(ending_to_cut=k)[1] > 0:
                self.word = self.word[:-len(k)] + v
                break
            else:
                continue

    def step4(self):
        ends = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement', 'ment', 'ent', 'ion',
                'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize']

        for e in ends:
            if e == 'ion':
                if self.word.endswith(e) and self.m_split(ending_to_cut=e)[1] > 1 and self.word[:-len(e)][-1] in ['t', 's']:
                    self.word = self.word[:-len(e)]
                    break
                else: continue
            elif self.word.endswith(e) and self.m_split(ending_to_cut=e)[1] > 1:
                self.word = self.word[:-len(e)]
                break

    def step5a(self):
        if self.word.endswith('e') and self.m_split(ending_to_cut='e')[1] > 1:
            self.word = self.word[:-1]
        elif self.word.endswith('e') and self.m_split(ending_to_cut='e')[1] == 1 and not self.condition_o(ending_to_cut='e'):
            self.word = self.word[:-1]

    def step5b(self):
        if self.m_split()[1] > 1 and self.condition_d() and self.word.endswith('l'):
            self.word = self.word[:-1]

    def is_vowel(self, letter):
        vowels = ['a', 'o', 'i', 'e', 'u']
        if letter in vowels or letter == 'y' and self.word[self.word.index(letter) - 1] not in vowels:
            return True
        else:
            return False

    def is_consonant(self, letter):
        return not self.is_vowel(letter)

    def m_split(self, ending_to_cut=None):  # it will count m split for whole word or for given part of it
        word = self.word if not ending_to_cut else self.word[:-len(ending_to_cut)]
        if word:  # may happen that we try o get rid of suffix 'able' in word 'able'
            cv = ''
            for l in word:
                if self.is_consonant(l):
                    cv += 'c'
                else:
                    cv += 'v'
            final_cv = cv[0]
            for c_or_v in cv[1:]:
                if c_or_v == final_cv[-1]:
                    pass
                else:
                    final_cv += c_or_v
            return final_cv, final_cv.count('vc')
        else: return '', -1


if __name__ == '__main__':
    input = test.splitlines()
    exp_out = out.splitlines()
    s = Stemmer(input)
    stemmed = s.stem()
    right = []
    wrong = []
    for k, i, j in zip(input, stemmed, exp_out):
        if i != j: wrong.append(('input: '+k, 'result: '+i, 'correct stem: '+j))
        else: right.append(('input: '+k, 'result: '+i, 'correct stem: '+j))
    [print(w) for w in wrong]
    print(f"{round(1 - len(wrong)/len(right),4)} % of words are stemmed correctly!")
    """
    most of bad cases caused by:
    ly --> li on step 1c causes later to fail on step2 with 'ously' or with other suffixes removal
    suffixes 'ent', 'ment', 'ement' usually are removed at step4 while they shouldnt
    short words with -s or -ies like 'is', 'dies' got ending removed
    feed --> fe, speed --> spe on step 1b. causes wrong form as well
    """

    # test = ['wondrously']
    # s = Stemmer(test)
    # print(s.stem(True))
# ('wondrously', 'wondrousli', 'wondrous')