#!/usr/bin/env python3

from generator import generate

files = [
    ('index', None),
    ('aviation', 'Aviation'),
    ('hair', 'Hair Care'),
    ('sayings', 'Sayings'),
    ('rabbits', 'Rabbits'),
    ('music', 'Music'),
    ('keyboards', 'Keyboards'),
]

for (name, subtitle) in files:
    with open('markdown/' + name + '.md', 'r') as input_stream:
        with open(name + '.html', 'w') as output_stream:
            title = 'David Harvey-Macaulay'
            if subtitle:
                title += ' :: ' + subtitle
            generate(input_stream, output_stream, title)
