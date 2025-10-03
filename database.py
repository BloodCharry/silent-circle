import aiosqlite, os, json, datetime
DB_FILE = os.getenv('DATABASE_FILE', './data/silentcircle.db')

async def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            full_name TEXT,
            status TEXT,
            status_meta TEXT,
            about TEXT,
            photo_file_id TEXT,
            state TEXT,
            created_at TEXT,
            updated_at TEXT,
            can_edit_name INTEGER DEFAULT 1
        )''')
        await db.commit()

async def create_or_update_user(telegram_id, full_name=None, status=None, status_meta=None, state=None):
    async with aiosqlite.connect(DB_FILE) as db:
        cur = await db.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
        row = await cur.fetchone()
        now = datetime.datetime.utcnow().isoformat()
        if row:
            updates = []
            params = []
            if full_name is not None:
                updates.append('full_name = ?'); params.append(full_name)
            if status is not None:
                updates.append('status = ?'); params.append(status)
            if status_meta is not None:
                updates.append('status_meta = ?'); params.append(status_meta)
            if state is not None:
                updates.append('state = ?'); params.append(state)
            if updates:
                updates.append('updated_at = ?'); params.append(now)
                sql = 'UPDATE users SET ' + ', '.join(updates) + ' WHERE telegram_id = ?'
                params.append(telegram_id)
                await db.execute(sql, params)
                await db.commit()
            cur = await db.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
            row = await cur.fetchone()
            return dict(zip([column[0] for column in cur.description], row))
        else:
            await db.execute('INSERT INTO users (telegram_id, full_name, status, status_meta, state, created_at, updated_at) VALUES (?,?,?,?,?,?,?)', (telegram_id, full_name, status, status_meta, state or 'collecting', now, now))
            await db.commit()
            cur = await db.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
            row = await cur.fetchone()
            return dict(zip([column[0] for column in cur.description], row))

async def get_user_by_tg(telegram_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cur = await db.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        row = await cur.fetchone()
        if not row:
            return None
        return dict(zip([column[0] for column in cur.description], row))

async def update_user_by_tg(telegram_id, **kwargs):
    keys = []
    params = []
    for k,v in kwargs.items():
        if k in ('full_name','status','status_meta','about','photo_file_id','state','can_edit_name'):
            keys.append(f"{k} = ?")
            params.append(v)
    if not keys:
        return False
    params.append(datetime.datetime.utcnow().isoformat())
    keys.append('updated_at = ?')
    params.append(telegram_id)
    sql = 'UPDATE users SET ' + ', '.join(keys) + ' WHERE telegram_id = ?'
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(sql, params)
        await db.commit()
    return True

async def list_pending_users():
    async with aiosqlite.connect(DB_FILE) as db:
        cur = await db.execute('SELECT * FROM users WHERE state = ?', ('pending',))
        rows = await cur.fetchall()
        return [dict(zip([column[0] for column in cur.description], row)) for row in rows]
