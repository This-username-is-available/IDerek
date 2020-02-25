#!/usr/bin/env python
# coding=utf-8

"""
@Author       : Li Baoyan
@Date         : 2020-02-23 11:37:56
@Github       : https://github.com/This-username-is-available
@LastEditTime : 2020-02-25 12:43:59
@LastEditors  : Li Baoyan
@Description  : 
"""


import asyncio
import threading
import time
import tkinter
import tkinter.messagebox
import tkinter.scrolledtext
import urllib.parse

import aiohttp
import bs4


def right_key(event, editor):
    """右键菜单"""

    def cut(editor, event=None):
        editor.event_generate("<<Cut>>")

    def copy(editor, event=None):
        editor.event_generate("<<Copy>>")

    def paste(editor, event=None):
        editor.event_generate("<<Paste>>")

    menubar.delete(0, tkinter.END)
    menubar.add_command(label="剪切", command=lambda: cut(editor))
    menubar.add_command(label="复制", command=lambda: copy(editor))
    menubar.add_command(label="粘贴", command=lambda: paste(editor))
    menubar.post(event.x_root, event.y_root)


def pack_disposable_widget(widget_args):  # 一次性控件打包
    if widget_args[0] == "Label":
        widget = tkinter.Label(
            widget_args[1],
            text=widget_args[2],
            width=widget_args[3],
            height=widget_args[4],
            wraplength=800,
            justify="left",
            font=("微软雅黑", 10),
        )
        widget.pack()
        disposable_widgets.add(widget)
    elif widget_args[0] == "Button":
        widget = tkinter.Button(
            widget_args[1],
            text=widget_args[2],
            width=widget_args[3],
            height=widget_args[4],
            command=widget_args[5],
            font=("微软雅黑", 10),
        )
        widget.pack()
        disposable_widgets.add(widget)
    else:
        raise Exception('"pack_disposable_widget()" does not support this widget.')
    return widget


def change_disposable_widget(interface):  # 一次性控件转场
    for widgets in disposable_widgets:
        widgets.destroy()
    disposable_widgets.clear()
    for widgets in interface:
        pack_disposable_widget(widgets)


def keep_chinese(content):  # 输入文本，返回所有非中文字符变成空格的文本
    contentstr = ""
    for char in content:
        if char >= u"\u4e00" and char <= u"\u9fa5":
            contentstr += char
        else:
            contentstr = contentstr + " "
    return contentstr


def pure_messagebox(text):
    pseudo_root = tkinter.Tk()
    pseudo_root.withdraw()  # 隐藏主窗口，实现只有一个弹窗弹出
    tkinter.messagebox.showinfo("", text)
    pseudo_root.destroy()  # 销毁假的主窗口


def progress_bar(progress, length):
    blank = (
        "|"
        + "█" * int(progress * length)
        + " " * (length - int(progress * length))
        + "|"
    )
    return blank


def input_word_num():

    num = text_box.get("0.0", "end").strip()
    text_box.delete("1.0", "end")

    try:
        word_nums.add(int(num))
        tkinter.messagebox.showinfo("", "输入成功。若有其他字数类型请继续输入。")
    except ValueError:
        if not num:
            tkinter.messagebox.showinfo("", "请在输入框内输入字数类型。")
        else:
            tkinter.messagebox.showwarning("", "请输入纯数字！！")


def to_search_definition():
    if text_box.get("0.0", "end").strip():
        tkinter.messagebox.showwarning("", "输入框内仍有待输入的字数类型，请先点击输入！！")
    elif word_nums:
        change_disposable_widget(INTERFACE2)
        tkinter.messagebox.showinfo("", "请将待查询的成语单OCR（图片转文字）结果置于以上输入框内，不需改格式。")
    else:
        tkinter.messagebox.showwarning("", "未输入字数类型！！")


def search_definition_gui(function):

    global progress, top

    tkinter.messagebox.showinfo("", "查询中，请耐心等待……")
    progress = tkinter.StringVar()
    progress.set(progress_bar(0, 15))

    top = tkinter.Toplevel()
    tkinter.Label(top, text="请勿关闭此窗口。", width=20, height=1).pack()
    tkinter.Label(
        top, textvariable=progress, width=20, height=3, font=("Courier New", 10)
    ).pack()

    all_input_idiom = text_box.get("0.0", "end").replace("█", "").strip()

    Thread_1 = threading.Thread(target=function, args=(all_input_idiom,))
    Thread_1.setDaemon(True)
    Thread_1.start()

    wait_until_complete()


def wait_until_complete():

    global all_output_idiom

    if is_searching:
        root.after(CHECK_INTERVAL * 1000, wait_until_complete)  # 自我调用以实现定时调用效果
    else:
        top.destroy()

        text_box.delete("1.0", "end")
        text_box.insert("1.0", all_output_idiom)

        change_disposable_widget(INTERFACE3)

        if not all_output_idiom:
            tkinter.messagebox.showinfo("", "请将待查询的成语单OCR（图片转文字）结果置于以上输入框内。")
        elif all_output_idiom.find("█") != -1:
            tkinter.messagebox.showinfo("", "查询已完成。请修改已标记成语的错误。")
        else:
            tkinter.messagebox.showinfo("", "查询已完成。无错误。")


async def async_main(idioms, function, pool):
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(pool)
        tasks = []
        for idiom in idioms:
            task = asyncio.ensure_future(function(sem, idiom, session))
            tasks.append(task)
        a = await asyncio.gather(*tasks)
        return a


def search_definition_first_time_threading(all_input_idiom):

    global all_output_idiom, is_searching, last_search_time, searched_count, all_count, start_searching_time

    all_output_idiom = ""

    is_searching = True

    idioms = [
        idiom for idiom in keep_chinese(all_input_idiom).split() if idiom
    ]  # 成语文本格式化后转列表

    all_count = len(idioms)
    start_searching_time = time.time()
    last_search_time = time.time()
    searched_count = 0

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    all_output_idiom = "\n".join(
        loop.run_until_complete(async_main(idioms, fetch_for_first_searching, POOL))
    )
    loop.close()

    is_searching = False


async def fetch_for_first_searching(sem, idiom, session):

    global last_search_time, searched_count, timeouts

    async with sem:
        url = "https://hanyu.baidu.com/s"
        params = {"wd": idiom, "ptype": "zici"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        }
        try:
            async with session.get(
                url, params=params, headers=headers, timeout=10
            ) as resp:
                idiom_html = await resp.text()
            timeouts = 0
        except:
            idiom_html = ""
            timeouts += 1
            if timeouts == 5:
                tkinter.messagebox.showerror("", "请求超时，请重试，或重启电脑后重试。")
                root.destroy()
    if idiom_html.find('<div class="tab-content">') != -1:
        passage_texts = (
            bs4.BeautifulSoup(idiom_html, "lxml")
            .find(class_="tab-content")
            .find_all(name="p")
        )  # 词条的释义一栏
        output_idiom = (
            idiom
            + "："
            + "".join(
                [passage_text.contents[0].string for passage_text in passage_texts]
            )
            .replace(" ", "")
            .replace("\n", "")
        )  # p节点除子节点外内容
    elif idiom in [x.decode() for x in list(SPECIAL_WORDS)]:
        output_idiom = idiom + "：" + SPECIAL_WORDS[idiom.encode()].decode()
    else:
        output_idiom = "██" + idiom  # 错误码

    try:
        last_search_time = time.time()
        searched_count += 1
        unsearched_count = all_count - searched_count
        used_time = last_search_time - start_searching_time
        speed = searched_count / used_time
        rest_time = unsearched_count / speed
        progress.set(
            "预计剩余时间：{}s\n{}\n{}个/s".format(
                str(int(rest_time)),
                str(progress_bar(searched_count / all_count, 15)),
                str(int(speed)),
            )
        )
    except ZeroDivisionError:
        searched_count += 1
        progress.set("完成度：100%")

    return output_idiom


def search_definition_again_threading(all_input_idiom):

    global all_output_idiom, is_searching, last_search_time, searched_count, all_count, start_searching_time

    idioms = [idiom for idiom in all_input_idiom.split() if idiom]

    all_output_idiom = ""

    is_searching = True

    all_count = len(
        [idiom for idiom in idioms if idiom.find("：") == -1]
    )  # 没有":"，即没查过的词语总数
    start_searching_time = time.time()
    last_search_time = time.time()
    searched_count = 0

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    all_output_idiom = "\n".join(
        loop.run_until_complete(async_main(idioms, fetch_for_searching_again, POOL))
    )
    loop.close()

    is_searching = False


async def fetch_for_searching_again(sem, idiom, session):

    global last_search_time, searched_count, timeouts

    if idiom.find("：") != -1:
        output_idiom = idiom
    else:
        async with sem:
            url = "https://hanyu.baidu.com/s"
            params = {"wd": idiom, "ptype": "zici"}
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            }
            try:
                async with session.get(
                    url, params=params, headers=headers, timeout=10
                ) as resp:
                    idiom = idiom.replace("█", "")
                    idiom_html = await resp.text()
                timeouts = 0
            except:
                idiom_html = ""
                timeouts += 1
                if timeouts == 5:
                    tkinter.messagebox.showerror("", "请求超时，请重试，或重启电脑后重试。")
                    root.destroy()
        if idiom_html.find('<div class="tab-content">') != -1:
            passage_texts = (
                bs4.BeautifulSoup(idiom_html, "lxml")
                .find(class_="tab-content")
                .find_all(name="p")
            )
            output_idiom = (
                idiom
                + "："
                + "".join(
                    [passage_text.contents[0].string for passage_text in passage_texts]
                )
                .replace(" ", "")
                .replace("\n", "")
            )
        elif idiom in [x.decode() for x in list(SPECIAL_WORDS)]:
            output_idiom = idiom + "：" + SPECIAL_WORDS[idiom.encode()].decode()
        else:
            output_idiom = "██" + idiom  # 错误码

        try:
            last_search_time = time.time()
            searched_count += 1
            unsearched_count = all_count - searched_count
            used_time = last_search_time - start_searching_time
            speed = searched_count / used_time
            rest_time = unsearched_count / speed
            progress.set(
                "预计剩余时间：{}s\n{}\n{}个/s".format(
                    str(int(rest_time)),
                    str(progress_bar(searched_count / all_count, 15)),
                    str(int(speed)),
                )
            )
        except ZeroDivisionError:
            searched_count += 1
            progress.set("完成度：100%")
    return output_idiom


def output_definition():

    all_output_idiom_definition = "\n".join(
        [
            idiom for idiom in text_box.get("0.0", "end").strip().split() if idiom
        ]  # 按空字符串划分后再连接的成语释义和未查出的成语
    )
    all_output_idiom = "\n".join(
        [
            line.split("：")[0] if line.find("：") != -1 else line.strip()
            for line in all_output_idiom_definition.split()
        ]
    )  # 按空字符串划分，从释义行提出冒号之前的成语再连接

    with open("成语总集.txt", "r+", encoding="gbk") as all_idiom_file:
        content = all_idiom_file.read()
        all_idiom_file.seek(0, 0)
        all_idiom_file.write(
            str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            + "\n"
            + all_output_idiom
            + "\n\n"
            + content
        )
    with open("释义总集.txt", "r+", encoding="gbk") as all_definition_file:
        content = all_definition_file.read()
        all_definition_file.seek(0, 0)
        all_definition_file.write(
            str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            + "\n"
            + all_output_idiom_definition
            + "\n"
            + content
        )

    tkinter.messagebox.showinfo("", "成语已自动追加至成语总集.txt中。释义已自动追加至释义总集.txt中。")


def quit_main():
    pure_messagebox(
        "感谢使用IDerek。反馈请发送至邮箱792405142@qq.com或github@This-username-is-available。"
    )
    root.destroy()


if __name__ == "__main__":

    # import sys

    # reload(sys)
    # sys.setdefaultencoding("utf-8")

    is_searching = True
    word_nums = set()
    disposable_widgets = set()
    SPECIAL_WORDS = {
        b"\xe4\xb8\x80\xe7\x8f\xad\xe9\x9c\xb8\xe6\xb0\x94": b"\xe6\xb0\xb8\xe4\xb9\x85\xe6\xb5\x81\xe4\xbc\xa0",
        b"\xe9\xaa\x8c\xe8\xaf\x81\xe9\x97\xae\xe9\xa2\x98\xe7\xad\x94\xe6\xa1\x88": b"[0]",
    }
    CHECK_INTERVAL = 1  # (s)
    POOL = 25
    pure_messagebox(
        """欢迎使用IDerek。
    请确定有网络连接。
    请从现在开始认真留意下方提示框中的每一个字！！
    反馈请发送至邮箱792405142@qq.com或github@This-username-is-available。"""
    )

    root = tkinter.Tk()
    root.title("IDerek")
    width, height = root.maxsize()
    root.geometry("{}x{}".format(width, height))

    menubar = tkinter.Menu(root, tearoff=False)
    text_box = tkinter.scrolledtext.ScrolledText(
        root, width=100, height=18, font=("微软雅黑", 10)
    )
    text_box.pack()
    text_box.bind("<Button-3>", lambda x: right_key(x, text_box))  # 右键菜单

    INTERFACE3 = (
        (
            "Button",
            root,
            "再次查询释义并标记",
            20,
            2,
            lambda: search_definition_gui(search_definition_again_threading),
        ),
        ("Button", root, "输出释义至文件", 20, 2, output_definition),
        ("Button", root, "退出", 20, 2, quit_main),
        (
            "Label",
            root,
            """有标记的成语需手工改错，改错时更正汉字的错误即可，不需要删去空行和空格以及“█”。要保证每行不能有两个及以上成语。中间有标点的成语应写到一行里并把标点去掉。
    手工改错后再次查询，会把未查询的成语释义查出，如果还有错误可以改正后再查。
    若有某些“█”误标记，很可能是上一步的字数类型输入错误，如果不是请再试一次，还不行的话直接输出，后期处理时再改动文件。""",
            120,
            8,
        ),
    )

    INTERFACE2 = (
        (
            "Button",
            root,
            "整理，查询释义并标记",
            20,
            2,
            lambda: search_definition_gui(search_definition_first_time_threading),
        ),
        (
            "Label",
            root,
            """首次查询会将原来杂乱的文本自动整理为每行一个成语+该成语释义的标准格式并用“██”标记查不到或有错误的成语。""",
            120,
            8,
        ),
    )

    INTERFACE1 = (
        ("Button", root, "点击以输入字数类型", 20, 2, input_word_num),
        ("Button", root, "下一环节", 20, 2, to_search_definition),
        (
            "Label",
            root,
            "输入字数类型会将输入框中的纯数字作为字数类型输入并清空输入框。例如成语里有四，六，八字成语，那就分三次输入，每次只输入一个纯数字——比如“4”，然后按下按钮，再重复如上步骤分别输入“6”、“8”。输完所有字数类型后再进行下一环节。",
            120,
            8,
        ),
    )

    change_disposable_widget(INTERFACE1)
    root.mainloop()
