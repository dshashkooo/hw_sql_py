import password as token

conn = token.key


# Функция для создания таблиц
def create_db_structure():
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        client_id INT REFERENCES clients(id),
        phone_number TEXT UNIQUE
    );
    """)
    conn.commit()
    cur.close()


# Функция для добавления нового клиента в базу данных
def add_client(first_name, last_name, email=None):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO clients (first_name, last_name, email)
    VALUES (%s, %s, %s)""", (first_name, last_name, email))
    conn.commit()
    cur.close()


# Функция для добавления телефона для существующего клиента
def add_phone(client_id, phone_number):
    cur = conn.cursor()
    cur.execute("INSERT INTO phones (client_id, phone_number) VALUES (%s, %s)", (client_id, phone_number))
    conn.commit()
    cur.close()


# Функция для изменения данных о клиенте
def update_client(client_id, **kwargs):
    if not kwargs:
        return  # Если нет данных для обновления, выходим из функции

    cur = conn.cursor()
    updates = []
    for key, value in kwargs.items():
        if key == 'phone_numbers':
            # Если переданы новые телефонные номера, обновляем их
            for phone_number in value:
                cur.execute("INSERT INTO phones (client_id, phone_number) VALUES (%s, %s)", (client_id, phone_number))
        else:
            updates.append((key, value))
    if updates:
        set_values = ', '.join([col + ' = %s' for col, _ in updates])
        update_values = [values for values in updates]
        update_values.append(client_id)
        cur.execute('UPDATE clients SET {} WHERE id = %s'.format(set_values), update_values)
    conn.commit()
    cur.close()


# Функция для удаления телефона для существующего клиента
def delete_phone(client_id):
    cur = conn.cursor()
    cur.execute("""
    UPDATE clients 
    SET phone = NULL 
    WHERE id = %s""", (client_id,))
    conn.commit()
    cur.close()


# Функция для удаления существующего клиента
def delete_client(client_id):
    cur = conn.cursor()
    # Проверка наличия привязанных номеров
    cur.execute("SELECT COUNT(*) FROM phones WHERE client_id = %s", (client_id,))
    num_phones = cur.fetchone()[0]
    # Если у клиента нет привязанных номеров телефонов, можно удалить его
    if num_phones == 0:
        cur.execute("DELETE FROM clients WHERE id = %s", (client_id,))
        conn.commit()
        print("Клиент успешно удален")
    else:
        print("Нельзя удалить клиента, у которого есть привязанные номера телефонов")
    cur.close()


# Функция для поиска клиента по любой комбинации параметров
def search_client(**kwargs):
    cur = conn.cursor()
    query = "SELECT DISTINCT c.* FROM clients c LEFT JOIN phones p ON c.id = p.client_id WHERE "
    params = []
    for key, value in kwargs.items():
        if key == "phone_number":
            query += "p.phone_number = %s "
        else:
            query += f"c.{key} = %s "
        params.append(value)
    cur.execute(query, params)
    result = cur.fetchall()
    return result


if __name__ == '__main__':
    create_db_structure()
    # add_client('Данила', 'Иванов', 'ema1iee31l12153@ya.ru')
    # add_phone(15, '12443-456-7890')
    # update_client(3, phone_numbers=['123-456-7890', '234-567-8901'])
    print(search_client(phone_number='12443-456-7890'))
