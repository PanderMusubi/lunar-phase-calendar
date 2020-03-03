#!/usr/bin/env python3

from datetime import date, datetime, timedelta
from astral import Astral
from os.path import isdir
from os import makedirs, chdir, getpid
from socket import getfqdn


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
                     'Premier croissant',
                     'Premier quartier',
                     'Lune gibbeuse croissante',
                     'Pleine lune',
                     'Lune gibbeuse décroissante',
                     'Dernier quartier',
                     'Dernier croissant'),
                    'es':
                    ('Luna nueva',
                     'Luna creciente',
                     'Cuarto creciente',
                     'Luna creciente gibosa',
                     'Luna llena',
                     'Luna menguante gibosa',
                     'Cuarto menguante',
                     'Luna menguante'),
                    'pt':
                    ('Lua nova',
                     'Lua crescente',
                     'Quarto crescente',
                     'Lua crescente gibosa',
                     'Lua cheia',
                     'Lua minguante gibosa',
                     'Quarto minguante',
                     'Lua minguante'),
                    'it':
                    ('Luna nuova',
                     'Luna crescente',
                     'Primo quarto',
                     'Gibbosa crescente',
                     'Luna piena',
                     'Gibbosa calante',
                     'Ultimo quarto',
                     'Luna calante'),
                    'af':
                    ('Donkermaan',
                     'Groeiende sekelmaan',
                     'Eerste kwartier',
                     'Groeiende bolmaan',
                     'Volmaan',
                     'Afnemende bolmaan',
                     'Laaste kwartier',
                     'Afnemende sekelmaan'),
                   }
moon_phase_symbols = ('🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘')

# capitalized header values for day, phase, symbol, name and title
header = {'en': ('Day', 'Phase', 'Symbol', 'Name', 'Lunar Phase'),
          'nl': ('Dag', 'Fase', 'Symbool', 'Naam', 'Maanfase'),
          'de': ('Tag', 'Phase', 'Symbole', 'Name', 'Mondphase'),
          'fr': ('Jour', 'Phase', 'Symbole', 'Nom', 'Phase lunaire'),
          'es': ('Día', 'Fase', 'Símbolo', 'Nombre', 'Fase lunar'),
          'pt': ('Dia', 'Fase', 'Símbolo', 'Nome', 'Fase da Lua'),
          'it': ('Giorno', 'Fase', 'Simbolo', 'Nome', 'Fase lunari'),
          'af': ('Dag', 'Fase', 'Simbool', 'Naam', 'Maanfase'),
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
    # date and time
    utcnow = datetime.utcnow()
    dtstamp = utcnow.strftime('%Y%m%dT%H%M%SZ')
    
    # event UID
    uid_format='UID:%(date)s-%(pid)d-%(seq)04d-%(lang)s@%(domain)s\n'
    uid_replace_values = {
        'date': dtstamp,
        'pid':  getpid(),
        'domain': getfqdn()
    }
    event_seq = 1
 
    # open files for writing    
    tsv = open('moon-phases.tsv', 'w')
    tsv_new = open('new-moon.tsv', 'w')
    tsv_full = open('full-moon.tsv', 'w')
    tsv_all = open('moon-phases-all.tsv', 'w')
    md = open('moon-phases.md', 'w')
    md_new = open('new-moon.md', 'w')
    md_full = open('full-moon.md', 'w')
    md_all = open('moon-phases-all.md', 'w')
    ics = open('moon-phases.ics', 'w', newline='\r\n')
    ics_new = open('new-moon.ics', 'w', newline='\r\n')
    ics_full = open('full-moon.ics', 'w', newline='\r\n')
    
    # write headers
    tsv_header = '# {}\t# {}\t# {}\t# {}\n'.format(
        header[lang][0].ljust(10),
        header[lang][1],
        header[lang][2],
        header[lang][3])
    tsv_header_short = '# {}\t# {}\n'.format(
        header[lang][0],
        header[lang][1])
    tsv.write(tsv_header)
    tsv_all.write(tsv_header)
    tsv_new.write(tsv_header_short)
    tsv_full.write(tsv_header_short)
    md_header = '''# {}

{} | {} | {} | {}
-----------|-------:|---|---
'''.format(header[lang][4].title(), header[lang][0].ljust(10),
           header[lang][1].ljust(6),
           header[lang][2],
           header[lang][3])
    md_header_new = '''# {}

{} | {}
-----------|------:
'''.format(moon_phase_names[lang][4].title(), header[lang][0].ljust(10),
           header[lang][1])
    md_header_full = '''# {}

{} | {}
-----------|------:
'''.format(moon_phase_names[lang][4].title(), header[lang][0].ljust(10),
           header[lang][1])
    md.write(md_header)
    md_all.write(md_header)
    md_new.write(md_header_new)
    md_full.write(md_header_full)
    calendar_header = open('../templates/calendar-header-{}.txt'.format(lang))
    for line in calendar_header:
        ics.write(line.replace('Lunar Phase', header[lang][4].title()))
        ics_new.write(line.replace('Lunar Phase', moon_phase_names[lang][0].title()))
        ics_full.write(line.replace('Lunar Phase', moon_phase_names[lang][4].title()))

    # create event header
    event_header = ''
    for line in open('../templates/event-header.txt'):
        event_header += line.replace('DTSTAMP:', 'DTSTAMP:{}'.format(dtstamp))
    
    # create event footer
    event_footer = ''
    for line in open('../templates/event-footer.txt'):
        event_footer += line

    a = Astral()
    today = date.today()
    start = today - timedelta(days=31 + 1)
    end = today + timedelta(days=(2 * 366) + (2 * 31))
    for i in range((end - start).days):
        day = start + timedelta(days=i)
        phase, code = day_to_moon_phase_and_accurate_code(a, day)
        symbol = moon_phase_code_to_symbol(code)
        name = moon_phase_code_to_name(code, lang)
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
            ics.write('{}{} {}\n'.format(event_header.strip(), symbol, name))
            ics.write(uid_format % (dict(list(uid_replace_values.items()) + list({ 'lang': 'nl', 'seq': event_seq }.items()))))
            event_seq += 1
            ics_start = '{}'.format(day)
            ics_end = '{}'.format(day + timedelta(days=1))
            ics.write('DTSTART;VALUE=DATE:{}\n'.format(ics_start.replace('-', '')))
            ics.write('DTEND;VALUE=DATE:{}\n'.format(ics_end.replace('-', '')))
            ics.write(event_footer)
        if code == 0:
            tsv_new.write('{}\t{:6.3f}\n'.format(day, phase))
            md_new.write('{} | {:6.3f}\n'.format(day, phase,))
            ics_new.write('{}{} {}\n'.format(event_header.strip(), symbol, name))
            ics_new.write(uid_format % (dict(list(uid_replace_values.items()) + list({ 'lang': 'nl', 'seq': event_seq }.items()))))
            event_seq += 1
            ics_start = '{}'.format(day)
            ics_end = '{}'.format(day + timedelta(days=1))
            ics_new.write('DTSTART;VALUE=DATE:{}\n'.format(ics_start.replace('-', '')))
            ics_new.write('DTEND;VALUE=DATE:{}\n'.format(ics_end.replace('-', '')))
            ics_new.write(event_footer)
        if code == 4:
            tsv_full.write('{}\t{:6.3f}\n'.format(day, phase))
            md_full.write('{} | {:6.3f}\n'.format(day, phase,))
            ics_full.write('{}{} {}\n'.format(event_header.strip(), symbol, name))
            ics_full.write(uid_format % (dict(list(uid_replace_values.items()) + list({ 'lang': 'nl', 'seq': event_seq }.items()))))
            event_seq += 1
            ics_start = '{}'.format(day)
            ics_end = '{}'.format(day + timedelta(days=1))
            ics_full.write('DTSTART;VALUE=DATE:{}\n'.format(ics_start.replace('-', '')))
            ics_full.write('DTEND;VALUE=DATE:{}\n'.format(ics_end.replace('-', '')))
            ics_full.write(event_footer)

            
    calendar_footer = open('../templates/calendar-footer.txt')
    for line in calendar_footer:
        ics.write(line)
        ics_new.write(line)
        ics_full.write(line)

for lang in sorted(header.keys()):
    if not isdir(lang):
        makedirs(lang)
    chdir(lang)
    write_files(lang)
    chdir('..')
