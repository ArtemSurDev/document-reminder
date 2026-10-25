SELECT id, title, number, expiry FROM documents ORDER BY expiry;

SELECT id, name, email FROM users ORDER BY name;

SELECT id, title, expiry FROM documents WHERE expiry <= '2026-12-31';

SELECT id, title FROM documents WHERE title LIKE '%паспорт%';

SELECT documents.title, documents.expiry, users.name AS owner_name
FROM documents
JOIN users ON documents.owner_id = users.id;

SELECT notifications.message, notifications.created, users.name AS user_name, documents.title AS doc_title
FROM notifications
JOIN users ON notifications.user_id = users.id
JOIN documents ON notifications.document_id = documents.id;

SELECT COUNT(*) AS total_documents FROM documents;

SELECT COUNT(*) AS total_notifications FROM notifications;

SELECT users.name, COUNT(documents.id) AS doc_count
FROM users
LEFT JOIN documents ON users.id = documents.owner_id
GROUP BY users.id, users.name;

SELECT users.name, COUNT(documents.id) AS doc_count
FROM users
JOIN documents ON users.id = documents.owner_id
GROUP BY users.id, users.name
HAVING COUNT(documents.id) > 1;