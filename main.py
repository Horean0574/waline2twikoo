import json
import uuid
import hashlib
import click
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
from markdown import markdown

cidMap = { }
uidMap = { }
res = []


def step_start(prompt):
    click.echo(prompt, nl=False)


def step_complete(another_newline=False):
    if another_newline:
        click.echo("  完成✅\n")
    else:
        click.echo("  完成✅")


def new_uuid():
    return str(uuid.uuid4()).replace("-", "")


def md5_encrypt(data):
    md5 = hashlib.md5()
    md5.update(data.encode("UTF-8"))
    return md5.hexdigest()


def iso2unix(iso):
    dt = datetime.fromisoformat(iso)
    return int(dt.timestamp() * 1000)


def get_converted(item, site_domain, master_mail):
    url = quote(item["url"])
    return {
        "nick": item["nick"],
        "mail": item["mail"],
        "link": item["link"],
        "ua": item["ua"],
        "ip": item["ip"],
        "url": url,
        "comment": markdown(item["comment"].replace("\n", "\n\n")),
        "pid": cidMap[item["pid"]] if "pid" in item else None,
        "rid": cidMap[item["rid"]] if "rid" in item else None,
        "_id": cidMap[item["objectId"]],
        "uid": uidMap[item["mail"]],
        "mailMd5": md5_encrypt(item["mail"]),
        "master": bool(item["mail"] == master_mail),
        "href": "https://" + site_domain + url,
        "isSpam": bool(item["status"] != "approved"),
        "created": iso2unix(item["insertedAt"]),
        "updated": iso2unix(item["updatedAt"]),
        "top": bool(item["sticky"] > 0) if "sticky" in item else False,
    }


def read_waline(read_file):
    step_start("读取 Waline 评论数据中……")
    with open(read_file, "r", encoding="UTF-8") as f:
        waline = json.load(f)["data"]["Comment"]
    total = len(waline)
    cnt = 0
    step_complete()
    return waline, total, cnt


def establish_map(waline):
    step_start("映射建立中……")
    for item in waline:
        cidMap[item["objectId"]] = new_uuid()
        if item["mail"] not in uidMap:
            uidMap[item["mail"]] = new_uuid()
    step_complete(True)


def convert_all(site_domain, master_mail, waline, total, cnt):
    for item in waline:
        cnt += 1
        step_start(f"{cnt}/{total}: 正在转换来自 [{item["nick"]}] 的评论……")
        res.append(get_converted(item, site_domain, master_mail))
        step_complete()


def write_twikoo(write_file):
    step_start("\n写入文件中……")
    output_path = Path(write_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(write_file, "w", encoding="UTF-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    step_complete()


def main(site_domain, master_mail, master_uid, read_file, write_file):
    global uidMap
    if master_uid != "":
        uidMap = { master_mail: master_uid }
    waline, total, cnt = read_waline(read_file)
    establish_map(waline)
    convert_all(site_domain, master_mail, waline, total, cnt)
    write_twikoo(write_file)


def interactive_input():
    site_domain = click.prompt("你的站点域名")
    bcf = click.prompt("你（博主）有在新的Twikoo评论系统上评论过吗？(y/N)", type=bool, default=False, show_default=False)
    if bcf:
        master_mail = click.prompt("你的电子邮件")
        master_uid = click.prompt("你的 Twikoo UID（可在导出 Twikoo 评论数据后看到）")
    else:
        master_mail = master_uid = ""
    read_file = click.prompt("原 Waline 评论数据文件路径（相对路径，JSON文件）")
    write_file = click.prompt("新的 Twikoo 评论数据文件存储路径（相对路径，JSON文件）")
    click.echo()
    main(site_domain, master_mail, master_uid, read_file, write_file)


if __name__ == '__main__':
    click.echo("Program started.\n")
    interactive_input()
    click.echo("\nProgram ended.")
