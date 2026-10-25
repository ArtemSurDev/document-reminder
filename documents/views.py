import sqlite3
from django.shortcuts import render

DB_PATH = "data/document_reminder.sqlite"


def document_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    documents = conn.execute("""
                             SELECT documents.id,
                                    documents.title,
                                    documents.number,
                                    documents.expiry,
                                    users.name AS owner_name
                             FROM documents
                                      JOIN users ON documents.owner_id = users.id
                             ORDER BY documents.expiry
                             """).fetchall()
    conn.close()

    return render(request, "documents/document_list.html", {"documents": documents})


def document_detail(request, document_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    document = conn.execute("""
                            SELECT documents.id,
                                   documents.title,
                                   documents.number,
                                   documents.expiry,
                                   users.name AS owner_name
                            FROM documents
                                     JOIN users ON documents.owner_id = users.id
                            WHERE documents.id = ?
                            """, (document_id,)).fetchone()
    conn.close()

    return render(
        request,
        "documents/document_detail.html",
        {"document": document},
        status=404 if document is None else 200,
    )


def available_documents(request):
    search_date = request.GET.get("date")
    documents = []

    if search_date:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        documents = conn.execute("""
                                 SELECT id, title, expiry
                                 FROM documents
                                 WHERE expiry >= ?
                                 ORDER BY expiry
                                 """, (search_date,)).fetchall()
        conn.close()

    return render(
        request,
        "documents/available.html",
        {"documents": documents, "search_date": search_date}
    )
