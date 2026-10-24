#!/usr/bin/env python3
"""Refresh the public GitHub contribution snapshot; the site builds offline."""
import argparse
from datetime import date, datetime, timezone, timedelta
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/users/Semt0/contributions'


class Calendar(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.days, self.tooltips, self.active = {}, {}, None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'td' and attrs.get('data-date'):
            self.days[attrs['id']] = {'date': attrs['data-date'], 'level': int(attrs['data-level'])}
        if tag == 'tool-tip':
            self.active = attrs.get('for')

    def handle_data(self, text):
        if self.active:
            self.tooltips[self.active] = self.tooltips.get(self.active, '') + text

    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.active = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='Read a previously downloaded GitHub response')
    args = parser.parse_args()
    if args.input:
        text = args.input.read_text()
    else:
        request = Request(SOURCE, headers={'User-Agent': 'Semt0-blog-contribution-snapshot'})
        with urlopen(request, timeout=30) as response:
            text = response.read().decode('utf-8')
    calendar = Calendar(text)
    days = []
    for key, day in calendar.days.items():
        label = calendar.tooltips.get(key, '').strip()
        match = re.match(r'(?:(No)|([\d,]+)) contributions? on ', label)
        if not match or not 0 <= day['level'] <= 4:
            raise ValueError('Unrecognized GitHub contribution cell: ' + label)
        day['count'] = 0 if match[1] else int(match[2].replace(',', ''))
        days.append(day)
    days.sort(key=lambda day: day['date'])
    if not 350 <= len(days) <= 378:
        raise ValueError('Incomplete contribution calendar')
    first = date.fromisoformat(days[0]['date'])
    if any(date.fromisoformat(day['date']) != first + timedelta(days=i) for i, day in enumerate(days)):
        raise ValueError('The calendar must contain consecutive, unique dates')
    data = {'username': 'Semt0', 'source': SOURCE,
            'fetchedAt': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'from': days[0]['date'], 'to': days[-1]['date'],
            'total': sum(day['count'] for day in days), 'days': days}
    destination = ROOT / 'src/data/github-contributions.json'
    destination.write_text(json.dumps(data, indent=2) + '\n')
    print(f"Saved {len(days)} days, {data['total']} contributions ({data['from']} to {data['to']}).")


if __name__ == '__main__':
    main()
