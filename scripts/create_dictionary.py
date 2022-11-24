import PyPDF2
from langdetect import detect
from tqdm import tqdm

f = open("/Users/ayman/Desktop/artr.pdf", 'rb')

reader = PyPDF2.PdfFileReader(f)

dd = {}

for i in tqdm(range(reader.numPages)):
    p = reader.getPage(i)
    for line in p.extract_text().split('\n'):
        if 'turkish-learn' in line:
            continue

        if 'تعلم اللغة الرتكية' in line:
            continue

        if line == 'الكلمة باللغة الرتكيةالكلمة باللغة العربية':
            continue

        c = None
        for w in line.split():
            try:
                if detect(w) == 'ar':
                    c = w
                    break
            except:
                continue
        if c:
            idx = line.find(c)
            dd[line[:idx].strip()] = line[idx:].strip()