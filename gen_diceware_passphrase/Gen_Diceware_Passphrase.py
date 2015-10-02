'''
Assumptions:
User's going to want spaces between words. This does not seem unreasonable
to me.

Random.org API JSON return:
{
    "jsonrpc": "2.0",
    "result": {
        "random": {
            "data": [
                5,
              *snip*
                3
            ],
             *snip*

TODO:
- Error handling in post().

Requirements:
pip install requests (https://github.com/kennethreitz/requests)

'''

import requests
import json
import argparse


# Magic number. Diceware requires 5 * Int to index into the word list.
DICEWARE_INDEX = 5
# Word list from http://world.std.com/%7Ereinhold/beale.wordlist.asc
# I formatted it as a Julia dict to save having to do file I/O and muck
#     around with transforming it into a Dict (or whatever) on-the-fly.
include('./beale.wordlist.asc.py')

description = '''Generate a passphrase with an arbitrary number of ''' \
              '''words, comprised of an arbitrary minimum number of ''' \
              '''characters, using the Diceware rules and random ''' \
              '''Integers from Random.org.'''

# For printing some kind of version identifier from the command line
VERSION = '0.1'

def handle_args():
    # Kindly provided by Bystroushaak's `argparse builder`
    # http://kitakitsune.org/argparse_builder
    parser = argparse.ArgumentParser(prog='gen_diceware_passphrase',
                                     description=description)
    parser.add_argument('-l', '--phrase-length', default=6, type=int,
                        help='Number of words in the generated passphrase.')
    parser.add_argument('-n', '--min-chars', default=17, type=int,
                        help='Minimum number of characters in the generated ' +
                        'passphrase.')
    parser.add_argument('api-key', required=True, metavar='API_KEY',
                        help='Your personal Random.org API key.')
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s, version {0}'.format(VERSION))
    return parser.parse_args()


def array_to_string(arr):
    # Quoting a data structure into a string (in this case '$arr') returns
    # a string...
    s = replace('$arr', ',', '')
    # Strip '{' '}'.
    return s[2:length(s) - 1]


def split_string_to_array(s, phrase_length):
    s = string('')
    # `phrase_length` word indexes (default 6)...
    for i in range(phrase_length):
        # ...of `DICEWARE_INDEX` char each (has to be 5), delimited by spaces.
        s *= str[i:i + (DICEWARE_INDEX - 1)] * ' '
    return split(s)


def main():
    args = handle_args()
    phrase_length = args['phrase_length']
    passphrase = string('')
    JSONRequest = {
        'jsonrpc': '2.0',
        'method': 'generateIntegers',
        'params': {
            'apiKey': args['api_key'],
            # Number of ints to get.
            'n': phrase_length * DICEWARE_INDEX,
            # Simulate a die-6 roll.
            'min': 1,  # Requested Int minimum.
            'max': 6,  # Requested Int maximum.
            'replacement': true,
            'base': 10
        },
        # `id` value doesn't matter. I think this is to allow us and
        #     the server to verify that we're talking about the
        #     same request.
        # 'id': rand(1:10000)
    }
    # Returns a Response *object*.
    response = requests.post('https://api.random.org/json-rpc/1/invoke',
                             json=JSONRequest)
    # Grab the JSON (the `data` field of the Response object).
    j = JSON.parse(response.data)
    # Grab the 'roll' data from the JSON.
    rolls = array_to_string(j['result']['random']['data'])
    wordindexes = split_string_to_array(rolls, phrase_length)
    for w in wordindexes:
        passphrase *= wordlist[w] *  ' '

    if length(passphrase) < args['min_chars']:
        passphrase = string('')
        # Don't hammer Random.org
        # run(`sleep 20`)
        main()

    # Because we have one space left at the end of the string.
    passphrase = strip(passphrase)
    println('$passphrase')

if __name__ == '__main__':
    sys.exit(main())
