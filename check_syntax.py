import ast
import sys

files = [
    'backend/app.py',
    'backend/utils.py',
    'backend/models.py',
    'backend/routes/auth_routes.py',
    'backend/routes/trip_routes.py',
    'backend/routes/alert_routes.py',
    'backend/utils/gps_utils.py',
    'backend/utils/notifications.py',
    'backend/extensions.py',
    'run.py'
]

errors = []
for f in files:
    try:
        with open(f, 'r') as file:
            ast.parse(file.read())
    except SyntaxError as e:
        errors.append(f'{f}: {e}')

if errors:
    print('Syntax errors found:')
    for e in errors:
        print(e)
else:
    print('No syntax errors found.')
