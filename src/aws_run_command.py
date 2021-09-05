#!/usr/bin/env python
import boto3
import time
import sys
from logging import getLogger, StreamHandler, DEBUG, Formatter
from datetime import datetime

args = sys.argv
command = "cat /etc/hosts"
instance_id = args[1]
ssm = boto3.client('ssm')

##Command投入

r = ssm.send_command(
        InstanceIds = [instance_id],
        DocumentName = "AWS-RunShellScript",
        Parameters = {
            "commands": [
            command
            ]    
        }
    )
command_id = r['Command']['CommandId']

## 処理終了待ち
time.sleep(5)

res = ssm.list_command_invocations(
          CommandId = command_id,
          Details = True
      )
invocations = res['CommandInvocations']
status = invocations[0]['Status']

if status == "Failed":
    print("Command実行エラー")

## 結果格納

account = invocations[0]['CommandPlugins'][0]['Output']
print(account)