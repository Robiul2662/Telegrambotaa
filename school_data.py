"""Add only verified school information from public/authorized sources."""
SCHOOLS = [
    # Example structure; replace with verified records:
    # {
    #   "name": "Verified school name",
    #   "eiin": "123456",
    #   "school_type": "Government secondary school",
    #   "district": "District",
    #   "upazila": "Upazila",
    #   "source_url": "https://official-source.example",
    #   "staff": [
    #       {"name": "Publicly listed name", "designation": "Assistant Teacher",
    #        "subject": "Bangla", "source_url": "https://official-source.example"}
    #   ]
    # }
]

def search_schools_by_eiin(eiin):
    return [s for s in SCHOOLS if str(s.get("eiin", "")) == str(eiin)]

def search_schools_by_text(query):
    q = query.casefold()
    fields = ("name", "eiin", "district", "upazila", "school_type")
    return [
        s for s in SCHOOLS
        if any(q in str(s.get(field, "")).casefold() for field in fields)
    ]
