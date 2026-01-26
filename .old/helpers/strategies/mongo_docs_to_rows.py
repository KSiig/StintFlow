from datetime import timedelta

def mongo_docs_to_rows(docs):
    rows = []

    for doc in docs:
        row = [
            doc.get("stint_type"),
            doc.get("name"),
            "Completed ✅" if doc.get("status") else "Pending ⏳",
            doc.get("pit_end_time"),
            int(doc.get("tires_changed", 0)),
            int(doc.get("tires_left", 0)),
            timedelta(seconds=int(doc.get("stint_time_seconds", 0))),
        ]
        rows.append(row)

    return rows