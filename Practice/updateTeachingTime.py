# -*- coding:utf8 -*-

import requests
import json
import pymongo

def updateTeachingTime(teacherId,blockId):
    base_url = 'https://uat-svc.51uuabc.com/api/graphql'
    headers = {
        "authorization": "Bearer h05bPDXRUYaAuw5U1QSkwvdaq0sUmUqqPV63in2yOVI8YIirtbY2UJO_RKgTcRzys_lHUYtbKO_ILMV6YP67VQ",
        "content-type": "application/json",
        "Origin": "https://uat-teacher.51uuabc.com",
        "Referer": "https://uat-teacher.51uuabc.com/admin/teacher/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }

    s = requests.session()
    updateTeachingTime = "{\"operationName\":\"updateWorkingTimeEffectiveDateRangeForBlock\",\"variables\":{\"input\":{\"blockId\":\"\",\"teacherId\":\"\",\"effectiveStartTime\":1561910400000,\"effectiveEndTime\":1577807999000}},\"query\":\"mutation updateWorkingTimeEffectiveDateRangeForBlock($input: UpdateWorkingTimeEffectiveDateRangeForBlockInput!) {\\n  updateWorkingTimeEffectiveDateRangeForBlock(input: $input) {\\n    code\\n    msg\\n    resultCode\\n    successData {\\n      blockId\\n      weekday\\n      startTime\\n      endTime\\n      reason\\n      __typename\\n    }\\n    failedData {\\n      blockId\\n      reason\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"
    dic_updateTeachingTime = json.loads(updateTeachingTime)
    dic_updateTeachingTime["variables"]["input"]["blockId"] = blockId
    dic_updateTeachingTime["variables"]["input"]["teacherId"] = teacherId
    updateTeachingTime = json.dumps(dic_updateTeachingTime)
    updateTeachingTime_result = s.post(base_url,data=updateTeachingTime,headers=headers)
    print(updateTeachingTime_result.text)



if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://10.68.100.54:27017/")
    db = client["recruit"]
    col_time = db["workingtimeagreements"]


    for i in range(30298,30343):
        teacherId = str(i)

        blockId = col_time.find_one({"teacherId":teacherId})["blockId"]

        updateTeachingTime(teacherId,blockId)
    client.close()