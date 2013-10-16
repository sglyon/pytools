import os
import re

book_name = 'LesMis'  # Folder name where to find main file
file_name = "lesMisTomeOne.txt"  # Name of main file from folder above
book = open(book_name + os.path.sep + file_name).read().lower()

level_labels = ('livre.+--.+', 'chapitre\s+[ivxlcdm]+')

res = [re.compile("(^%s)" % i, re.MULTILINE) for i in level_labels]

book_inds = [(m.start(), m.end()) for m in res[0].finditer(book)]
book_inds.append((-1, -1))

for i, b in enumerate(book_inds):
    if b[0] == -1:
        break
    b_name = book[b[0]:b[1]].strip()
    b_text = book[b[0]:book_inds[i+1][0] - 1].strip()
    b_dir = book_name + os.path.sep + str(i) + b_name
    if not os.path.exists(b_dir):
        os.makedirs(b_dir)
    chap_inds = [(m.start(), m.end()) for m in res[1].finditer(b_text)]
    chap_inds.append((-1, -1))
    for k, c in enumerate(chap_inds):
        if c[0] == -1:
            break
        c_name = b_text[c[0]:c[1]].strip()
        c_text = b_text[c[0]:chap_inds[k+1][0] - 1].strip()
        f = open(b_dir + os.path.sep + c_name + '.txt', 'w')
        f.write(c_text)
