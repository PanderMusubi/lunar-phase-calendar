#!/usr/bin/env python3
'''Generates calendars with lunar phase in iCal format.'''

from datetime import date, datetime, timedelta
from json import load
from os.path import isdir, realpath, join, dirname
from os import makedirs, chdir, getpid, getcwd
from socket import getfqdn
from astral.moon import phase

__location__ = realpath(join(getcwd(), dirname(__file__)))
moon_phase_names = load(open(join(__location__, 'moon-phase-names.json'), encoding='utf8'))  # pylint:disable=consider-using-with
moon_phase_symbols = ('🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘')

countries = load(open(join(__location__, 'countries.json'), encoding='utf8'))  # pylint:disable=consider-using-with

# capitalized header values for day, phase, symbol, name and title
header = load(open(join(__location__, 'headers.json'), encoding='utf8'))  # pylint:disable=consider-using-with

# explicitely capitalize with title() all words
titles = ('en', 'pt')


def moon_phase_code_to_name(code: str, lang: str = 'en') -> str:
    '''Converts moon phase code to name.'''
    return moon_phase_names[lang][code]


def moon_phase_code_to_symbol(code: int) -> str:
    '''Converts moon phase code to symbol.'''
    return moon_phase_symbols[code]


def moon_phase_to_inacurate_code(phase: float) -> int:
    '''Converts moon phase code to inacurate code.'''
    value = int(phase)
    res = None
    if value == 0:
        res = 0
    elif 0 < value < 7:
        res = 1
    elif value == 7:
        res = 2
    elif 7 < value < 14:
        res = 3
    elif value == 14:
        res = 4
    elif 14 < value < 21:
        res = 5
    elif value == 21:
        res = 6
    else:
        res = 7
    return res


def day_to_moon_phase_and_accurate_code(day: date) -> tuple:
    '''Converts day to moon phase and accurate code.'''
    phase_today = phase(day)
    code_today = moon_phase_to_inacurate_code(phase_today)

    phase_yesterday = phase(day - timedelta(days=1))
    code_yesterday = moon_phase_to_inacurate_code(phase_yesterday)

    if (code_today - code_yesterday) % 8 > 1:
        # skipped one code, hence do correction
        return phase_today, (code_today - 1) % 8

    if code_today % 2 != 0:
        return phase_today, code_today

    if code_today == code_yesterday:
        return phase_today, (code_today + 1) % 8

    return phase_today, code_today


def write_files(country: str, lang: str) -> None:
    '''Writes calendar files.'''
    # date and time
    utcnow = datetime.utcnow()
    dtstamp = utcnow.strftime('%Y%m%dT%H%M%SZ')

    # event UID
    uid_format = 'UID:%(date)s-%(pid)d-%(seq)04d-%(lang)s@%(domain)s\n'
    uid_replace_values = {
        'date': dtstamp,
        'pid': getpid(),
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
    ics_all = open('moon-phases-all.ics', 'w', newline='\r\n', encoding='utf8')  # pylint:disable=consider-using-with

    # write headers
    tsv_header = f'# {header[lang][0].ljust(10)}\t# {header[lang][1]}\t#' \
        f' {header[lang][2]}\t# {header[lang][3]}\n'
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
    calendar_header = open(f'../../templates/calendar-header-{country}.txt', encoding='utf8')  # pylint:disable=consider-using-with
    for line in calendar_header:
        if lang in titles:
            ics.write(line.replace('Lunar Phase', header[lang][4].title()))
            ics_new.write(line.replace('Lunar Phase', moon_phase_names[lang][0].title()))
            ics_full.write(line.replace('Lunar Phase', moon_phase_names[lang][4].title()))
            ics_all.write(line.replace('Lunar Phase', header[lang][4].title()))
        else:
            ics.write(line.replace('Lunar Phase', header[lang][4]))
            ics_new.write(line.replace('Lunar Phase', moon_phase_names[lang][0]))
            ics_full.write(line.replace('Lunar Phase', moon_phase_names[lang][4]))
            ics_all.write(line.replace('Lunar Phase', header[lang][4]))

    # create event header
    event_header = ''
    for line in open('../../templates/event-header.txt', encoding='utf8'):  # pylint:disable=consider-using-with
        event_header += line.replace('DTSTAMP:', f'DTSTAMP:{dtstamp}')

    # create event footer
    event_footer = ''
    for line in open('../../templates/event-footer.txt', encoding='utf8'):  # pylint:disable=consider-using-with
        event_footer += line  # pylint:disable=consider-using-join

    today = date.today()
    start = today - timedelta(days=31 + 1)
    end = today + timedelta(days=(3 * 366) + (2 * 31))
    for i in range((end - start).days):
        day = start + timedelta(days=i)
        phase, code = day_to_moon_phase_and_accurate_code(day)
        symbol = moon_phase_code_to_symbol(code)
        name = moon_phase_code_to_name(code, lang)
        tsv_all.write(f'{day}\t{phase:6.3f}\t{symbol}\t{name}\n')
        mkd_all.write(f'{day} | {phase:6.3f} | {symbol} | {name}\n')
        ics_all.write(f'{event_header.strip()}{symbol} {name}\n')
        ics_all.write(uid_format % (dict(
            list(uid_replace_values.items()) + list({'lang': 'nl',
                                                     'seq': event_seq}.items())))
        )
        event_seq += 1
        ics_start = f'{day}'
        ics_end = f'{day + timedelta(days=1)}'
        ics_all.write(f'DTSTART;VALUE=DATE:{ics_start.replace("-", "")}\n')
        ics_all.write(f'DTEND;VALUE=DATE:{ics_end.replace("-", "")}\n')
        ics_all.write(event_footer)
        if code % 2 == 0:
            tsv.write(f'{day}\t{phase:6.3f}\t{symbol}\t{name}\n')
            mkd.write(f'{day} | {phase:6.3f} | {symbol} | {name}\n')
            ics.write(f'{event_header.strip()}{symbol} {name}\n')
            ics.write(uid_format % (dict(
                list(uid_replace_values.items()) + list({'lang': 'nl',
                                                         'seq': event_seq}.items())))
            )
            event_seq += 1
            ics_start = f'{day}'
            ics_end = f'{day + timedelta(days=1)}'
            ics.write(f'DTSTART;VALUE=DATE:{ics_start.replace("-", "")}\n')
            ics.write(f'DTEND;VALUE=DATE:{ics_end.replace("-", "")}\n')
            ics.write(event_footer)
        if code == 0:
            tsv_new.write(f'{day}\t{phase:6.3f}\n')
            mkd_new.write(f'{day} | {phase:6.3f}\n')
            ics_new.write(f'{event_header.strip()}{symbol} {name}\n')
            ics_new.write(uid_format % (dict(
                list(uid_replace_values.items()) + list({'lang': 'nl',
                                                         'seq': event_seq}.items())))
            )
            event_seq += 1
            ics_start = f'{day}'
            ics_end = f'{day + timedelta(days=1)}'
            ics_new.write(f'DTSTART;VALUE=DATE:{ics_start.replace("-", "")}\n')
            ics_new.write(f'DTEND;VALUE=DATE:{ics_end.replace("-", "")}\n')
            ics_new.write(event_footer)
        if code == 4:
            tsv_full.write(f'{day}\t{phase:6.3f}\n')
            mkd_full.write(f'{day} | {phase:6.3f}\n')
            ics_full.write(f'{event_header.strip()}{symbol} {name}\n')
            ics_full.write(uid_format % (dict(
                list(uid_replace_values.items()) + list({'lang': 'nl',
                                                         'seq': event_seq}.items())))
            )
            event_seq += 1
            ics_start = f'{day}'
            ics_end = f'{day + timedelta(days=1)}'
            ics_full.write(f'DTSTART;VALUE=DATE:{ics_start.replace("-", "")}\n')
            ics_full.write(f'DTEND;VALUE=DATE:{ics_end.replace("-", "")}\n')
            ics_full.write(event_footer)

    calendar_footer = open('../../templates/calendar-footer.txt', encoding='utf8')  # pylint:disable=consider-using-with
    for line in calendar_footer:
        ics.write(line)
        ics_new.write(line)
        ics_full.write(line)
        ics_all.write(line)


def generate():
    '''Generate files.'''
    for country in sorted(countries.keys()):
        if not isdir(country):
            makedirs(country)
        chdir(country)
        for language in sorted(countries[country]):
            if not isdir(language):
                makedirs(language)
            chdir(language)
            write_files(country, language)
            chdir('..')
        chdir('..')


if __name__ == '__main__':
    generate()
