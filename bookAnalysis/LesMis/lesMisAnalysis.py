import os
from glob import glob
from collections import Counter
import pandas as pd
from pandas import DataFrame as DF

writer = pd.ExcelWriter("Summary.xlsx")

for bk in [x[0] for x in os.walk('.')]:
    sers = []
    if bk == '.':
        continue
    for ch in glob(bk + os.path.sep + '*.txt'):
        freq = Counter()
        with open(ch) as f:
            for line in f:
                for word in line.split():
                    # import pdb; pdb.set_trace()
                    freq.update([word.strip(',.?!;:')])
                # freq.update(line.split())

        sers.append(DF(pd.Series(freq, name=ch.split(os.path.sep)[2][:-4])))

    df = sers[0].join(sers[1:])
    df = df.fillna(0)
    df.to_excel(writer, 'livre %i' % (int(bk[2]) + 1))

writer.save()

    # df.append((bk[2:], sers[0].join(sers[1:])))
