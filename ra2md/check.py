import re

f = open('rulesmd.ini', 'r')

weapons = {}
attribs = [
    'Damage',
    'ROF',
    'Range',
    'Speed',
    'Burst'
]
skip_weapons = ['20mmRapid']

title = ''
for line in f:
    # [(\w+)]
    match = re.match(r'\[(\w+)\]', line)
    if match:
        title = match.group(1)
    if not title or title in skip_weapons:
        continue
    for attrib in attribs:
        match = re.match(rf'{attrib}=(\d+)', line)
        if match:
            value = int(match.group(1))
            if title not in weapons:
                weapons[title] = {}
            weapons[title][attrib] = value
f.close()


def CheckDps(attr1, attr2, weapon):
    damage1 = attr1.get('Damage', 0)
    rof1 = attr1.get('ROF', 1)
    burst1 = attr1.get('Burst', 1)
    dps1 = damage1 * burst1 / float(rof1)
    damage2 = attr2.get('Damage', 0)
    rof2 = attr2.get('ROF', 1)
    burst2 = attr2.get('Burst', 1)
    dps2 = damage2 * burst2 / float(rof2)
    if dps1 > dps2:
        print(f'{weapon} DPS {dps2:.2f}=damage({damage2})*burst({burst2}))/rof({rof2}) < {dps1:.2f}=damage({damage1})*burst({burst1}))/rof({rof1})')
        return False


def CheckAttr(attr1, attr2, weapon, attr):
    value1 = attr1.get(attr, 0)
    value2 = attr2.get(attr, 0)
    if value1 > value2:
        print(f'{weapon} {attr} {value2} < {value1}')
        return False


for weapon, attribs in weapons.items():
    if f'{weapon}E' in weapons:
        attrib1 = weapons[weapon]
        attrib2 = weapons[f'{weapon}E']
        CheckDps(attrib1, attrib2, weapon)
        CheckAttr(attrib1, attrib2, weapon, 'Range')
        CheckAttr(attrib1, attrib2, weapon, 'Speed')
