python -c "
import sys; print('Python:', sys.executable)
import pkg_resources; 
langs = [p for p in pkg_resources.working_set if 'langchain' in p.project_name.lower()]
for lang in langs: print(f'{lang.project_name}: {lang.version}')
try:
    import langchain.agents; print('langchain.agents contents:', [x for x in dir(langchain.agents) if 'create' in x.lower()])
except: print('Import failed')
"
