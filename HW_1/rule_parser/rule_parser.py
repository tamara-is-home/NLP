import spacy
import itertools

nlp = spacy.load(r'B:\stuff\anaconda\lib\site-packages\en_core_web_sm\en_core_web_sm-3.1.0')
# TODO: comment line above and uncomment line below
#nlp = spacy.load('en_core_web_sm-3.1.0')

class DocParser:
    def __init__(self, doc):
        self.doc = doc
        self.feature_map = {
            'POS': 'pos_',
            'TAG': 'tag_',
            'DEP': 'dep_',
            'LOWER': 'lower',
            'TEXT': 'text',
            'IS_ALPHA': 'is_alpha',
            'IS_DIGIT': 'is_digit',
            'IS_LOWER': 'is_lower',
            'IS_UPPER': 'is_upper',
            'IS_TITLE': 'is_title',
            'IS_PUNCT': 'is_punct',
            'IS_SPACE': 'is_space',
            'IS_STOP': 'is_stop',
            'IS_START': 'is_start',
            'IS_END': 'is_end',
            'LIKE_NUM': 'like_num',
            'LIKE_URL': 'like_url',
            'LIKE_EMAIL': 'like_email',
            'LEMMA': 'lemma',
            'ORIGINAL': 'original',
            'SHAPE': 'shape',
        }
        self.all_seq_spans = [(i, i+1) for i in range(len(doc))]
        self.prev_spans = []
        self.op = None

    def parse_token_features(self, token, feats) -> bool:
        for key in feats:
            if key == 'OP':
                pass
            elif getattr(token, self.feature_map[key]) != feats[key]:
                return False
        return True

    def get_all_nodes(self, feats):

        self.op = feats.get('OP', None)

        if not self.prev_spans:
            if self.op and self.op == '+':
                all = []
                for token in self.doc:
                    # print(token)
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        all.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')
                print(f'Spans found on this step before + operator are: {all}')
                print(f'All current spans are: {self.prev_spans}')
                self.prev_spans = self.get_combinations(all)
                print(f'Spans after + operator are: {self.prev_spans}')

            elif self.op and self.op == '!':
                all = []
                for token in self.doc:
                    # print(token)
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        all.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')
                print(f'Spans found on this step before ! operator are: {all}')
                print(f'All current spans are: {self.prev_spans}')
                self.prev_spans = self.get_anti_combinations(all, [*range(len(self.doc))])
                print(f'Spans after ! operator are: {self.prev_spans}')

            # regarding optional operator. If we dont found match, we ignore it
            # if we found match, we work only with those spans, which we found.
            # so if it is a first step, '?' operator is technically the same as no operator
            elif self.op and self.op == '?':
                all = []
                for token in self.doc:
                    # print(token)
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        all.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')
                print(f'Spans found on this step before ? operator are: {all}')
                print(f'All current spans are: {self.prev_spans}')
                self.prev_spans = all
                print(f'Spans after ? operator are: {self.prev_spans}')

            # if no matches found on first step with "*" - its ok
            # the next step will be considered as first and self.prev_spans will be empty
            # if they will be found - we'll take all combs as with '+'
            elif self.op and self.op == '*':
                all = []
                for token in self.doc:
                    # print(token)
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        all.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')
                print(f'Spans found on this step before * operator are: {all}')
                print(f'All current spans are: {self.prev_spans}')
                self.prev_spans = self.get_combinations(all)
                print(f'Spans after * operator are: {self.prev_spans}')

            else:
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        self.prev_spans.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')

        else:
            print(f'Prev spans are {self.prev_spans}')
            this_state_result = []
            if self.op and self.op == '+':
                print('OP +:')
                all = []
                for token in self.doc:
                    # print(token)
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        all.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')
                print(f'Spans found on this step before + operator are: {all}')
                print(f'All current spans are: {self.prev_spans}')
                all_sequences = self.get_combinations(all)

                for prev_start, prev_end in self.prev_spans:
                    for seg_start, seq_end in all_sequences:
                        if prev_end == seg_start or prev_end == seq_end:
                            this_state_result.append((prev_start, seq_end))
                self.prev_spans = this_state_result
                print('All spans after operator +:', self.prev_spans)

            elif self.op and self.op == '!':
                print('OP !:')
                all = []
                for token in self.doc:
                    # print(token)
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        all.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')
                print(f'Spans found on this step before ! operator are: {all}')
                print(f'All current spans are: {self.prev_spans}')

                self.prev_spans = self.reduce(self.prev_spans, all)
                print('All spans after operator !:', self.prev_spans)

            # on the second + step this operator acts like:
            # if we found no match we will keep working with current spans
            # if we found match we will keep working only with that matches
            elif self.op and self.op == '?':
                print('OP ?:')
                for prev_span_start, prev_span_end in self.prev_spans:
                    if prev_span_end < len(self.doc):
                        if self.parse_token_features(self.doc[prev_span_end], feats):
                            print(
                                f'token {self.doc[prev_span_end]} passed {feats}, appending {prev_span_start, prev_span_end + 1}')
                            this_state_result.append((prev_span_start, prev_span_end + 1))
                        else:
                            print(f'token {self.doc[prev_span_end]} didnt pass {feats}')
                print(f'Spans found on this step before ? operator are: {this_state_result}')
                print(f'All current spans are: {self.prev_spans}')
                if not this_state_result:
                    self.prev_spans += this_state_result  # do nothing
                if this_state_result:
                    self.prev_spans = this_state_result
                print('All spans after operator ?:', self.prev_spans)

            # I think this operator should work like '+' + '?' on second step.
            # If no matches - skip. If matches - take all combinations
            elif self.op and self.op == '*':
                print('OP *:')
                all = []
                for token in self.doc:
                    # print(token)
                    if self.parse_token_features(token, feats):
                        print(f'token {token} passed {feats}, appending {token.i, token.i + 1}')
                        all.append((token.i, token.i + 1))
                    else:
                        print(f'token {token} didnt pass {feats}')
                print(f'Spans found on this step before * operator are: {all}')
                print(f'All current spans are: {self.prev_spans}')
                all_sequences = self.get_combinations(all)
                if all_sequences:
                    for prev_start, prev_end in self.prev_spans:
                        for seg_start, seq_end in all_sequences:
                            if prev_end == seg_start or prev_end == seq_end:
                                this_state_result.append((prev_start, seq_end))
                    self.prev_spans = this_state_result
                else: self.prev_spans += this_state_result  # if we didnt found match with '*' we do nothing
                print('All spans after operator *:', self.prev_spans)

            else:
                for prev_span_start, prev_span_end in self.prev_spans:
                    if prev_span_end < len(self.doc):
                        if self.parse_token_features(self.doc[prev_span_end], feats):
                            print(f'token {self.doc[prev_span_end]} passed {feats}, appending {prev_span_start, prev_span_end+1}')
                            this_state_result.append((prev_span_start, prev_span_end+1))
                        else:
                            print(f'token {self.doc[prev_span_end]} didnt pass {feats}')
                self.prev_spans = this_state_result

    def parse_expression(self, expression):
        self.prev_spans = []

        for feats in expression:
            self.get_all_nodes(feats)

        self.prev_spans = list(set(self.prev_spans))
        self.prev_spans.sort()
        return self.prev_spans

    @staticmethod
    def reduce(input_list1, input_list2):
        # used in anti matching
        # [(5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5,12), (5,13)] reduce by [(10, 11)] --> [(5, 6), (5, 7), (5, 8), (5, 9)]
        out_ranges = []
        for i, j in input_list2:
            out_ranges.append([*range(i, j + 1)])
        out_ranges = [item for sublist in out_ranges for item in sublist]
        final = []

        for i, j in input_list1:
            flag = True
            for el in range(i, j):
                if el in out_ranges:
                    flag = False
            if flag:
                final.append((i, j))

        return final

    # code with graphs from lectures refused to work on my pc, so had to make this guy
    @staticmethod
    def get_combinations(input_list):
        if not input_list: return []
        # [(1, 2), (2, 3), (4, 5), (6, 7), (7, 8), (8, 9), (11,12)] --> [(1, 2), (1, 3), (2, 3), (4, 5), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9), (11, 12)]
        local_maxes = []
        local_mins = [input_list[0][0]]
        for i in range(len(input_list) - 1):
            if input_list[i][1] != input_list[i + 1][0]:
                local_maxes.append(input_list[i][1])
                local_mins.append(input_list[i + 1][0])
        local_maxes.append(input_list[-1][1])

        combinations = [itertools.combinations([*(range(i, j + 1))], 2) for i, j in zip(local_mins, local_maxes)]
        final = []
        for i in combinations:
            for j in i:
                final.append(j)

        return final

    @staticmethod
    def get_anti_combinations(input_list, whole_range: list):
        # is used in ! operator. Given founded tuples and whole len of word (as list [1,..n]). Returns all excluding founded
        # (1,2),(2,3),(6,7),(7,8) --> (0,1),(3,4),(4,5),(5,6),(8,9)..(n-1,n)
        whole_range = [(i, i + 1) for i in range(len(whole_range) - 1)]
        return [i for i in whole_range if i not in input_list]


if __name__ == '__main__':

    text = 'I live in London and work in in New Yorkshir Tempenny J&L Consulting Ltd. Ltd. and my gf works in McDonalds Ltd.'  #
    doc = nlp(text)
    parser = DocParser(doc)
    result = parser.parse_expression(

        [{'TEXT': 'in', 'OP': '*'},  # is 'zero or more' but not 'zero and more' so it'll take all 'in's if found any or skip
         {'POS': 'PROPN', 'OP': '+'},
         {'TEXT': 'Yorkshir', 'OP': '?'},  # if Yorkshir found, we'll keep matching only those spans, otherwise skip
         {'POS': 'PROPN', 'OP': '+'},
        {'TEXT': 'Ltd.', 'OP': '!'},
]
    )
    print('RESULTING:')
    print(result)
    for start, end in result:
        print(doc[start:end])