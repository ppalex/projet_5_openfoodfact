
import Configuration.config as config

config.load('./configuration/config.yml')


class Payload:
    def __init__(self, action, tag_0, tag_contains_0, tagtype_0, page_size,
                 json):
        """Constructor of the class Payload.

        Arguments:
            action {String} -- Type of request.
            tag_0 {String} -- Value to get from API.
            tag_contains_0 {String} -- 'Contains' or 'not contains' µ
                                            information.
            tagtype_0 {String} -- Criteria.
            page_size {int} -- Number of result to be return.
            json {bool} -- True to return the data in JSON.
        """
        self.action = action
        self.tag_0 = tag_0
        self.tag_contains_0 = tag_contains_0
        self.tagtype_0 = tagtype_0
        self.page_size = page_size
        self.json = json

    def get_payload_formatted(self):
        """This method return an dictionnary representing a payload.

        Returns:
            [dict] -- Dict representing the payload for the API.
        """
        payload = {
            "action": self.action,
            "tag_0": self.tag_0,
            "tag_contains_0": self.tag_contains_0,
            "tagtype_0": self.tagtype_0,
            "page_size": self.page_size,
            "json": self.json
        }
        return payload
