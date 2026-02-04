import re
from typing import Optional

_SEMESTER_RE = re.compile(r"\bsemester\s*(\d+)\b", re.IGNORECASE)


def infer_doc_type(q: str) -> Optional[str]:
    ql = (q or "").lower()
    if any(k in ql for k in ["jadwal", "jam", "hari", "ruang", "kelas"]):
        return "schedule"
    if any(k in ql for k in ["transkrip", "nilai", "grade", "bobot", "ipk", "ips"]):
        return "transcript"
    if "krs" in ql:
        return "schedule"
    return None
