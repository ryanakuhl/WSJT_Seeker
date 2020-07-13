import pyperclip, time, os, glob, easygui, adif_io, json
from datetime import datetime
from pyhamtools import LookupLib, Callinfo
from scripts import qsl_lookup

wsjt_captured = []
needed_countries = []
countries_hunting_dict = json.load(open('C:\\Users\\#\\#\\#\\venv\\countries_hunting.txt', 'r'))
already_worked = json.load(open('C:\\Users\\#\\#\\#\\venv\\qsl_contacts.txt', 'r'))

countries_mastered = {}
[countries_mastered.update({a[0]: []}) for a in already_worked.values() if a[0] not in countries_mastered.keys()]
for c in already_worked.values():
    [countries_mastered.get(c[0]).append(x) for x in c[1] if x not in countries_mastered.get(c[0])]
countries_mastered ={k.upper().replace('ST.', 'SAINT'): v for k, v in countries_mastered.items()}

band_plan = {'160M': (1.8, 2),
             '80M': (3.5, 4),
             '40M': (7.175, 7.3),
             '20M': (14.0, 14.350),
             '17M': (18.06, 18.168),
             '15M': (21.0, 21.45),
             '12M': (24.93, 24.99),
             '10M': (28.0, 29.7),
             '6m': (50.0, 54.0)
             }


class WSJTSaw:
    def __init__(self, s):
        self.minutes_last_seen = round((datetime.utcnow() - datetime.strptime(s[0], '%y%m%d_%H%M%S')).total_seconds()/60)
        self.freq = s[1].split(' ')[0]
        self.band = ''
        for k in band_plan:
            if band_plan.get(k)[0] < float(self.freq) < band_plan.get(k)[1]:
                self.band = k
        self.mode = s[1].split(' ')[2]
        self.comments = [x for x in s[2].split(' ') if x]
        self.rx_country = self.comments[3]
        self.tx_country = self.comments[4]


class Countries:
    def __init__(self, c):
        self.country_call = c
        self.country = countries_hunting_dict.get(c)
        self.discovered = 'False'
        self.freq = ''
        self.band = ''
        self.last_seen = 10000000000000000000
        self.callsign = ''


for country in countries_hunting_dict:
    needed_countries.append(Countries(country))

fl = 'C:\\Users\\#\\#\\Local\\wsjt-x\\all.txt'
while True:
    if (datetime.now() - datetime.fromtimestamp(os.path.getmtime(fl))).total_seconds() < 5*60:
        with open(fl, 'r') as f:
            for line in f.readlines()[-500:]:
                wsjt_captured.append(WSJTSaw(line.rstrip().split('    ')))
        f.close()
    for a in needed_countries:
        for t in wsjt_captured:
            if a.country_call == t.tx_country[:len(a.country_call)]:
                setattr(a, 'discovered', 'True')
                setattr(a, 'band', t.band)
                setattr(a, 'callsign', t.tx_country)
                if t.minutes_last_seen < a.last_seen:
                    setattr(a, 'last_seen', t.minutes_last_seen)
    for a in needed_countries:
        if a.discovered == 'True':
            if a.country not in countries_mastered.keys():
                print(a.callsign, a.country, a.band, a.last_seen, 'minutes ago')
            elif a.country in countries_mastered:
                if a.band not in countries_mastered.get(a.country):
                    print(a.callsign, a.country, a.band, a.last_seen, 'minutes ago')
    print('~~~~~~~\n')
    time.sleep(5*60)
