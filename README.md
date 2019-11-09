### 功能

自动获取网易云音乐每日推荐歌曲，并添加到以日期命名的新歌单。

### 开发背景

昨天我脑子里突然想起来前几天网易云音乐给我推荐的一首歌，莫名感觉好听，但是当时没有收藏，也记不清歌名，我就去网易云音乐看有没有历史推荐记录。
结果发现只有会员才能查看日推记录，而且只能看近5天的，索性自己写了这个脚本。

### 使用环境
- Python 3.7
- 本项目依赖于[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)，请先搭建好环境
    推荐使用docker镜像一键部署

    ```bash
    docker pull binaryify/netease_cloud_music_api
    docker run -d -p 3000:3000 --name netease_cloud_music_api    binaryify/netease_cloud_music_api
    ```
    其他方式请参考官方文档
   [https://binaryify.github.io/NeteaseCloudMusicApi](https://binaryify.github.io/NeteaseCloudMusicApi)

### 使用帮助

- 将config.sample.py 改名为 config.py，并配置账户信息
- 运行main.py即可

    ```bash
    python main.py
    ```
