#!/usr/bin/env python3

from datetime import date, timedelta
from astral import Astral
from os.path import isdir
from os import makedirs, chdir

moon_phase_names = {'en':
                    ('New moon',
                     'Waxing crescent',
                     'First quarter',
                     'Waxing gibbous',
                     'Full moon',
                     'Waning gibbous',
                     'Last quarter',
                     'Waning crescent'),
                    'nl':
                    ('Nieuwe maan',
                     'Wassende, sikkelvormige maan',
                     'Eerste kwartier',
                     'Wassende,vooruitspringende maan',
                     'Volle maan',
                     'Krimpende, vooruitspringende maan',
                     'Laatste kwartier',
                     'Krimpende, sikkelvormige maan'),
                    'de':
                    ('Neumond',
                     'Zunehmender Sichelmond',
                     'Erstes Viertel',
                     'Zunehmender Mond',
                     'Vollmond',
                     'Abnehmender Mond',
                     'Letztes Viertel',
                     'Abnehmender Sichelmond'),
                    'fr':
                    ('Nouvelle lune',
                     'Premier croissant ',
                     'Premier quartier',
                     'Lune gibbeuse croissante',
                     'Pleine lune',
                     'Lune gibbeuse décroissante',
                     'Dernier quartier',
                     'Dernier croissant'),
                   }
moon_phase_symbols = ('🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘')

header = {'en': ('Day', 'Phase', 'Symbol', 'Name'),
          'nl': ('Dag', 'Fase', 'Symbool', 'Naam'),
          'de': ('Tag', 'Phase', 'Symbole', 'Name'),
          'fr': ('Jour', 'Phase', 'Symbole', 'Nom'),
         }


def moon_phase_code_to_name(code, lang='en'):
    return moon_phase_names[lang][code]


def moon_phase_code_to_symbol(code):
    return moon_phase_symbols[code]


def moon_phase_to_inacurate_code(phase):
    phase = int(phase)
    if phase == 0:
        return 0
    elif phase > 0 and phase < 7:
        return 1
    elif phase == 7:
        return 2
    elif phase > 7 and phase < 14:
        return 3
    elif phase == 14:
        return 4
    elif phase > 14 and phase < 21:
        return 5
    elif phase == 21:
        return 6
    else:
        return 7


def day_to_moon_phase_and_accurate_code(a, day):
    phase_today = a.moon_phase(date=day, rtype=float)
    code_today = moon_phase_to_inacurate_code(phase_today)

    if code_today % 2 != 0:
        return phase_today, code_today
    
    phase_yesterday = a.moon_phase(date=day - timedelta(days=1), rtype=float)
    code_yesterday = moon_phase_to_inacurate_code(phase_yesterday)
   
    if code_today == code_yesterday:
        return phase_today, code_today + 1   
        
    return phase_today, code_today


def write_files(lang='en'):
    tsv = open('moon-phases.tsv', 'w')
    tsv_full = open('moon-phases-full.tsv', 'w')
    tsv_all = open('moon-phases-all.tsv', 'w')
    md = open('moon-phases.md', 'w')
    md_full = open('moon-phases-full.md', 'w')
    md_all = open('moon-phases-all.md', 'w')
    tsv_header = '# {}\t# {}\t# {}\t# {}\n'.format(
        header[lang][0].ljust(10),
        header[lang][1],
        header[lang][2],
        header[lang][3])
    tsv_header_full = '# {}\t# {}\n'.format(
        header[lang][0],
        header[lang][1])
    tsv.write(tsv_header)
    tsv_all.write(tsv_header)
    tsv_full.write(tsv_header_full)
    md_header = '''{} | {} | {} | {}
-----------|-------:|---|---
'''.format(header[lang][0].ljust(10),
           header[lang][1].ljust(6),
           header[lang][2],
           header[lang][3])
    md_header_full = '''{} | {}
-----------|------:
'''.format(header[lang][0].ljust(10),
           header[lang][1])
    md.write(md_header)
    md_all.write(md_header)
    md_full.write(md_header_full)
    a = Astral()
    today = date.today()
    start = today - timedelta(days=31 + 1)
    end = today + timedelta(days=366 + (2 * 31))
    for i in range((end - start).days):
        day = start + timedelta(days=i)
        phase, code = day_to_moon_phase_and_accurate_code(a, day)
        symbol = moon_phase_code_to_symbol(code)
        name = moon_phase_code_to_name(code)
        tsv_all.write('{}\t{:6.3f}\t{}\t{}\n'.format(day,
                                                     phase,
                                                     symbol,
                                                     name))
        md_all.write('{} | {:6.3f} | {} | {}\n'.format(day,
                                                       phase,
                                                       symbol,
                                                       name))
        if code % 2 == 0:
            tsv.write('{}\t{:6.3f}\t{}\t{}\n'.format(day,
                                                     phase,
                                                     symbol,
                                                     name))
            md.write('{} | {:6.3f} | {} | {}\n'.format(day,
                                                       phase,
                                                       symbol,
                                                       name))
        if code == 4:
            tsv_full.write('{}\t{:6.3f}\n'.format(day, phase))
            md_full.write('{} | {:6.3f}\n'.format(day, phase,))


for lang in sorted(header.keys()):
    if not isdir(lang):
        makedirs(lang)
    chdir(lang)
    write_files(lang)
    chdir('..')
