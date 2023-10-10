MAPPINGS = {
    "properties": {
        "title": {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        "description": {
            "type": "text"
        },
        "created_at": {
            "type": "date",
            "format": "yyyy-MM-dd HH:mm"
        }
    }
}
