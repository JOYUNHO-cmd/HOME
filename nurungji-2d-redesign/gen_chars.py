"""내사랑 누룽지 7종 캐릭터를 2D 게임 스타일 SVG로 생성해 content.js와 characters/*.svg에 반영."""
import json, math, re, sys

INK = '#3B2026'
SW = 6

CHARS = {
    'fresh':       dict(shape='round',  fill='#F6C760', hi='#FFE29A', dots='#FFF7DF', acc='sprout',  mood='happy'),
    'seven-boil':  dict(shape='round',  fill='#E3AE6E', hi='#F6D3A0', dots='multi',   acc='scarf',   mood='wink'),
    'barley':      dict(shape='round',  fill='#B98457', hi='#D9A97A', dots='#F3DDC0', acc='barley',  mood='happy'),
    'almond':      dict(shape='square', fill='#F2B45C', hi='#FFD98F', dots='almond',  acc='almond',  mood='happy'),
    'oat':         dict(shape='square', fill='#EBD3A0', hi='#FFF0C9', dots='#FFFFFF', acc='leaf',    mood='wink'),
    'seven-snack': dict(shape='square', fill='#EE9B63', hi='#FFC596', dots='multi',   acc='ribbon',  mood='wow'),
    'black':       dict(shape='square', fill='#7E5A92', hi='#A585B8', dots='#D9C6E6', acc='star',    mood='happy'),
}

CX, CY = 160, 150


def blob(cx, cy, rx, ry, bumps, amp, square=False):
    pts = []
    n = 180
    for i in range(n):
        t = 2 * math.pi * i / n
        c, s = math.cos(t), math.sin(t)
        if square:
            p = 4.0
            r = (abs(c) ** p + abs(s) ** p) ** (-1 / p)
        else:
            r = 1.0
        k = 1 + amp * math.sin(bumps * t)
        pts.append((cx + rx * r * c * k, cy + ry * r * s * k))
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
    return d


def dots_svg(kind, shape):
    import random
    rnd = random.Random(7)
    out = []
    multi = ['#FFFFFF', '#3B2026', '#8BC34A', '#E85D75', '#FFD54F']
    for _ in range(26):
        while True:
            x = rnd.uniform(-78, 78); y = rnd.uniform(-70, 74)
            if shape == 'round' and x * x / 86 ** 2 + y * y / 80 ** 2 > 0.8:
                continue
            if -46 < x < 46 and -40 < y < 40:  # 얼굴 영역 비우기
                continue
            break
        a = rnd.uniform(0, 180)
        if kind == 'almond':
            out.append(f'<ellipse cx="{CX+x:.1f}" cy="{CY+y:.1f}" rx="7" ry="4.5" fill="#FFF1D6" stroke="{INK}" stroke-width="2" transform="rotate({a:.0f} {CX+x:.1f} {CY+y:.1f})"/>')
        else:
            col = rnd.choice(multi) if kind == 'multi' else kind
            out.append(f'<ellipse cx="{CX+x:.1f}" cy="{CY+y:.1f}" rx="5" ry="2.6" fill="{col}" opacity=".95" transform="rotate({a:.0f} {CX+x:.1f} {CY+y:.1f})"/>')
    return ''.join(out)


def accessory(acc):
    top = CY - 92
    if acc == 'sprout':
        return (f'<path d="M160 {top+8} V{top-14}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                f'<path d="M160 {top-12} Q140 {top-34} 122 {top-22} Q140 {top-6} 160 {top-12} Z" fill="#7ED36A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M160 {top-14} Q180 {top-40} 200 {top-28} Q182 {top-8} 160 {top-14} Z" fill="#9BE07F" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    if acc == 'barley':
        g = ''.join(f'<ellipse cx="{160+(9 if i%2 else -9)}" cy="{top-6-i*11}" rx="7" ry="10" fill="#E8B96A" stroke="{INK}" stroke-width="3.5" transform="rotate({(25 if i%2 else -25)} {160+(9 if i%2 else -9)} {top-6-i*11})"/>' for i in range(4))
        return f'<path d="M160 {top+10} V{top-46}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>' + g
    if acc == 'almond':
        return (f'<path d="M160 {top-34} Q186 {top-6} 160 {top+12} Q134 {top-6} 160 {top-34} Z" fill="#C98A4B" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round" transform="rotate(18 160 {top-10})"/>'
                f'<path d="M156 {top-20} Q150 {top-8} 156 {top+2}" stroke="#E7B27A" stroke-width="4" fill="none" stroke-linecap="round" transform="rotate(18 160 {top-10})"/>')
    if acc == 'leaf':
        return (f'<path d="M150 {top+6} Q138 {top-30} 168 {top-44} Q178 {top-10} 150 {top+6} Z" fill="#8FD47A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M152 {top} Q158 {top-20} 166 {top-34}" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if acc == 'ribbon':
        return (f'<path d="M160 {top+4} L128 {top-18} Q120 {top+4} 128 {top+24} Z" fill="#FF7E95" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                f'<path d="M160 {top+4} L192 {top-18} Q200 {top+4} 192 {top+24} Z" fill="#FF7E95" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                f'<circle cx="160" cy="{top+4}" r="9" fill="#FFB3C1" stroke="{INK}" stroke-width="4.5"/>')
    if acc == 'star':
        pts = []
        for i in range(10):
            r = 24 if i % 2 == 0 else 11
            a = -math.pi / 2 + i * math.pi / 5
            pts.append(f'{160 + r*math.cos(a):.1f} {top-12 + r*math.sin(a):.1f}')
        return f'<path class="nr-twinkle" d="M{" L".join(pts)} Z" fill="#FFD54F" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
    return ''


def scarf():
    return (f'<path d="M98 {CY+40} Q160 {CY+70} 222 {CY+40} L224 {CY+58} Q160 {CY+90} 96 {CY+58} Z" fill="#6CC27A" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
            f'<path d="M200 {CY+60} L210 {CY+100} L190 {CY+98} L186 {CY+64} Z" fill="#6CC27A" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
            f'<path d="M120 {CY+56} L124 {CY+66} M150 {CY+64} L152 {CY+74} M180 {CY+63} L178 {CY+73}" stroke="#4E9E5C" stroke-width="3.5" stroke-linecap="round"/>')


def face(mood):
    ex, ey = 26, CY - 6
    blush = (f'<ellipse cx="{CX-50}" cy="{CY+14}" rx="13" ry="8" fill="#FF7E95" opacity=".6"/>'
             f'<ellipse cx="{CX+50}" cy="{CY+14}" rx="13" ry="8" fill="#FF7E95" opacity=".6"/>')
    def eye(x):
        return (f'<g class="nr-eye"><ellipse cx="{x}" cy="{ey}" rx="11" ry="14" fill="{INK}"/>'
                f'<circle cx="{x+4}" cy="{ey-6}" r="5" fill="#fff"/><circle cx="{x-4}" cy="{ey+5}" r="2.2" fill="#fff"/></g>')
    if mood == 'wow':
        eyes = eye(CX - ex) + eye(CX + ex)
        mouth = f'<ellipse cx="{CX}" cy="{CY+22}" rx="10" ry="12" fill="{INK}"/><ellipse cx="{CX}" cy="{CY+28}" rx="6" ry="4" fill="#FF7E95"/>'
    else:
        right = (f'<path d="M{CX+ex-12} {ey+2} Q{CX+ex} {ey-12} {CX+ex+12} {ey+2}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                 if mood == 'wink' else eye(CX + ex))
        eyes = eye(CX - ex) + right
        mouth = (f'<path d="M{CX-15} {CY+14} Q{CX} {CY+38} {CX+15} {CY+14} Z" fill="{INK}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                 f'<ellipse cx="{CX}" cy="{CY+27}" rx="7" ry="4.5" fill="#FF7E95"/>')
    return blush + eyes + mouth


def build(cid, c, name, nick):
    sq = c['shape'] == 'square'
    rx, ry = (94, 86) if not sq else (90, 84)
    body = blob(CX, CY, rx, ry, 16 if not sq else 20, 0.035 if not sq else 0.02, square=sq)
    hi = blob(CX - 10, CY - 12, rx * 0.62, ry * 0.5, 10, 0.03, square=sq)
    limbs = (f'<g stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none">'
             f'<path d="M136 {CY+80} V{CY+106}"/><path d="M184 {CY+80} V{CY+106}"/></g>'
             f'<path d="M116 {CY+116} Q116 {CY+100} 134 {CY+100} H144 V{CY+122} H124 Q116 {CY+122} 116 {CY+116} Z" fill="#FF7E95" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
             f'<path d="M204 {CY+116} Q204 {CY+100} 186 {CY+100} H176 V{CY+122} H196 Q204 {CY+122} 204 {CY+116} Z" fill="#FF7E95" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    arms = (f'<g class="nr-arm-l"><path d="M{CX-rx+6} {CY+16} Q{CX-rx-26} {CY+26} {CX-rx-26} {CY+52}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/>'
            f'<circle cx="{CX-rx-26}" cy="{CY+58}" r="13" fill="#fff" stroke="{INK}" stroke-width="5"/></g>'
            f'<g class="nr-arm-r"><path d="M{CX+rx-6} {CY+6} Q{CX+rx+28} {CY-6} {CX+rx+26} {CY-40}" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/>'
            f'<circle cx="{CX+rx+26}" cy="{CY-46}" r="13" fill="#fff" stroke="{INK}" stroke-width="5"/></g>')
    steam = ''
    if c['shape'] == 'round':
        steam = (f'<g class="nr-steam" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".9">'
                 f'<path d="M58 70 q-10 -14 0 -28 q10 -14 0 -28"/><path d="M262 76 q-10 -14 0 -28 q10 -14 0 -28"/></g>')
    else:
        steam = (f'<g class="nr-crunch" fill="#FFD54F" stroke="{INK}" stroke-width="3">'
                 f'<path d="M48 64 l6 -16 l6 16 l16 6 l-16 6 l-6 16 l-6 -16 l-16 -6 z"/><path d="M266 54 l4 -10 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 z"/></g>')
    dots = dots_svg(c['dots'], c['shape'])
    extra = scarf() if c['acc'] == 'scarf' else ''
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 300" role="img" aria-label="{name} 캐릭터 {nick}" class="nr-chr">'
           f'<ellipse class="nr-shadow" cx="{CX}" cy="282" rx="72" ry="10" fill="{INK}" opacity=".16"/>'
           f'{steam}<g class="nr-hop">{limbs}{arms}'
           f'<path d="{body}" fill="{c["fill"]}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
           f'<path d="{hi}" fill="{c["hi"]}" opacity=".65"/>{dots}'
           f'<path d="M{CX-62} {CY-50} Q{CX-50} {CY-68} {CX-30} {CY-72}" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none" opacity=".85"/>'
           f'{accessory(c["acc"])}{extra}{face(c["mood"])}</g></svg>')
    return svg


def main(root):
    src = open(f'{root}/content.js', encoding='utf-8').read()
    data = json.loads(src[src.index('=') + 1:].rstrip().rstrip(';'))
    for p in data['products']:
        svg = build(p['id'], CHARS[p['id']], p['name'], p['nick'])
        p['svg'] = svg
        open(f'{root}/characters/{p["id"]}.svg', 'w', encoding='utf-8').write(svg)
    open(f'{root}/content.js', 'w', encoding='utf-8').write('window.SITE_CONTENT=' + json.dumps(data, ensure_ascii=False) + ';\n')
    print('ok', len(data['products']))


if __name__ == '__main__':
    main(sys.argv[1])
