import sqlite3

class DB:
    def connect(self):
        self.con = sqlite3.connect('mysql.db')
        self.cur = self.con.cursor()


    def create_table_estoque(self):
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


    def create_table_user(self):
        try:
            self.cur.execute(f'''
                             create table if not exists User (
                             id integer primary key autoincrement,
                             nome text,
                             email text,
                             item text,
                             situacao boolean check (situacao in (0, 1))
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
    
    def insert_user(self, nome, email, item):
        self.cur.execute(
            '''insert into User (nome, email, item, situacao) values (?, ?, ?, ?)''', (nome, email, item, 1)
        )


    def consulting_item_by_name(self, name):
        return self.cur.execute(
            '''select * from Estoque where item=?''', (name,)
        ).fetchone()
    
    def consulting_user(self, nome, email, item):
        user = self.cur.execute(
            '''select * from User where nome=? and email=? and item=? and situacao=?''',(nome, email, item, 1)
        ).fetchone()

        return user
    
    def emprestar(self, item, nome, email):
        try:
            self.cur.execute(
                '''update Estoque set
                qnt_estoque = qnt_estoque - 1, 
                qnt_emprestados = qnt_emprestados + 1 
                where item=?''', (item,)
            )
            items = self.consulting_item_by_name(item)
            if items[1] < abs(items[2]) + abs(items[3]) + abs(items[4]):
                self.con.rollback()
                return {'Erro': 'No find itens'}
            
            self.insert_user(nome, email, item)
            

        except Exception as erro:
            self.con.rollback()
            return {'Erro': erro}
        else:
            self.con.commit()
            return {'Sucesso':'OK'}
    
    def devolver(self, item, nome, email):
        try:
            self.cur.execute(
                '''update Estoque set
                qnt_estoque = qnt_estoque + 1, 
                qnt_emprestados = qnt_emprestados - 1 
                where item=?''', (item,)
            )
            items = self.consulting_item_by_name(item)
            if items[1] < abs(items[2]) + abs(items[3]) + abs(items[4]):
                self.con.rollback()
                return {'Erro': 'No find itens'}
            
            if self.consulting_user(nome, email, item):
                self.cur.execute(
                    '''update User set
                    situacao = 0
                    where nome = ? and email = ? and item=?''', (nome, email, item)
                )
            else:
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
