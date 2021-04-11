from docx import Document
from notebooks.reconstruction import WordReconstructable

with open('word_document_test.docx', 'rb') as wf:
    document = Document(wf)

word_reconstructable = WordReconstructable(document)

# I believe that the sentences listed below will reconstruct the document accurately.
# @Hayden if you run into issues with the tabs not showing in the resulting document or
# if the tabs are highlighted then that's probably not your fault and you don't need to
# change WordReconstructable to accomodate.
annotated_paragraphs = [
    [
        ('\tThis is a sentence. ', False),
        ('This paragraph started with a tab. ', True),
        ('All sentences with more than five words should be highlighted. ', True),
        ('This has four words.', False)
    ],
    [
        ('This is another sentence. ', False),
        ('This paragraph did not start with a tab. ', True),
        ('How many words are in this question? ', True),
        ('There are five.', False)
    ]
]

print(word_reconstructable.paragraphs)

annotated_paragraphs = dict(zip(word_reconstructable.keys, annotated_paragraphs))

word_reconstructable.highlight(annotated_paragraphs)

word_reconstructable.document.save('result_document.docx')
