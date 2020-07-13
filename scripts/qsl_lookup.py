import easygui, adif_io, time, json
from pyhamtools import LookupLib, Callinfo

already_worked = json.load(open('C:\\Users\\#\\#\\#\\venv\\qsl_contacts.txt', 'r'))
with open(easygui.fileopenbox(), 'r') as f:
    lotw = [a for a in adif_io.read_from_string(f.read())[0] if a.get('QSL_RCVD') == 'Y']
f.close()

print(len(lotw) - len(already_worked), 'new qsos')
for a in lotw:
    try:
        callsign = a.get('CALL')
        band = a.get('BAND')
        if callsign not in already_worked.keys():
            my_lookuplib = LookupLib(lookuptype="countryfile")
            cic = Callinfo(my_lookuplib)
            country = cic.get_all(callsign).get('country')
            already_worked[callsign] = [country, [band]]
            time.sleep(2)
            if lotw.index(a) % 10 == 0:
                json.dump(already_worked, open("C:\\Users\\#\\#\\#\\venv\\qsl_contacts.txt", 'w'))
                print(len(already_worked), lotw.index(a))
        elif band not in already_worked.get(callsign)[1]:
            already_worked.get(callsign)[1].append(band)
    except:
        pass

json.dump(already_worked, open("C:\\Users\\#\\#\\#\\venv\\qsl_contacts.txt", 'w'))
