![sc2](screenshots/screenshots1.gif)

## 特性
- 支持搜索微信好友
- 支持搜索微信群
- 支持模糊搜索：中文、拼音、简拼
- 快速打开对应对话框

## 使用说明
1. 下载安装
2. 修改以下脚本中的两个参数（需要先获取微信数据库密码，方法下面有讲）
![tu](screenshots/WX20180819-104347.png)
3. 打开Alfred，输入 “sync”，同步微信联系人数据
4. 开始使用

## 获取微信数据库密码
> - 当前并没有找到更简单的方式，所以只能用 lldb 调试微信，打印出密码。
> - 自测支持：微信2.3.16 和 2.3.17 版本测试成功

获取密码过程如下：
1. 重新打开微信（停在扫码登录界面）
2. 在终端输入命令行: 
```shell
lldb -p $(pgrep WeChat)
```
3. 上面命令会进入到 lldb 中，在lldb中输入：
```shell
br set -n sqlite3_key
```
4. 输入字母 “c”, 回车
5. 手机扫码登录微信
6. 打开终端，继续在lldb中输入：
```shell
memory read --size 1 --format x --count 32 $rsi
```
得到如下结果
 ```shell
0x000000000000: 0xab 0xab 0xab 0xab 0xab 0xab 0xab 0xab
0x000000000008: 0xab 0xab 0xab 0xab 0xab 0xab 0xab 0xab
0x000000000010: 0xab 0xab 0xab 0xab 0xab 0xab 0xab 0xab
0x000000000018: 0xab 0xab 0xab 0xab 0xab 0xab 0xab 0xab
```
把左边的第1列忽略，只复制右边的8列。然后把里面的“0x”、空格、换行都删除，得到一个完整的64位字符串。这个就是最后的结果了。

## 相关介绍
https://www.jianshu.com/p/8a2df7086452

## 原理
![sc3](screenshots/WX20180819-104858.png)

> 其中读取微信数据库步骤，需要用到 lldb 给微信打断点，获取数据库密码。
> 
> PS：期待更好的数据库密码获取方式。
