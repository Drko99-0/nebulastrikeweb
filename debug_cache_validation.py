import sqlite3
import json
from datetime import datetime, timedelta

def test_cache_validation():
    conn = sqlite3.connect('pyserver/dev.db')
    cursor = conn.cursor()
    
    # Obtener configuración del worker
    cursor.execute("SELECT value FROM WorkerConfig WHERE key = 'visuals_cache_ttl_hours'")
    ttl_row = cursor.fetchone()
    cache_ttl_hours = int(ttl_row[0]) if ttl_row else 24
    cache_ttl = timedelta(hours=cache_ttl_hours)
    
    print(f'=== Configuración de caché ===')
    print(f'cache_ttl_hours: {cache_ttl_hours}')
    print(f'cache_ttl: {cache_ttl}')
    print(f'now_utc: {datetime.utcnow()}')
    
    print(f'\n=== Validación de caché para jugadores 18-21 ===')
    cursor.execute('''
        SELECT registrant_id, riotId, tagline, updatedAt
        FROM VisualsCache 
        WHERE registrant_id IN (18, 19, 20, 21)
        ORDER BY registrant_id
    ''')
    
    for row in cursor.fetchall():
        rid, riot_id, tagline, updated_at_str = row
        print(f'\nJugador {rid} ({riot_id}#{tagline}):')
        print(f'  updatedAt (str): {updated_at_str}')
        
        # Parsear la fecha
        try:
            # Intentar diferentes formatos de fecha
            updated_at = None
            for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S']:
                try:
                    updated_at = datetime.strptime(updated_at_str, fmt)
                    break
                except ValueError:
                    continue
            
            if updated_at:
                print(f'  updatedAt (parsed): {updated_at}')
                time_diff = datetime.utcnow() - updated_at
                print(f'  time_diff: {time_diff}')
                is_valid = time_diff < cache_ttl
                print(f'  is_cache_valid: {is_valid}')
                print(f'  time_diff < cache_ttl: {time_diff} < {cache_ttl} = {is_valid}')
            else:
                print(f'  ERROR: Could not parse date')
                
        except Exception as e:
            print(f'  ERROR parsing date: {e}')
    
    conn.close()

if __name__ == "__main__":
    test_cache_validation()