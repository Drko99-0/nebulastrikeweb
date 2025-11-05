import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('pyserver/dev.db')
cursor = conn.cursor()

print('=== Estado de VisualCache para jugadores 18-21 ===')
cursor.execute('''
    SELECT registrant_id, riotId, tagline, updatedAt, lastError, nextRetryAt, retryAttempts,
           CASE WHEN LENGTH(data) > 200 THEN SUBSTR(data, 1, 200) || '...' ELSE data END as data_preview
    FROM VisualsCache 
    WHERE registrant_id IN (18, 19, 20, 21)
    ORDER BY registrant_id
''')

for row in cursor.fetchall():
    rid, riot_id, tagline, updated_at, last_error, next_retry, attempts, data_preview = row
    print(f'\nJugador {rid} ({riot_id}#{tagline}):')
    print(f'  updatedAt: {updated_at}')
    print(f'  lastError: {last_error}')
    print(f'  nextRetryAt: {next_retry}')
    print(f'  retryAttempts: {attempts}')
    print(f'  data_preview: {data_preview}')
    
    # Verificar si hay datos válidos
    try:
        if data_preview and not data_preview.endswith('...'):
            data_obj = json.loads(data_preview)
            has_valid_data = (data_obj.get('status') != 'pending' and 
                            (data_obj.get('top') or data_obj.get('account') or data_obj.get('mmr')))
            print(f'  has_valid_data: {has_valid_data}')
            print(f'  status: {data_obj.get("status", "N/A")}')
        else:
            print(f'  data_truncated: True')
    except Exception as e:
        print(f'  data_parse_error: {e}')

conn.close()