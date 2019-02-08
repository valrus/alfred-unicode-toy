# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import argparse
import codecs
import itertools
import json
import os
import string
import sys

TRANSLATION_BASE = string.printable.strip()

TRANSLATIONS = {
    "Circled": '''0①②③④⑤⑥⑦⑧⑨ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ!"#$%&⦸'()⊛⊕,⊖⨀⊘:;⧀⊜⧁?@[⦸⦸]^_`{⦶}~''',
    "Circled (neg)": '''⓿123456789🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Fullwidth": '''０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！"＃＄％＆＼＇（）＊＋，－．／：；<＝>？＠［＼＼］＾＿｀｛｜｝～''',
    "Math bold": '''𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math bold Fraktur": '''0123456789𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math bold italic": '''0123456789𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math bold script": '''0123456789𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math double-struck": '''𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math monospace": '''𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math sans": '''𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math sans bold": '''𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math sans bold italic": '''0123456789𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math sans italic": '''0123456789𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Parenthesized": '''0⑴⑵⑶⑷⑸⑹⑺⑻⑼⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Regional Indicator": '''0123456789🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Squared": '''0123456789🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉!"#$%&⧅'()⧆⊞,⊟⊡⧄:;<=>?@[⧅⧅]^_`{|}~''',
    "Squared (neg)": '''0123456789🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "A-cute": '''0123456789ábćdéfǵhíjḱĺḿńőṕqŕśtúvẃxӳźÁBĆDÉFǴHíJḰĹḾŃŐṔQŔśTŰVẂXӲŹ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "CJK+Thai": '''0123456789ﾑ乃cd乇ｷgんﾉﾌズﾚﾶ刀oｱq尺丂ｲu√wﾒﾘ乙ﾑ乃cd乇ｷgんﾉﾌズﾚﾶ刀oｱq尺丂ｲu√wﾒﾘ乙!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Curvy 1": '''0123456789ค๒ƈɗﻉिﻭɦٱﻝᛕɭ๓กѻρ۹ɼรՇપ۷ฝซץչค๒ƈɗﻉिﻭɦٱﻝᛕɭ๓กѻρ۹ɼรՇપ۷ฝซץչ!"#$%&\'()*+,-܁/:;<=>?@[\\]^_`{|}~''',
    "Curvy 2": '''0123456789αв¢∂єƒﻭнιנкℓмησρ۹яѕтυνωχуչαв¢∂єƒﻭнιנкℓмησρ۹яѕтυνωχуչ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Curvy 3": '''0123456789ค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Faux Cyrillic": '''0123456789аъсↁэfБЂіјкlмиорqѓѕтцvшхЎzДБҀↁЄFБНІЈЌLМИФРQЯЅГЦVЩЖЧZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Faux Ethiopic": '''0123456789ልጌርዕቿቻኗዘጎጋጕረጠክዐየዒዪነፕሁሀሠሸሃጊልጌርዕቿቻኗዘጎጋጕረጠክዐየዒዪነፕሁሀሠሸሃጊ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Math Fraktur": '''0123456789𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Rock Dots": '''012ӟ456789äḅċḋëḟġḧïjḳḷṁṅöṗqṛṡẗüṿẅẍÿżÄḄĊḊЁḞĠḦЇJḲḶṀṄÖṖQṚṠṪÜṾẄẌŸŻ!"#$%&\'()*+,⸚∵/:;<=>?@[\\]^_`{|}~''',
    "Small Caps": '''0123456789ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴩqʀꜱᴛᴜᴠᴡxyᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴩQʀꜱᴛᴜᴠᴡxYᴢ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Stroked": '''01ƻ3456789ȺƀȼđɇfǥħɨɉꝁłmnøᵽꝗɍsŧᵾvwxɏƶȺɃȻĐɆFǤĦƗɈꝀŁMNØⱣꝖɌSŦᵾVWXɎƵ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Subscript": '''₀₁₂₃₄₅₆₇₈₉ₐbcdₑfgₕᵢⱼₖₗₘₙₒₚqᵣₛₜᵤᵥwₓyzₐBCDₑFGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥWₓYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Superscript": '''⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖqʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''',
    "Inverted": '''0123456789ɐqɔpǝɟƃɥıɾʞןɯuodbɹsʇnʌʍxʎzɐqɔpǝɟƃɥıɾʞןɯuodbɹsʇn𐌡ʍxʎz¡"#$%⅋\,()*+‘-./:;<=>¿@[\\]^_`{|}~''',
    "Reversed": '''0߁23456789AdↄbɘꟻgHijklmᴎoqpᴙꙅTUvwxYzAdↃbƎꟻGHIJK⅃MᴎOꟼpᴙꙄTUVWXYZ!"#$%&\'()*+,-./:⁏<=>⸮@[\\]^_`{|}∽'''
}


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.

    From https://docs.python.org/2/library/itertools.html#recipes
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def getUTF16Chars(s):
    """Get a list of UTF-16 representations of the chars in a word.

    In particular, surrogate pairs will be kept together for chars outside the BMP.

    Logic: encode the string to UTF-32, split it to 4-byte chunks, then decode each chunk.
    Because each 4-byte chunk represents a single character in utf32, decoding non-BMP chars will
    produce utf-16 surrogate pairs on narrow Python builds and single unicode chars on wide builds.
    """
    return [b''.join(u32_bytes).decode('utf-32be') for u32_bytes in grouper(s.encode('utf-32be'), 4)]


def ordUTF32(u32c):
    return int(u32c.encode('hex'), 16)


def make_item(title, text):
    encoded_text = text.encode('utf-8')
    return dict(
        title=title,
        subtitle=encoded_text,
        valid=True,
        arg=json.dumps({
            'alfredworkflow': {
                'arg': encoded_text,
            }
        }),
        icon='icon.png',
        autocomplete=title,
        text={
            'copy': encoded_text,
            'largetype': encoded_text
        }
    )


def toy_translate(text, result_string):
    # A normal translate dict doesn't work because of the narrow Python build;
    # characters outside the BMP are expressed as surrogate pairs so aren't suitable.
    toy_map = dict(zip(TRANSLATION_BASE, getUTF16Chars(result_string)))
    return ''.join([ toy_map.get(c, c) for c in text ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    args = parser.parse_args()

    query = args.query.decode('utf-8')

    print(json.dumps({
        'items': [
            make_item(translation_name, toy_translate(query, translation_string))
            for translation_name, translation_string in TRANSLATIONS.iteritems()
        ]
    }))


if __name__ == '__main__':
    main()
