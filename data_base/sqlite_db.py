import sqlite3 as sq
from create_bot import bot

def sql_start():
    global base, cur
    base = sq.connect('ProGames_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.execute('''CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price TEXT,
            quantity INTEGER,
            total_price TEXT
        )''')
    base.commit()

# Функція для додавання товару з таблиці "menu" до таблиці "purchases"
async def sql_add_to_cart(product_name):
    product = cur.execute('SELECT * FROM menu WHERE name = ?', (product_name,)).fetchone()
    if product:
        cur.execute('INSERT INTO purchases (name, description, price, quantity, total_price) VALUES (?, ?, ?, ?, ?)',
                    (product[1], product[2], product[3], 1, product[3]))
        base.commit()
        return True
    else:
        return False

# Функція для читання замовлених товарів з таблиці purchases
async def sql_read_purchases():
    cursor = base.cursor()
    cursor.execute('SELECT * FROM purchases')
    rows = cursor.fetchall()
    return rows

# Функція для отримання інформації про товар за назвою
async def sql_get_product(product_name):
    return cur.execute('SELECT * FROM menu WHERE name = ?', (product_name,)).fetchone()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОпис: {ret[2]}\nЦіна {ret[-1]}')

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

async def sql_delete_all_items():
    cur.execute('DELETE FROM purchases')
    base.commit()

async def sql_delete_from_cart(product_name):
    cur.execute('DELETE FROM purchases WHERE name = ?', (product_name,))
    base.commit()
