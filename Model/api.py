class Payload:
    def __init__(self, action, tag_0, tag_contains_0, tagtype_0, page_size,
                 json):

        self.action = action
        self.tag_0 = tag_0
        self.tag_contains_0 = tag_contains_0
        self.tagtype_0 = tagtype_0
        self.page_size = page_size
        self.json = json

    def get_payload_formatted(self):
        payload = {
            "action": self.action,
            "tag_0": self.tag_0,
            "tag_contains_0": self.tag_contains_0,
            "tagtype_0": self.tagtype_0,
            "page_size": self.page_size,
            "json": self.json
        }
        return payload