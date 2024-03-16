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
        email TEXT UNIQUE,
        phone TEXT UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        client_id INT REFERENCES clients(id),
        phone_number TEXT
    );
    """)
    conn.commit()
    cur.close()


# Функция для добавления нового клиента в базу данных
def add_client(first_name, last_name, email=None, phone=None):
    cur = conn.cursor()
    cur.execute(f"""
    INSERT INTO clients (first_name, last_name, email, phone)
    VALUES (%s, %s, %s, %s)""", (first_name, last_name, email, phone))
    conn.commit()
    cur.close()


# Функция для добавления телефона для существующего клиента
def add_phone(client_id, phone_number):
    cur = conn.cursor()
    cur.execute("""UPDATE clients SET phone = %s WHERE id = %s""", (phone_number, client_id))
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
        set_values = ', '.join([f'{col} = %s' for col, _ in updates])
        update_values = [values for values in updates]
        update_values.append(client_id)
        cur.execute(f'UPDATE clients SET {set_values} WHERE id = %s', update_values)
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
    cur.execute("""DELETE FROM clients WHERE id = %s""", (client_id,))
    conn.commit()
    cur.close()


if __name__ == '__main__':
    create_db_structure()
    # add_client('Данила', 'Иванов', 'ema1i31l12153@ya.ru', '13313234-4536-7890')
    # add_phone(8, '123-456-7890')
    update_client(14, phone_numbers=['123-456-7890', '234-567-8901'])
