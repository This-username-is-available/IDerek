# IDerek（语流）

<img src="https://i.loli.net/2020/03/13/ShB1HLiFNCOAW6u.png"  width="50">

包括成语单OCR结果格式化，自动改错，批量查询成语或词语释义。极其业余，大神轻喷。

可以查询（包括但不限于）汉字，词语，术语，成语。

**本项目内不含OCR软件！！只提供对OCR结果的处理！！**

**本人学生党，本身水平非常菜且没时间，内含大量只能用不能看的意面代码！！不希望任何人贡献此项目，除非您有极大的耐心和意志力！！**

## 配置

标准版：Windows7+操作系统或Python3.6+

xp版：Windows xp+操作系统或Python2.7+

## 安装

直接下载。

## 用法

运行exe文件，自带GUI。还需要成语单的OCR结果或成语文本，对文本格式几乎无要求。

## 原理

通过除逗号外的非汉字字符划分输入的OCR结果来格式化同时允许中间有逗号的成语的存在。

通过百度汉语的（伪）API接口抓取词条页面，百度汉语中能查到的视为正确。

通过在成语数据库中进行相似度比对实现自动改错。

爬取成语数据库的脚本在我的项目[my-baiduhanyu](https://github.com/This-username-is-available/my-baiduhanyu)中，还附带一个爬释义的。

## 关于不同版本

xp版是Windows通用的。但是查词逻辑相当落后，不支持自动改错，错误率较高。而且巨！慢！无！比！。Windows xp只能用这个版本。现已停止更新功能。

标准版只能用在Win7以上操作系统，速度飞快，支持自动改错。

## 对OCR结果格式的要求

成语和成语之间有任意的非汉字字符（包括空格和换行）即可。

例如像下面这些都符合要求：

> 558.一无所获，364、二三其德
>
> 四体不勤/五谷不分 六神无主
>
> 七拼八凑djjdii妄九言十，？'?啰嗦，

唯一不好弄的例子是下面这种：

> 荦荦大端耳濡目染声嘶力竭著书立说

或者这样：

> 眈眈逐逐，上行下效，迫在眉睫，定夺

（拿什么分隔都行就是别两个成语之间只用一个逗号！！那是标识八字成语用的！！）

这种可能需要你去程序界面按几十个enter才行……更好的选择是换一个能帮你排版的OCR软件。

## 权威性

你完全可以把它当成一个快捷版百度汉语。百度汉语权威性还是有保障的，至少比百度百科靠谱。对付高考还是绰绰有余。

没有采用某些现成的开源数据库，一是其中数据有很多错误，二是考虑到时效性。为了权威性和全面性还特意做了很多努力。

## 自定义成语释义

自行改动user_data.json。

## 下一步可能的改进方向

- 行首是否带序号

- 成语之间是否空行

真需要的可以issue或者发邮箱，需要的人多再加入。

## 作者

- Github：[@This-username-is-available](https://github.com/This-username-is-available)

- 邮箱：<792405142@qq.com>

## 支持

如果这个项目帮到了你，给我个星标吧！

也可以扫这个赞助二维码请我喝杯咖啡哦~

<img src="https://i.loli.net/2020/03/13/83wLpUO7ZJb1qya.jpg"  width="250">

## License

MIT License

Copyright © 2020 This-username-is-available

**本项目不用于任何商业用途！！侵删！！**
