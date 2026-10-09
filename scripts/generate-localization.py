#!/usr/bin/env python3
"""Generate the standard .strings resource from reviewed UTF-8 translations."""
from pathlib import Path
from collections import Counter
import json,re,subprocess
root=Path(__file__).resolve().parent.parent
translations={}
pattern=r'%(?:\d+\$)?(?:@|lld|ld|d|f|g|s|u|llu)|%%'
for number,line in enumerate((root/'localization/translations.tsv').read_text().splitlines(),1):
    if not line: continue
    key,value=line.split('\t',1)
    if key in translations and translations[key]!=value:
        raise ValueError(f'Conflicting translation at line {number}: {key}')
    if Counter(re.findall(pattern,key))!=Counter(re.findall(pattern,value)):
        raise ValueError(f'Format placeholders differ at line {number}: {key}')
    translations[key]=value
for key,value in list(translations.items()):
    for variant in [key.lower(),key[:1].lower()+key[1:]]:
        translations.setdefault(variant,value)
    if not key.endswith('…'):
        translations.setdefault(key+'…',value+'…')
# Deliberately unchanged technical names and numeric-only strings need no translation.
keys=set()
for path in (root/'build/localization').glob('*.stringsdata'):
    obj=json.loads(path.read_text())
    keys.update(entry['key'] for entry in obj.get('tables',{}).get('Localizable',[]))
missing=[k for k in sorted(keys) if k not in translations and re.search('[A-Za-z]',k) and k not in {'Compositor','px','sRGB','RGB','PNG','JPEG','PDF','HSL'} and not re.fullmatch(r'[%@lld0-9 ×°·]+',k)]
resource=root/'Compositor/zh-Hans.lproj/Localizable.strings'
resource.parent.mkdir(exist_ok=True)
resource.write_text('/* Compositor 1.4.8 Simplified Chinese, local patch. */\n'+''.join(f'{json.dumps(k,ensure_ascii=False)} = {json.dumps(v,ensure_ascii=False)};\n' for k,v in sorted(translations.items())))
subprocess.run(['plutil','-lint',str(resource)],check=True)
report={'translation_pairs':len(translations),'native_keys':len(keys),'missing_native_keys':missing}
(root/'build/localization-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
