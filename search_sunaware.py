import os
TERMS=['SunAware','sunaware','SUN AWARE','SUNAWARE']
SKIP={'venv','node_modules','dist','build','__pycache__','.git','.idea','.vscode'}
for dirpath, dirnames, filenames in os.walk('.'):
    dirnames[:]=[d for d in dirnames if d not in SKIP]
    for name in filenames:
        path=os.path.join(dirpath,name)
        try:
            with open(path,'r',encoding='utf-8') as fh:
                for idx,line in enumerate(fh,1):
                    lower=line.lower()
                    for term in TERMS:
                        if term.lower() in lower:
                            print('{}:{}:{}'.format(path,idx,line.rstrip()))
                            break
        except Exception:
            continue
