#!/usr/bin/env python3
'''Generates calendars with lunar phase in iCal format.'''

from datetime import date, datetime, timedelta
from json import load
from os.path import isdir, realpath, join, dirname
from os import makedirs, chdir, getpid, getcwd
from socket import getfqdn
from astral import moon


__location__ = realpath(join(getcwd(), dirname(__file__)))
moon_phase_names = load(open(join(__location__, 'moon-phase-names.json'), encoding='utf8'))  # pylint:disable=consider-using-with
moon_phase_symbols = ('🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘')

# capitalized header values for day, phase, symbol, name and title
header = load(open(join(__location__, 'headers.json'), encoding='utf8'))  # pylint:disable=consider-using-with

# explicitely capitalize with title() all words
titles = ('en', 'pt')


def moon_phase_code_to_name(code, lang='en'):
    '''Converts moon phase code to name.'''
    return moon_phase_names[lang][code]


def moon_phase_code_to_symbol(code):
    '''Converts moon phase code to symbol.'''
    return moon_phase_symbols[code]


def moon_phase_to_inacurate_code(phase):
    '''Converts moon phase code to inacurate code.'''
    phase = int(phase)
    value = None
    if phase == 0:
        value = 0
    elif 0 < phase < 7:
        value = 1
    elif phase == 7:
        value = 2
    elif 7 < phase < 14:
        value = 3
    elif phase == 14:
        value = 4
    elif 14 < phase < 21:
        value = 5
    elif phase == 21:
        value = 6
    else:
        value = 7
    return value


def day_to_moon_phase_and_accurate_code(day):
    '''Converts day to moon phase and accurate code.'''
    phase_today = moon.phase(day)
    code_today = moon_phase_to_inacurate_code(phase_today)

    if code_today % 2 != 0:
        return phase_today, code_today

    phase_yesterday = moon.phase(day - timedelta(days=1))
    code_yesterday = moon_phase_to_inacurate_code(phase_yesterday)

    if code_today == code_yesterday:
        return phase_today, code_today + 1

    return phase_today, code_today


def write_files(lang='en'):
    '''Writes calendar files.'''
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
    tsv = open('moon-phases.tsv', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    tsv_new = open('new-moon.tsv', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    tsv_full = open('full-moon.tsv', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    tsv_all = open('moon-phases-all.tsv', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    mkd = open('moon-phases.md', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    mkd_new = open('new-moon.md', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    mkd_full = open('full-moon.md', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    mkd_all = open('moon-phases-all.md', 'w', encoding='utf8')  # pylint:disable=consider-using-with
    ics = open('moon-phases.ics', 'w', newline='\r\n', encoding='utf8')  # pylint:disable=consider-using-with
    ics_new = open('new-moon.ics', 'w', newline='\r\n', encoding='utf8')  # pylint:disable=consider-using-with
    ics_full = open('full-moon.ics', 'w', newline='\r\n', encoding='utf8')  # pylint:disable=consider-using-with

    # write headers
    tsv_header = f'# {header[lang][0].ljust(10)}\t# {header[lang][1]}\t# {header[lang][2]}\t# {header[lang][3]}\n'
    tsv_header_short = f'# {header[lang][0]}\t# {header[lang][1]}\n'
    tsv.write(tsv_header)
    tsv_all.write(tsv_header)
    tsv_new.write(tsv_header_short)
    tsv_full.write(tsv_header_short)
    title = header[lang][4]
    if lang in titles:
        title = title.title()
    mkd_header = f'''# {title}

{header[lang][0].ljust(10)} | {header[lang][1].ljust(6)} | {header[lang][2]} | {header[lang][3]}
-----------|-------:|---|---
'''
    title = moon_phase_names[lang][0]
    if lang in titles:
        title = title.title()
    mkd_header_new = f'''# {title}

{header[lang][0].ljust(10)} | {header[lang][1]}
-----------|------:
'''
    title = moon_phase_names[lang][4]
    if lang in titles:
        title = title.title()
    mkd_header_full = f'''# {title}

{header[lang][0].ljust(10)} | {header[lang][1]}
-----------|------:
'''
    mkd.write(mkd_header)
    mkd_all.write(mkd_header)
    mkd_new.write(mkd_header_new)
    mkd_full.write(mkd_header_full)
    calendar_header = open(f'../templates/calendar-header-{lang}.txt', encoding='utf8')  # pylint:disable=consider-using-with
    for line in calendar_header:
        if lang in titles:
            ics.write(line.replace('Lunar Phase', header[lang][4].title()))
            ics_new.write(line.replace('Lunar Phase', moon_phase_names[lang][0].title()))
            ics_full.write(line.replace('Lunar Phase', moon_phase_names[lang][4].title()))
        else:
            ics.write(line.replace('Lunar Phase', header[lang][4]))
            ics_new.write(line.replace('Lunar Phase', moon_phase_names[lang][0]))
            ics_full.write(line.replace('Lunar Phase', moon_phase_names[lang][4]))

    # create event header
    event_header = ''
    for line in open('../templates/event-header.txt', encoding='utf8'):  # pylint:disable=consider-using-with
        event_header += line.replace('DTSTAMP:', f'DTSTAMP:{dtstamp}')

    # create event footer
    event_footer = ''
    for line in open('../templates/event-footer.txt', encoding='utf8'):  # pylint:disable=consider-using-with
        event_footer += line

    today = date.today()
    start = today - timedelta(days=31 + 1)
    end = today + timedelta(days=(3 * 366) + (2 * 31))
    for i in range((end - start).days):
        day = start + timedelta(days=i)
        phase, code = day_to_moon_phase_and_accurate_code(day)
        symbol = moon_phase_code_to_symbol(code)
        name = moon_phase_code_to_name(code, lang)
        tsv_all.write('{}\t{:6.3f}\t{}\t{}\n'.format(day,
                                                     phase,
                                                     symbol,
                                                     name))
        mkd_all.write('{} | {:6.3f} | {} | {}\n'.format(day,
                                                       phase,
                                                       symbol,
                                                       name))
        if code % 2 == 0:
            tsv.write('{}\t{:6.3f}\t{}\t{}\n'.format(day,
                                                     phase,
                                                     symbol,
                                                     name))
            mkd.write('{} | {:6.3f} | {} | {}\n'.format(day,
                                                       phase,
                                                       symbol,
                                                       name))
            ics.write(f'{event_header.strip()}{symbol} {name}\n')
            ics.write(uid_format % (dict(
                list(uid_replace_values.items()) +
                list({ 'lang': 'nl', 'seq': event_seq }.items())))
            )
            event_seq += 1
            ics_start = f'{day}'
            ics_end = f'{day + timedelta(days=1)}'
            ics.write(f'DTSTART;VALUE=DATE:{ics_start.replace("-", "")}\n')
            ics.write(f'DTEND;VALUE=DATE:{ics_end.replace("-", "")}\n')
            ics.write(event_footer)
        if code == 0:
            tsv_new.write('{}\t{:6.3f}\n'.format(day, phase))
            mkd_new.write('{} | {:6.3f}\n'.format(day, phase,))
            ics_new.write(f'{event_header.strip()}{symbol} {name}\n')
            ics_new.write(uid_format % (dict(
                list(uid_replace_values.items()) +
                list({ 'lang': 'nl', 'seq': event_seq }.items())))
            )
            event_seq += 1
            ics_start = f'{day}'
            ics_end = f'{day + timedelta(days=1)}'
            ics_new.write(f'DTSTART;VALUE=DATE:{ics_start.replace("-", "")}\n')
            ics_new.write(f'DTEND;VALUE=DATE:{ics_end.replace("-", "")}\n')
            ics_new.write(event_footer)
        if code == 4:
            tsv_full.write('{}\t{:6.3f}\n'.format(day, phase))
            mkd_full.write('{} | {:6.3f}\n'.format(day, phase,))
            ics_full.write(f'{event_header.strip()}{symbol} {name}\n')
            ics_full.write(uid_format % (dict(
                list(uid_replace_values.items()) +
                list({ 'lang': 'nl', 'seq': event_seq }.items())))
            )
            event_seq += 1
            ics_start = f'{day}'
            ics_end = f'{day + timedelta(days=1)}'
            ics_full.write(f'DTSTART;VALUE=DATE:{ics_start.replace("-", "")}\n')
            ics_full.write(f'DTEND;VALUE=DATE:{ics_end.replace("-", "")}\n')
            ics_full.write(event_footer)

    calendar_footer = open('../templates/calendar-footer.txt', encoding='utf8')  # pylint:disable=consider-using-with
    for line in calendar_footer:
        ics.write(line)
        ics_new.write(line)
        ics_full.write(line)

for language in sorted(header.keys()):
    if not isdir(language):
        makedirs(language)
    chdir(language)
    write_files(language)
    chdir('..')
