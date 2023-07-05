from db import DB
from fastapi import FastAPI

'''
Para excutar a API localmente execute:
uvicorn app:app --reload

E se for a primeira vez executando não esqueça de cirar o DB
estoque.create_table()
'''


estoque = DB()
app = FastAPI()

# estoque.create_table()

@app.get('/')
def teste():
    return {'codigo': 200}

@app.get('/estoque/get-item')
def get_items():
    try:
        estoque.connect()
        items = estoque.get_items()
        estoque.con.close()
    except:
         return {'Erro':'nenhum item encontrado'}
    else:
        return [{'item':row[0],'qnt_total':row[1],'qnt_estoque':row[2],'qnt_empretados':row[3]} for row in items]
    
@app.get('/estoque/get-item/{nome_item}')
def get_item(nome_item: str):
    try:
        estoque.connect()
        item = estoque.consulting_item_by_name(nome_item)
        estoque.con.close()
        dic = {
            'Item':item[0], 
            'qnt_total':item[1], 
            'qnt_estoque':item[2], 
            'qnt_emprestados':item[3]
            }
        return dic
    except:
        return {'Erro':'item não encontrado'}


@app.post('/estoque/post-item')
def insert_item(nome_item:str, qnt_total:int, qnt_estoque:int, qnt_emprestados:int):
    try:
        estoque.connect()
        estoque.insert_item((nome_item, qnt_total, qnt_estoque, qnt_emprestados))
        estoque.con.close()
    except:
        return {'Erro':'nao foi possivel realizar'}
    else:
        return get_item(nome_item)


@app.put('/estoque/emprestar')
def emprestar_item(nome_item:str):
    try:
        estoque.connect()
        estoque.emprestar(nome_item)
        estoque.con.close()
    except:
        return {'Erro':'nao foi possivel realizar'}
    else:
        return get_item(nome_item)


@app.put('/estoque/devolver')
def devolver_item(nome_item:str):
    try:
        estoque.connect()
        estoque.devolver(nome_item)
        estoque.con.close()
    except:
        return {'Erro':'nao foi possivel realizar'}
    else:
        return get_item(nome_item)
