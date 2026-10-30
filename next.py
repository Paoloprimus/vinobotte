import glob,re,sys
n=int(sys.argv[1]) if len(sys.argv)>1 else 2
done=set()
for f in glob.glob('spec/*.txt'):
    m=re.search(r'dominio: (\S+)',open(f).read())
    if m: done.add(m.group(1))
done|={'accordini.it'}
rest=[d for d in open('coda.txt').read().split() if d not in done]
print(len(rest),'rimaste');print(' '.join(rest[:n]))
