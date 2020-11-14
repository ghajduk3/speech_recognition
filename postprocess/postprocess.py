
class Postprocess:

    @staticmethod
    def add_punctuation(text):

        replacements = {'konec':'.','vrstica':"\n"}
        return ' '.join([replacements[word] if word in replacements.keys() else word for word in text.split(" ")])