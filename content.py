class Content:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.text = ""

    def add_text(self, text):
        """
        Update the text of this Content.
        """
        self.text = text