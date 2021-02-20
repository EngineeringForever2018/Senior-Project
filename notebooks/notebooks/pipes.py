from pdpipe import PdPipelineStage


class SplitText(PdPipelineStage):
    def __init__(self, nlp, show_loading=False):
        desc = 'A pipeline that will split texts from a dataframe into sentences.'
        super().__init__(desc=desc)
        self.nlp = nlp
        self.show_loading = show_loading

    def _prec(self, df): # noqa
        return 'text' in df.columns

    def _transform(self, df, verbose):
        pass
