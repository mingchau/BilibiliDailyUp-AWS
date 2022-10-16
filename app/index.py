from bilibili import Bilibili


def lambda_handler(event, context):
    bilibili = Bilibili()
    bilibili.go()
