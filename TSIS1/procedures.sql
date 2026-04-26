-- Удаление старых версий функций и процедур
DROP FUNCTION IF EXISTS get_contacts_paginated(INTEGER, INTEGER);
DROP FUNCTION IF EXISTS search_contacts(TEXT);
DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS delete_contact_by_value(VARCHAR);  -- Удаляем старую версию процедуры

-- Процедура для добавления нового телефона
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Находим контакт по имени
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    -- Если контакт не найден
    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    -- Вставляем новый номер в таблицу phones
    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

-- Процедура для перемещения контакта в другую группу
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    -- Добавляем группу, если её нет в базе данных
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    -- Получаем id группы
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    -- Обновляем группу контакта
    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;
END;
$$;

-- Функция для поиска контактов по шаблону (по имени, email, телефону, группе)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Выполняем поиск по имени, email, телефону и группе
    RETURN QUERY
    SELECT
        c.name,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
       OR g.name ILIKE '%' || p_query || '%'
    ORDER BY c.name;
END;
$$;

-- Функция для пагинации контактов (LIMIT и OFFSET)
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Выполняем запрос с пагинацией
    RETURN QUERY
    SELECT
        c.name,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    ORDER BY c.name
    LIMIT p_limit OFFSET p_offset;
END;
$$;

-- Процедура для удаления контакта по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact_by_value(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Удаляем контакт по имени или телефону из таблицы contacts и phones
    DELETE FROM contacts
    WHERE name = p_value
       OR id IN (
           SELECT contact_id
           FROM phones
           WHERE phone = p_value
       );
END;
$$;