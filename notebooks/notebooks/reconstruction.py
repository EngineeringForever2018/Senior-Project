from docx import Document

class WordReconstructable:
    # @Hayden: The only hard requirement I have here is that you take in this word
    # document class from the docx library and act on it. You can change the function
    # signatures for the other methods if you have to, but I'd prefer not if it can be
    # helped, and try to tell me about how you're changing them as soon as possible.
    def __init__(self, document: Document):
        self._document = document

    @property
    def paragraphs(self) -> dict:
        """
        Return the paragraphs within the word document as a dictionary. The keys in the
        dictionary are used to uniquely identify each paragraph so that they can be
        modified and replaced later. The values in the dictionary are the paragraphs as
        strings.
        """
        # @Hayden: When parsing word docs for the backend I used document.paragraphs,
        # and the actual paragraph text could be retrieved with paragraph.text. See
        # https://python-docx.readthedocs.io/en/latest/api/document.html
        # 
        # @Hayden: To generate the keys you could simply get the paragraphs into a list
        # and use the index of each paragraph as its key. The following code would do
        # that.
        # 
        # return dict(enumerate(paragraph_list))
        # 
        # The reason that we return a dictionary instead of a list is because I feel
        # it's less rigid and prone to error, and because it opens the door for only
        # supplying some of the paragraphs to be highlighted instead of all of them.
        return {'dummy-key': 'dummy value', 'dummy-key2': 'dummy value 2'}

    @property
    def keys(self):
        """
        Return the keys that would be used to uniquely identify paragraphs from the
        paragraphs property.
        """
        return ['dummy-key', 'dummy-key2']

    def highlight(self, annotated_paragraphs):
        """
        Highlight sentences in the document based on :param annotated_paragraphs.

        :param annotated_paragraphs: The paragraphs to reconstruct the document with.
        Each paragraph is represented as a list of tuples. The first item in the tuple
        is a sentence within the paragraph and the second item tells whether this
        sentence should be highlighted. annotated_paragraphs should be a dictionary, and
        the keys should match those from the paragraphs property.
        """
        # The docx library seems to work with text runs, which was similar to the libary
        # that Noah and I were looking at for the frontend. See the first example in
        # https://python-docx.readthedocs.io/en/latest/
        pass

    @property
    def document(self):
        return self._document
