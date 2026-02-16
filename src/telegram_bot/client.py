import httpx

class BackendClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def send_text(self, user_external_ref: str, text: str) -> dict:
        r = httpx.post(
            f"{self.base_url}/inbox/text",
            json={"user_external_ref": user_external_ref, "text": text},
            headers={"x-api-key": self.api_key},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()

    def send_file(self, user_external_ref: str, file_bytes: bytes, filename: str, mime: str) -> dict:
        files = {"upload": (filename, file_bytes, mime)}
        data = {"user_external_ref": user_external_ref}
        r = httpx.post(
            f"{self.base_url}/inbox/file",
            data=data,
            files=files,
            headers={"x-api-key": self.api_key},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
    
    def confirm_draft(self, draft_id: int, payload: dict) -> dict:
        r = httpx.post(
            f"{self.base_url}/drafts/{draft_id}/confirm",
            json=payload,
            headers={"x-api-key": self.api_key},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()

