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
### 使用GithubActions部署
  使用GithubActions，无需服务器即可每天自动运行脚本
- 使用教程
  - 在github创建个空仓库
  - 创建/.github/workflows/actions.yml
  - actions.yml内容如下，将里面的phone和password改成自己的网易云账号密码即可
- actions.yml
    ```yaml
    name: 网易云音乐日推自动创建歌单

    on:
      schedule:
        # * is a special character in YAML so you have to quote this string
        - cron:  '* */1 * * *'

    jobs:
      build:

        runs-on: ubuntu-latest

        steps:
        - name: 更新为中国时间
          run: |
            sudo rm -rf /etc/localtime 
            sudo ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
            date
        - name: 安装网易云api
          run: git clone https://github.com/shanghaobo/NeteaseCloudMusicApi.git
        - name: 运行网易云api
          run: |
            cd NeteaseCloudMusicApi
            npm install
            nohup node app.js &
        - name: 安装并脚本
          run: git clone https://github.com/shanghaobo/NeteaseCloudMusicDay.git
        - name: 设置api
          run: echo "api='http://127.0.0.1:3000'" >> NeteaseCloudMusicDay/config.py
        - name: 设置网易云音乐登录账号
          run: echo "phone='xxxxxxxxxxx'" >> NeteaseCloudMusicDay/config.py
        - name: 设置网易云音乐登录密码
          run: echo "password='xxxxxx'" >> NeteaseCloudMusicDay/config.py
        - name: 运行脚本
          run: python3 NeteaseCloudMusicDay/main2.py

    ```

### 使用效果

  <img src="demo.jpg"  width="300px">