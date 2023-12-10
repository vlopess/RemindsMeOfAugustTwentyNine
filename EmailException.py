class EmailException(Exception):
    def __str__(self):
        return 'Email já cadastrado!'