# Lunar Phase Calendar

Roling ICS calendars with
[lunar phases](https://en.wikipedia.org/wiki/Lunar_phase) for two years in
advance.

Besides calendars with all the lunars phases, there are also calendars provided
with only the dates when there is a new or full moon. The calendars are
generated for different languages and in the formats:
* tab-separated format in TSV files, e.g. `en/moon-phases.tsv`
* MarkDown in MD files, e.g. `nl/new-moon.md`
* iCalendar in ICS files, e.g. `de/full-moon.ics`

The calendars are generated on a certain day for two years in advance and is
published in this repository. At the time of generation, a margin is used of one
month at the beginning and of two months at the end.

The calendars will be regenerated regularly. Browse around in order to find the
lunar phase calendar you are looking for. In case a calendar is lagging behind
too much, you want to contribute a translation or report a bug or feature,
please create an issue.


## Screenshots

![Thunderbird](images/thunderbird.png)

<img alt="Android" src="images/android.png" width="50%" />


## Calendar Software

Probably, you already have software installed for using online calendars. If
that is not the case, lunar phase calendars can be shown with:

| Name              | Android | iOS | macOS | Windows | Linux | Web interface |
|-------------------|:-------:|:---:|:-----:|:-------:|:-----:|:------------:|
| Google Calendar   | [✔](https://play.google.com/store/apps/details?id=com.google.android.calendar) | - | - | - | - | [✔](https://google.com/calendar) |
| ICSx⁵             | [✔](https://play.google.com/store/apps/details?id=at.bitfire.icsdroid) | - | - | - | - | - |
| CalDAV-Sync       | [✔](https://play.google.com/store/apps/details?id=org.dmfs.caldav.lib) | - | - | - | - | - |
| iCloud Calendar   | - | [✔](https://www.apple.com/icloud/#ccm) | - | - | - | - |
| Thunderbird       | - | - | [✔](https://www.thunderbird.net) | [✔](https://www.thunderbird.net) | [✔](https://www.thunderbird.net) | - |
| Apple Calendar    | - | - | [✔](https://www.apple.com/macos/what-is) | - | - | - |
| Microsoft Outlook | - | - | - | [✔](https://products.office.com/outlook) | - | [✔](https://outlook.com) |

Check marks in the table have links to the software. ICSx⁵ can also be found in
the [F-Droid](https://f-droid.org/repository/browse/?fdfilter=calendar&fdid=at.bitfire.icsdroid)
app store. Do **not** use software that can only import ICS files.


## Using ICS Files in Calendar Software

After you have copied the URL of an ICS file, please paste this in your calendar
software when adding a (read-only) online network or ICS calendar. Sometimes
this is called to subscribe to a calendar. Usually you can choose how often
synchronization has to be done to keep your lunar phase calendar up to date. Set
this to 24 hours, because there are not that many updates. Again, do **not**
choose the (one time) import of the ICS calender as it will not update itself.


## Emoji

Emoji support moon phases, hence the following Unicode characters are use in the
output files:
1. 🌑 [`U+1F311`](https://emojipedia.org/new-moon-symbol/) New moon
2. 🌒 [`U+1F312`](https://emojipedia.org/waxing-crescent-moon-symbol/) Waxing
crescent
3. 🌓 [`U+1F313`](https://emojipedia.org/first-quarter-moon-symbol/) First
quarter
4. 🌔 [`U+1F314`](https://emojipedia.org/waxing-gibbous-moon-symbol/) Waxing
gibbous
5. 🌕 [`U+1F315`](https://emojipedia.org/full-moon-symbol/) Full moon
6. 🌖 [`U+1F316`](https://emojipedia.org/waning-gibbous-moon-symbol/) Waning
gibbous
7. 🌗 [`U+1F317`](https://emojipedia.org/last-quarter-moon-symbol/) Last quarter
8. 🌘 [`U+1F318`](https://emojipedia.org/waning-crescent-moon-symbol/) Waning
crescent
