# -*- coding: utf-8 -*-

from linepy import *
from datetime import datetime
import codecs, json, time, timeit
cl = LINE()
oepoll = OEPoll(cl)
settingsOpen = codecs.open("temp.json","r","utf-8")
settings = json.load(settingsOpen)
clMID = cl.profile.mid
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']
msg_dict = {}
bl = [""]
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def helpmessage():
    helpMessage = """
╔═══════════
╠♥ ✿ 楓糖指令表 ✿ ♥
╠➥ 「Speed」查看機器速度
╠➥ 「Set」查看設定
╠➥ 「Reread On/Off」查看收回 打開/關閉
╚═〘 創作者 By: ©楓糖™  〙
"""
    return helpMessage
admin=['uec6d62c3e4a61f033332bc1d86133e49',clMID]
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in admin:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to, "uec6d62c3e4a61f033332bc1d86133e49")
                elif text.lower() == 'speed':
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    start = time.time()
                    cl.sendMessage(to,'處理速度\n' + str1 + '秒')
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,'指令反應\n' + format(str(elapsed_time)) + '秒')
                elif text.lower() == 'set':
                    ret_ = "╔══[ 設定 ]"
                    if settings["reread"] == True: ret_ += "\n╠ 查詢收回開啟 ✅"
                    else: ret_ += "\n╠ 查詢收回關閉 ❌"
                    ret_ += "\n╚══[ 設定 ]"
                    cl.sendMessage(to, str(ret_))
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to, "查詢收回開啟")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to, "查詢收回關閉")
        if op.type == 26:
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 2:
                        if msg.toType == 0:
                            cl.log("[%s]"%(msg._from)+msg.text)
                        else:
                            cl.log("[%s]"%(msg.to)+msg.text)
                        if msg.contentType == 0:
                            msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print(e)
    except Exception as error:
        logError(error)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
