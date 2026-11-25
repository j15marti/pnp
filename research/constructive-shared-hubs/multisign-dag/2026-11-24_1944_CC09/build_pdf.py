#!/usr/bin/env python3
"""Render the companion LaTeX through Pandoc AST and ReportLab.

Dependencies: pandoc; Python reportlab, matplotlib, Pillow. The mathematical
source stays in the .tex file. Every math expression must render successfully;
unsupported expressions fail the build rather than appearing as raw TeX.
"""
from pathlib import Path
import hashlib
import html
import io
import json
import re
import subprocess

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['mathtext.fontset'] = 'dejavuserif'
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                               Spacer, PageBreak, Image, Table, TableStyle,
                               HRFlowable, XPreformatted, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent
STEM = 'PNP_Best_Proof_Attempt_CC09_2026-11-24'
TMP = ROOT / 'render_work'
TMP.mkdir(exist_ok=True)
WIDTH = 482.4
MATH_CACHE = {}
MATH_RECORDS = []
UNKNOWN = []
SOURCE_URLS = {}
for match in re.finditer(r'@misc\{([^,\n]+),([\s\S]*?)(?=\n@misc|\Z)', (ROOT / 'references.bib').read_text()):
    url = re.search(r'\\(?:href|url)\{([^}]+)\}', match.group(2))
    if url:
        SOURCE_URLS['ref-' + match.group(1)] = url.group(1).replace('\\#', '#')


for name, family, weight, style in [
    ('Body', 'DejaVu Serif', 'normal', 'normal'),
    ('Body-Bold', 'DejaVu Serif', 'bold', 'normal'),
    ('Body-Italic', 'DejaVu Serif', 'normal', 'italic'),
    ('Body-BoldItalic', 'DejaVu Serif', 'bold', 'italic'),
    ('Head', 'DejaVu Sans', 'normal', 'normal'),
    ('Head-Bold', 'DejaVu Sans', 'bold', 'normal'),
    ('Mono', 'DejaVu Sans Mono', 'normal', 'normal'),
]:
    path = font_manager.findfont(FontProperties(family=family, weight=weight, style=style))
    pdfmetrics.registerFont(TTFont(name, path))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Body-Bold', italic='Body-Italic', boldItalic='Body-BoldItalic')
pdfmetrics.registerFontFamily('Head', normal='Head', bold='Head-Bold', italic='Head', boldItalic='Head-Bold')
NAVY = colors.HexColor('#16334A')
BASE = ParagraphStyle('body', fontName='Body', fontSize=10.35, leading=15.1,
                      spaceAfter=7.5, allowWidows=0, allowOrphans=0)
STYLES = {
    'body': BASE,
    'cell': ParagraphStyle('cell', parent=BASE, fontSize=9.1, leading=12.5, spaceAfter=1),
    'h1': ParagraphStyle('h1', fontName='Head-Bold', fontSize=17, leading=21, textColor=NAVY,
                         spaceBefore=16, spaceAfter=10, keepWithNext=True),
    'h2': ParagraphStyle('h2', fontName='Head-Bold', fontSize=12.1, leading=16.3, textColor=NAVY,
                         spaceBefore=13, spaceAfter=7, keepWithNext=True),
    'small': ParagraphStyle('small', parent=BASE, fontSize=9.2, leading=13.2),
    'reference': ParagraphStyle('reference', parent=BASE, fontSize=9.0, leading=11.8, spaceAfter=4.5),
    'code': ParagraphStyle('code', fontName='Mono', fontSize=8.2, leading=11,
                           borderWidth=.4, borderColor=colors.HexColor('#D4DDE4'),
                           backColor=colors.HexColor('#F5F7F8'), borderPadding=8, spaceBefore=5, spaceAfter=10),
}


def esc(s):
    return html.escape(s.replace('\u2013', '-').replace('\u2014', '-'), quote=True)


def norm_math(s):
    s = re.sub(r'\\label\{[^}]*\}', '', s)
    s = re.sub(r'\\(mathbb|mathbf|mathcal|mathrm|mathsf)\s*([A-Za-z0-9])', r'\\\1{\2}', s)
    s = re.sub(r'\\le(?![A-Za-z])', r'\\leq', s)
    s = re.sub(r'\\ge(?![A-Za-z])', r'\\geq', s)
    s = re.sub(r'\\ne(?![A-Za-z])', r'\\neq', s)
    s = re.sub(r'\\lor(?![A-Za-z])', r'\\vee', s)
    s = re.sub(r'\\sqrt\s*([A-Za-z0-9])', r'\\sqrt{\1}', s)
    s = re.sub(r'\\binom\s*([A-Za-z0-9])\s*([A-Za-z0-9])', r'\\binom{\1}{\2}', s)
    s = re.sub(r'\\pmod\s*\{([^}]*)\}', r'\ (\\mathrm{mod}\ \1)', s)
    s = re.sub(r'\\pmod\s*([A-Za-z0-9])', r'\ (\\mathrm{mod}\ \1)', s)
    s = s.replace('\\notag', '').replace('\\,', r'\,').replace('\n', ' ')
    return s.strip()


def math_asset(tex, size=10.5):
    normalized = norm_math(tex)
    key = (normalized, size)
    if key in MATH_CACHE:
        return MATH_CACHE[key]
    name = hashlib.sha256(repr(key).encode()).hexdigest()[:24] + '.png'
    path = TMP / name
    if not path.exists():
        math_to_image('$' + normalized + '$', str(path), prop=FontProperties(size=size), dpi=450, format='png', color='#111111')
    with PILImage.open(path) as im:
        w, h = im.size
    ans = (path, w * 72 / 450, h * 72 / 450)
    MATH_CACHE[key] = ans
    MATH_RECORDS.append({'original': tex, 'normalized': normalized, 'size': size, 'width': ans[1], 'height': ans[2]})
    return ans


def inlines(nodes, size=10.5):
    out = []
    for x in nodes:
        t, c = x['t'], x.get('c')
        if t == 'Str': out.append(esc(c))
        elif t in ('Space', 'SoftBreak'): out.append(' ')
        elif t == 'LineBreak': out.append('<br/>')
        elif t in ('Strong', 'Emph'):
            tag = 'b' if t == 'Strong' else 'i'
            out.append('<'+tag+'>'+inlines(c, size)+'</'+tag+'>')
        elif t == 'Math':
            p, w, h = math_asset(c[1], size)
            out.append(f'<img src="{p}" width="{w:.3f}" height="{h:.3f}" valign="-2.4"/>')
        elif t == 'Code': out.append('<font name="Mono" size="'+str(size*.88)+'">'+esc(c[1])+'</font>')
        elif t == 'Link':
            link = c[2][0]
            if link.startswith('#'):
                out.append('<link href="'+esc(link)+'" color="#174D72">'+inlines(c[1], size)+'</link>')
            else: out.append('<link href="'+esc(link)+'" color="#174D72">'+inlines(c[1], size)+'</link>')
        elif t == 'Cite': out.append(inlines(c[1], size))
        elif t == 'Span':
            if c[0][0]: out.append('<a name="'+esc(c[0][0])+'"/>')
            out.append(inlines(c[1], size))
        elif t == 'Quoted': out.append('“'+inlines(c[1], size)+'”')
        elif t in ('Superscript','Subscript'):
            tag='super' if t=='Superscript' else 'sub';out.append('<'+tag+'>'+inlines(c,size)+'</'+tag+'>')
        elif t == 'RawInline':
            if c[1].strip() not in ('\\qedhere', ''): UNKNOWN.append(x)
        else: UNKNOWN.append(x)
    return ''.join(out)


def plain(nodes):
    return re.sub('<[^>]+>', '', inlines(nodes))


def display_math(tex, width=WIDTH):
    if '\\begin{array}' in tex:
        # The sole array is the explicit affine-plane partition table.
        rows = [['Partition', 'Triple 1', 'Triple 2', 'Triple 3'],
                ['P1','012','345','678'],['P2','036','147','258'],
                ['P3','048','156','237'],['P4','057','138','246']]
        tab=Table(rows, colWidths=[90,80,80,80], hAlign='CENTER')
        tab.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Head'),('FONTSIZE',(0,0),(-1,-1),10),
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EDF2F6')),('LINEBELOW',(0,0),(-1,0),.6,NAVY),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        return [KeepTogether([Spacer(1,5),tab,Spacer(1,10)])]
    if '\\begin{aligned}' in tex:
        tex=tex.replace('\\begin{aligned}','').replace('\\end{aligned}','')
        lines=[s.replace('&','') for s in tex.split('\\\\')]
    else: lines=[tex]
    out=[Spacer(1,3)]
    for line in lines:
        if not norm_math(line):continue
        p,w,h=math_asset(line,11.5)
        scale=min(1.0,width/w)
        im=Image(str(p),width=w*scale,height=h*scale);im.hAlign='CENTER'
        out.append(im);out.append(Spacer(1,6))
    return out


def para_flow(nodes, style='body', width=WIDTH):
    out=[];buf=[]
    for n in nodes:
        if n['t']=='Math' and n['c'][0]['t']=='DisplayMath':
            if buf and inlines(buf).strip():out.append(Paragraph(inlines(buf),STYLES[style]))
            buf=[];out.extend(display_math(n['c'][1],width))
        else:buf.append(n)
    if buf and inlines(buf).strip():out.append(Paragraph(inlines(buf,STYLES[style].fontSize),STYLES[style]))
    return out


class Paper(BaseDocTemplate):
    def __init__(self, path):
        super().__init__(str(path),pagesize=(612,792),leftMargin=64.8,rightMargin=64.8,
                         topMargin=60,bottomMargin=57,title='Constructive P versus NP: Best Current Proof Attempt',
                         author='Research synthesis for j15marti/pnp',pageCompression=1)
        frame=Frame(self.leftMargin,self.bottomMargin,self.width,self.height,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='paper',frames=frame,onPage=self.header))
    def header(self,c,doc):
        if doc.page==1:return
        c.saveState();c.setFont('Head',8);c.setFillColor(NAVY)
        c.drawString(64.8,757,'CONSTRUCTIVE P VERSUS NP RESEARCH')
        c.drawRightString(547.2,757,'CC09 | 24 NOVEMBER 2026')
        c.setStrokeColor(colors.HexColor('#D0DAE2'));c.line(64.8,748,547.2,748)
        c.setFont('Head',8);c.drawCentredString(306,30,str(doc.page));c.restoreState()
    def afterFlowable(self,f):
        if hasattr(f,'section_info'):
            level,title,key=f.section_info
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=level,closed=False)
            if level==0:self.notify('TOCEntry',(0,title,self.page,key))


SECTION=0
SUBSECTION=0
def render_blocks(blocks, width=WIDTH, cell=False, reference=False):
    global SECTION,SUBSECTION
    ans=[]
    for b in blocks:
        t,c=b['t'],b.get('c')
        if t in ('Para','Plain'):ans.extend(para_flow(c,'cell' if cell else 'reference' if reference else 'body',width))
        elif t=='Header':
            level,attr,nodes=c
            text=plain(nodes)
            if level==1:
                if text=='Reproduction and artifact map':
                    ans.append(PageBreak());prefix='Appendix A. '
                else:SECTION+=1;prefix=str(SECTION)+'. '
                SUBSECTION=0
            else:SUBSECTION+=1;prefix=f'{SECTION}.{SUBSECTION} '
            p=Paragraph('<a name="'+esc(attr[0])+'"/>'+esc(prefix)+inlines(nodes),STYLES['h1' if level==1 else 'h2'])
            p.section_info=(0 if level==1 else 1,prefix+text,attr[0])
            ans.append(p)
        elif t=='Div':
            attr,sub=c
            if 'titlepage' in attr[1]:continue
            if attr[0]=='refs':
                ans.append(PageBreak())
                p=Paragraph('References',STYLES['h1']);p.section_info=(0,'References','references');ans.append(p)
            if attr[0]:ans.append(Paragraph('<a name="'+esc(attr[0])+'"/>',ParagraphStyle('anchor',fontSize=1,leading=0,spaceAfter=0,keepWithNext=True)))
            new=render_blocks(sub,width,cell,reference or attr[0]=='refs')
            if 'csl-entry' in attr[1] and attr[0] in SOURCE_URLS:
                if len(sub) != 1 or sub[0]['t'] != 'Para':
                    raise ValueError('Unexpected reference structure: ' + attr[0])
                new=[Paragraph('<link href="'+esc(SOURCE_URLS[attr[0]])+'">'+inlines(sub[0]['c'],9.0)+'</link>', STYLES['reference'])]
            if any(s in attr[1] for s in ('theorem','lemma','proposition','corollary','conjecture')):
                gap=Spacer(1,4);gap.keepWithNext=True;ans.append(gap)
            ans.extend([KeepTogether(new)] if 'csl-entry' in attr[1] else new)
        elif t=='Table':
            attr,caption,colspec,head,bodies,foot=c
            rows=head[1]+[row for body in bodies for row in body[2]+body[3]]+foot[1]
            cols=len(colspec)
            ratio=[.20,.47,.33] if cols==3 else [.29,.71] if cols==2 else [1/cols]*cols
            widths=[width*r for r in ratio]
            data=[]
            for row in rows:
                data.append([render_blocks(v[4],widths[j]-13,True) for j,v in enumerate(row[1])])
            tab=Table(data,colWidths=widths,repeatRows=len(head[1]),hAlign='LEFT')
            tab.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),
                ('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E9F0F5')),('LINEBELOW',(0,0),(-1,0),.7,NAVY),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F7F9FA')]),
                ('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#B5C4D0'))]))
            ans.extend([Spacer(1,3),tab,Spacer(1,10)])
        elif t in ('BulletList','OrderedList'):
            items=c[1] if t=='OrderedList' else c
            for item in items:ans.extend(render_blocks(item,width,cell,reference))
        elif t=='CodeBlock':
            # Wrap only display lines; original full commands remain in the .tex.
            lines=[]
            for line in c[1].splitlines():
                while len(line)>88:
                    cut=line.rfind(' ',0,88)
                    if cut<25:cut=88
                    lines.append(line[:cut]+' \\');line='    '+line[cut:].lstrip()
                lines.append(line)
            ans.append(XPreformatted(esc('\n'.join(lines)),STYLES['code']))
        elif t=='HorizontalRule':ans.append(HRFlowable(width='100%',color=colors.HexColor('#BDCAD4'),thickness=.7,spaceBefore=8,spaceAfter=8))
        elif t=='RawBlock':
            if c[1].strip() not in ('\\newpage','\\tableofcontents','\\appendix'):UNKNOWN.append(b)
        else:UNKNOWN.append(b)
    return ans


def cover(blocks):
    contents=blocks[0]['c'][1]
    out=[Spacer(1,26)]
    styles=[ParagraphStyle('eyebrow',fontName='Head-Bold',fontSize=9,leading=12,textColor=NAVY,spaceAfter=26),
            ParagraphStyle('title',fontName='Head-Bold',fontSize=30,leading=37,textColor=NAVY,spaceAfter=14),
            ParagraphStyle('subtitle',fontName='Head',fontSize=22,leading=28,textColor=NAVY,spaceAfter=16),
            ParagraphStyle('desc',fontName='Head',fontSize=12.6,leading=18,spaceAfter=0),
            ParagraphStyle('desc2',fontName='Head',fontSize=12.6,leading=18,spaceAfter=18),
            ParagraphStyle('date',fontName='Head',fontSize=10,leading=14,spaceAfter=10)]
    for i,b in enumerate(contents):
        if b['t']=='Para' and i<6:out.append(Paragraph(inlines(b['c']),styles[i]))
        elif b['t']=='Para':out.extend(para_flow(b['c'],'small'))
        elif b['t']=='HorizontalRule':out.append(HRFlowable(width='100%',thickness=.8,color=NAVY,spaceBefore=7,spaceAfter=11))
    out.append(PageBreak())
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc',fontName='Body',fontSize=10.7,leading=16,spaceBefore=7,leftIndent=0,firstLineIndent=0)]
    out.extend([Paragraph('Contents',STYLES['h1']),Spacer(1,13),toc,PageBreak()])
    return out


def main():
    subprocess.run(['pandoc','-f','latex','-t','json','--citeproc','--bibliography='+str(ROOT/'references.bib'),
                    '--csl='+str(ROOT/'research-numeric.csl'),str(ROOT/(STEM+'.tex')),'-o',str(TMP/'ast.json')],check=True)
    ast=json.loads((TMP/'ast.json').read_text())
    story=cover(ast['blocks'])+render_blocks(ast['blocks'][1:])
    if UNKNOWN:raise ValueError('Unhandled AST nodes: '+repr(UNKNOWN)[:4000])
    doc=Paper(ROOT/(STEM+'.pdf'))
    doc.multiBuild(story)
    (TMP/'math_render_audit.json').write_text(json.dumps({'count':len(MATH_RECORDS),'expressions':MATH_RECORDS},indent=2))
    print(json.dumps({'pdf':str(ROOT/(STEM+'.pdf')),'math_expressions':len(MATH_RECORDS),'pages':doc.page,'unhandled_nodes':len(UNKNOWN)},indent=2))


if __name__=='__main__':main()
