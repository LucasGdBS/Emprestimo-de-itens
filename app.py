'''Api que da acesso ao banco de dados onde se encontrarm os itens para
emprestimo'''
from db import DB
from log import log
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
    ''''Teste inicial. Se retornar 200 você está conectado'''
    return {'codigo': 200}

@app.get('/estoque')
def get_items():
    '''Retorna todos os itens'''
    try:
        estoque.connect()
        items = estoque.get_items()
        estoque.con.close()
    except:
         return {'Erro':'nenhum item encontrado'}
    else:
        return [{'item':row[0],'qnt_total':row[1],'qnt_estoque':row[2],'qnt_emprestados':row[3], 'qnt_quebrados':row[4]} for row in items]
    
@app.get('/estoque/get-item')
def get_item(nome_item: str):
    '''Retorna o item especificado'''
    try:
        estoque.connect()
        item = estoque.consulting_item_by_name(nome_item)
        estoque.con.close()
        dic = {
            'Item':item[0], 
            'qnt_total':item[1], 
            'qnt_estoque':item[2], 
            'qnt_emprestados':item[3],
            'qnt_quebrados':item[4]
            }
        return dic
    except:
        return {'Erro':'item não encontrado'}


@app.post('/estoque/post-item')
def insert_item(nome_item:str, qnt_total:int, qnt_estoque:int, qnt_emprestados:int):
    '''Adiciona um novo item ao banco'''
    try:
        estoque.connect()
        estoque.insert_item((nome_item, qnt_total, qnt_estoque, qnt_emprestados))
        estoque.con.close()
    except:
        return {'Erro':'nao foi possivel realizar'}
    else:
        return get_item(nome_item)


@app.put('/estoque/emprestar')
def emprestar_item(nome_item:str, user:str, email:str):
    '''Empresta um item, diminuindo a quantidade de itens em estoque e aumentando
    os itens emprestados'''
    
    estoque.connect()
    emprestimo = estoque.emprestar(nome_item, user, email)
    estoque.con.close()
    
    if 'Erro' not in emprestimo :
        log.write_row(user, email, nome_item, True)
        return get_item(nome_item)
    else:
        return emprestimo


@app.put('/estoque/devolver')
def devolver_item(nome_item:str, user:str, email:str):
    '''Devolve um item emprestado, diminutindo os itens emprestaodos e aumentando
    os itens em estoque'''
    
    estoque.connect()
    devolucao = estoque.devolver(nome_item, user, email)
    estoque.con.close()

    if 'Erro' not in devolucao:
        log.write_row(user, email, nome_item, False)
        return get_item(nome_item)
    else:
        return devolucao

@app.put('/estoque/modify')
def modify_item(nome_item:str, qnt_total:int, qnt_estoque:int, qnt_emprestados:int, qnt_quebrados:int):
    '''Modifica as quantidade de um item por completo'''

    estoque.connect()
    modify = estoque.modify_item(nome_item, qnt_total, qnt_estoque, qnt_emprestados, qnt_quebrados)
    estoque.con.close()

    if 'Erro' not in modify:
        return get_item(nome_item)
    else: 
        return modify

@app.get('/estoque/get_user')
def get_items_by_user(user:str, email:str):
    '''Visualiza todos os itens que estão emprestados para o usuario informado'''

    estoque.connect()
    items = estoque.get_items_by_user(user, email)
    estoque.con.close()

    if items:
        return items
    else:
        return 'Nenhum item'