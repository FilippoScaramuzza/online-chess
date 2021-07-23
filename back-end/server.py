from aiohttp import web
import aiohttp_cors
import socketio
import random
import os
import json

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)
cors = aiohttp_cors.setup(app)

for resource in app.router._resources:
    if resource.raw_match("/socket.io/"):
        continue
    cors.add(resource, { '*': aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*") })

games = []
rooms = []
tot_client = 0

@sio.event
def connect(sid, environ):
    global tot_client

    tot_client += 1
    log()

@sio.event
async def create(sid, data):
    game_id = ''.join(random.choice(
        '0123456789abcdefghijklmnopqrstuvwxyz') for i in range(4))
    games.append({
        'id': game_id,
        'players': [data['username']],
        'pgn': '',
        'status': 'starting'
    })

    sio.enter_room(sid, game_id)
    rooms.append({'id': game_id, 'sids': [sid]})
    await sio.emit('created', {'game': games[len(games)-1]})

    log()


@sio.event
async def fetch(sid, data):
    for game in games:
        if game['id'] == data['id']:
            for room in rooms:
                if room['id'] == data['id']:
                    if len(room['sids']) < 2 and room['sids'][0] != sid:
                        room['sids'].append(sid)
                        sio.enter_room(sid, data['id'])
            await sio.emit('fetch', {'game': game}, room=data['id'])

    log()

@sio.event
async def join(sid, data):
    gamefound = False
    username_already_in_use = False
    for game in games:
        if game['id'] == data['id']:
            if game['players'][0] == data['username']:
                username_already_in_use = True
            else:
                game['players'].append(data['username'])
                game['status'] = 'ongoing'
                sio.enter_room(sid, data['id'])
                for room in rooms:
                    if room['id'] == data['id']:
                        room['sids'].append(sid)

                await sio.emit('joined', {'game': game})
                gamefound = True

    if not gamefound:
        await sio.emit('gamenotfound')

    if username_already_in_use:
        await sio.emit('usernamealreadyinuse')

    log()

@sio.event
async def move(sid, data):  # id, from, to, pgn

    for game in games:
        if game['id'] == data['id']:
            game['pgn'] = data['pgn']
            await sio.emit('moved', {'from': data['from'],'to': data['to'] }, room = data['id'], skip_sid=sid)
            await sio.emit('fetch', {'game': game}, room = data['id'])

    log()

@sio.event
async def resign(sid, data):
    await sio.emit('resigned', room=data['id'], skip_sid=sid)
    index = -1
    for game in games:
        if game['id'] == data['id']:
            index = games.index(game)

    if index > -1:
        games.pop(index)
    
    log()

@sio.event
async def checkmate(sid, data):
    await sio.emit('checkmate', room=data['id'], skip_sid=sid)
    index = -1
    for game in games:
        if game['id'] == data['id']:
            index = games.index(game)

    if index > -1:
        games.pop(index)
    
    log()

@sio.event
async def disconnect(sid):
    global tot_client

    print('disconnect', sid)
    tot_client -= 1
    for room in rooms:
        if sid in room['sids']:
            await sio.emit('disconnected', room=room['id'])
            room['sids'].remove(sid)

    log()

def log():
    os.system('cls||clear')

    print(f'Users connected: {tot_client}')

    print(f'GAMES: ')

    print(json.dumps(games, indent=2))

if __name__ == '__main__':
    log()
    port = int(os.environ.get('PORT', 8000))
    web.run_app(app, port = port)
