


class Word:
    next_id = 0
    def __init__(self, text, status=0, id=None):
        self.text = text
        self.status = status
        if id:
            self.id = id
        else:
            self.id = Word.next_id
            Word.next_id += 1



    
