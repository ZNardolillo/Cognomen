# ftfy is a lovely tool that just instantly fixes things that looked like they would take 2 hours to repair,
# or require doing another 2 hour activity over from scratch. It basically fixes misinterpreted special characters


import ftfy
x = '"Ã¡kron","Ã¡mÌ€ma","Ã¡mmÃ¡","É”kwÃ¡n"'
fixed = ftfy.fix_text(x)
print(fixed)

with open('output.py', 'r', encoding='utf-8') as f:
    fixed = ftfy.fix_text(f.read())

with open('all_js_scripts.py', 'w', encoding='utf-8') as f:
    f.write(fixed)