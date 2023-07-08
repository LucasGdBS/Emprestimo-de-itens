from datetime import datetime

class Log:
    def __init__(self):
        self.file_name = 'log.txt'
        if not self.file_exists():
            self.create_file()
        
    
    def file_exists(self):
        try:
            file = open(self.file_name, 'r')
            file.close()
        except FileNotFoundError:
            return False
        else:
            return True
    
    def create_file(self):
        try:
            with open(self.file_name, 'w') as file:
                file.write('Log de emprestimos GARAGino\n')
        except Exception as erro:
            return erro
        else:
            return True
    
    def write_row(self, nome, email, item, estado):
        data = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        if estado:
            row = f'[{data}] {nome} com email {email} emprestou um {item}\n'
        else:
            row = f'[{data}] {nome} com email {email} devolveu um {item}\n'
        with open(self.file_name, 'a') as file:
            file.write(row)

log = Log()

