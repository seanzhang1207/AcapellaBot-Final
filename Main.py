import asyncio
import datetime
import random
import websockets
import json
import time
import socket

from RoadShowController import RoadShowController

roadShow = None


async def server(websocket, path):
    global roadShow
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        if data['type'] == "cmd":
            print("Received {} command.".format(data['cmd']))

            if data['cmd'] == "set-mode":
                mode = data['value']
                print(mode)
                if mode == 'interaction':
                    print(roadShow)
                    if roadShow == None:
                        roadShow = RoadShowController()
                        roadShow.start()
                    else:
                        roadShow.terminate()
                        roadShow.join()
                        roadShow = None
                else:
                    roadShow.terminate()
                    roadShow.join()
                    roadShow = None
            elif data['cmd'] == 'start-roadshow':
                if roadShow != None:
                    roadShow.interactionStage = 1
                else:
                    roadShow = RoadShowController()
                    roadShow.start()
            elif data['cmd'] == 'fake-recog':
                if roadShow != None:
                    roadShow.fakeSpeechRecogSignal.set()

            elif data['cmd'] == 'jump-stage-1':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 1
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-2':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 2
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-3':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 3
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-4':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 4
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-5':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 5
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-6':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 6
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-7':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 7
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-8':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 8
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'jump-stage-9':
                if roadShow != None:
                    roadShow.pause()
                    roadShow.interactionStage = 9
                    roadShow.waitingTime = 0
                    roadShow.waitingStartTime = 0
                    roadShow.waitingSignal = None
                    if roadShow.singAlong != None:
                        roadShow.singAlong.terminate()
                        roadShow.singAlong.join()
                    if roadShow.learnSong != None:
                        roadShow.learnSong.terminate()
                        roadShow.learnSong.join()
                    roadShow.resume()

            elif data['cmd'] == 'set-stage-1':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage1.set()
                    else:
                        roadShow.doStage1.clear()

            elif data['cmd'] == 'set-stage-2':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage2.set()
                    else:
                        roadShow.doStage2.clear()

            elif data['cmd'] == 'set-stage-3':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage3.set()
                    else:
                        roadShow.doStage3.clear()

            elif data['cmd'] == 'set-stage-4':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage4.set()
                    else:
                        roadShow.doStage4.clear()

            elif data['cmd'] == 'set-stage-5':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage5.set()
                    else:
                        roadShow.doStage5.clear()

            elif data['cmd'] == 'set-stage-6':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage6.set()
                    else:
                        roadShow.doStage6.clear()

            elif data['cmd'] == 'set-stage-7':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage7.set()
                    else:
                        roadShow.doStage7.clear()

            elif data['cmd'] == 'set-stage-8':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage8.set()
                    else:
                        roadShow.doStage8.clear()

            elif data['cmd'] == 'set-stage-9':
                print(data['value'])
                if roadShow != None:
                    if data['value'] == "on":
                        roadShow.doStage9.set()
                    else:
                        roadShow.doStage9.clear()


start_server = websockets.serve(server, '0.0.0.0', 8091)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
