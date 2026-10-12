"""Deterministic daily look for Steadfast shorts. palette = date.toordinal() % 6, treatment = date.toordinal() % 5 (30-day cycle)."""
import datetime
PALETTES=[  # all on site --bg #07070a; accents stay in the site/logo family
 dict(name='Periwinkle (site hero)', a=(91,110,245), b=(80,40,160), acc=(139,156,255)),
 dict(name='Logo gold',              a=(201,169,110), b=(90,60,30),  acc=(214,186,132)),
 dict(name='Midnight violet',        a=(120,80,210), b=(40,25,90),   acc=(185,166,255)),
 dict(name='Slate',                  a=(110,120,140), b=(40,45,58),  acc=(200,200,208)),
 dict(name='Deep teal',              a=(50,130,140), b=(20,50,70),   acc=(140,205,210)),
 dict(name='Steel blue',             a=(70,120,190), b=(25,45,95),   acc=(150,185,255)),
]
TREATMENTS=['mesh+grid (site hero)','spotlight+grain+vignette','diagonal light sweep','horizon band','soft cloud texture']
def style_for(date):
    o=date.toordinal(); return PALETTES[o%6], TREATMENTS[o%5]
if __name__=='__main__':
    for i in range(7):
        d=datetime.date(2026,10,12)+datetime.timedelta(i); p,t=style_for(d); print(d,p['name'],'|',t)
