import argparse
import os

from random import sample
from re import sub, findall


class Password(object):
    """Creates a XKCD 936-style password using words from the FreeBSD
    dictionary (see: http://goo.gl/Vt4Kd).

    This class accepts the following parameters:

    * num_words -- the number of words that will be used to generate the
      passowrd. Default is 4.
    * min_len -- the minimum length for any word. Default is 3.
    * max_len -- the maximum length for any word. Default is 8 (big words are
      hard to remember!)

    """

    def __init__(self, num_words=4, min_len=3, max_len=8):
        self.num_words = num_words
        self.min_len = min_len
        self.max_len = max_len
        self.content = self._words()

    def _words(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        word_list = os.path.join(parent_dir, "word_list.txt")
        content = open(word_list).read()
        return sub("\s", " ", content)

    def password(self):
        pattern = r"\b\w{{{0},{1}}}\b".format(self.min_len, self.max_len)
        words = findall(pattern, self.content)
        return sample(words, self.num_words)

    def as_string(self, delimiter='-'):
        return delimiter.join(self.password())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Options for Password')
    parser.add_argument('-n', '--num', type=int, default=4,
                        help="Number of words to use in your password")
    parser.add_argument('-m', '--min', type=int, default=3,
                        help="Minimum lenth of each word (default is 3)")
    parser.add_argument('-x', '--max', type=int, default=8,
                        help="Maximum lenth of each word (default is 8)")
    args = parser.parse_args()

    p = Password(num_words=args.num, min_len=args.min, max_len=args.max)
    print("\n{0}\n".format(p.as_string()))
