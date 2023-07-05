import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('mysql.db')
        self.cur = self.con.cursor()


    def create_table(self):
        try:
            self.cur.execute(f'''
                             create table if not exists Estoque (
                             item text primary key,
                             qnt_total integer,
                             qnt_estoque integer,
                             qnt_emprestados integer
                             )
                             ''')
        except Exception as erro:
            print(f'Failed to create table: {erro}')
        else:
            print(f'Table created successfully!\n')
    

    def insert_item(self, item:tuple):
        try:
            self.cur.execute(
                '''insert into Estoque values (?, ?, ?, ?)''', item
                )
        except Exception as erro:
            print('\nFailed to insert item')
            print(f'Reversing operation (rollbakc): {erro}\n')
            self.con.rollback()
        else:
            self.con.commit()
            print('Successfully added item')
    

    def insert_items(self, items):
        try:
            self.cur.executemany(
                '''insert into Estoque values (?, ?, ?, ?)''', items
            )
        except Exception as erro:
            print('\nFailed to insert item')
            print(f'Reversing operation (rollbakc): {erro}\n')
            self.con.rollback()
        else:
            self.con.commit()
            print('Successfully added item')


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
        except Exception as erro:
            print('Failed to change item\n')
            print(f'Reversing operation (rollbakc): {erro}\n')
            self.con.rollback()
        else:
            self.con.commit()
            print('Successfully change item\n')
    

    def delete_item(self, name):
        try:
            self.cur.execute(
                '''delete from Estoque where item=?''', (name,)
            )
        except Exception as erro:
            print('Failed to delete item\n')
            print(f'Reversing operation (rollbakc): {erro}\n')
            self.con.rollback()
        else:
            self.con.commit()
            print('Successfully delete item\n')
    
    
    

banco = DB()
# banco.create_table()
# banco.insert_items(('arduino', 10, 10, 0))
# banco.emprestar('arduino')
# print(banco.consulting_item_by_name('arduino'))
# banco.delete_item('arduino')
# banco.con.close()