import sqlite3

class DB:
    def connect(self):
        self.con = sqlite3.connect('mysql.db')
        self.cur = self.con.cursor()


    def create_table(self):
        try:
            self.cur.execute(f'''
                             create table if not exists Estoque (
                             item text primary key,
                             qnt_total integer,
                             qnt_estoque integer,
                             qnt_emprestados integer,
                             qnt_quebrados integer
                             )
                             ''')
        except Exception as erro:
            return {'Erro': erro}
        else:
            return {'Sucesso':'OK'}
    

    def insert_item(self, item:tuple):
        try:
            self.cur.execute(
                '''insert into Estoque values (?, ?, ?, ?, ?)''', item
                )
        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso':'OK'}
    

    def insert_items(self, items):
        try:
            self.cur.executemany(
                '''insert into Estoque values (?, ?, ?, ?, ?)''', items
            )
        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso':'OK'}


    def consulting_item_by_name(self, name):
        return self.cur.execute(
            '''select * from Estoque where item=?''', (name,)
        ).fetchone()
    
    def emprestar(self, name):
        try:
            self.cur.execute(
                '''update Estoque set
                qnt_estoque = qnt_estoque - 1, 
                qnt_emprestados = qnt_emprestados + 1 
                where item=?''', (name,)
            )
            item = self.consulting_item_by_name(name)
            if item[1] < abs(item[2]) + abs(item[3]) + abs(item[4]):
                self.con.rollback()
                return {'Erro': 'No find itens'}
        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso':'OK'}
    
    def devolver(self, name):
        try:
            self.cur.execute(
                '''update Estoque set
                qnt_estoque = qnt_estoque + 1, 
                qnt_emprestados = qnt_emprestados - 1 
                where item=?''', (name,)
            )
            item = self.consulting_item_by_name(name)
            if item[1] < abs(item[2]) + abs(item[3]) + abs(item[4]):
                self.con.rollback()
                return {'Erro': 'No find itens'}
        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso':'OK'}
    

    def delete_item(self, name):
        try:
            self.cur.execute(
                '''delete from Estoque where item=?''', (name,)
            )
        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso':'OK'}
    
    def get_items(self):
        return self.cur.execute(
            '''select * from Estoque'''
        ).fetchall()
    
    def item_broken(self, name):
        try:
            self.cur.execute(
                '''update Estoque set
                qnt_estoque = qnt_estoque - 1,
                qnt_quebrados = qnt_quebrados + 1
                where item=?''', (name, )
            )
            item = self.consulting_item_by_name(name)
            if item[1] < abs(item[2]) + abs(item[3]) + abs(item[4]):
                self.con.rollback()
                return {'Erro': 'No find itens'}
        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso': 'OK'}
    
    def modify_item(self, item, qnt_total, qnt_estoque, qnt_emprestados, qnt_quebrados):
        try:
            self.cur.execute(
                '''update Estoque set
                qnt_total=?,
                qnt_estoque=?,
                qnt_emprestados=?,
                qnt_quebrados=?
                where item=?''',  (qnt_total, qnt_estoque, qnt_emprestados, qnt_quebrados, item)
            )
        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso': 'OK'}
