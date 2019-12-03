import requests as r
import time
from . import MyLog
from . import config
log=MyLog.log

class CloudMusic:
    def __init__(self,api,phone,password):
        self.api = api
        self.phone=phone
        self.password=password
        self.s=r.session()

    def get(self,url):
        return self.s.get(self.api+url)

    def login(self):
        """登录"""
        res = self.get('/login/cellphone?phone=%s&password=%s' % (self.phone, self.password))
        data=res.json()
        if data.get('account'):
            return data.get('account').get('id')
        return None

    def refresh(self):
        """刷新登录状态"""
        res=self.get('/login/refresh')
        data=res.json()
        if data.get('code')==200:
            return True
        log.info(data)
        return False

    def createMusicList(self,name):
        """创建歌单"""
        res=self.get('/playlist/create?name=%s'%name)
        data=res.json()
        id=data.get('id')
        return id

    def getDaySend(self):
        """获取每日推荐"""
        res=self.get('/recommend/songs')
        data=res.json()
        recommend=data.get('recommend')
        ids=[]
        for item in recommend:
            ids.append(str(item.get('id')))
        return ids[::-1]

    def addMusicToList(self,list_id,music_ids):
        """添加歌单歌曲"""
        res=self.get('/playlist/tracks?op=add&pid=%s&tracks=%s'%(list_id,music_ids))
        data=res.json()
        if data.get('code')==200:
            return True
        return False

    def getMusicListDetail(self,list_id):
        """获取歌单详情"""
        res=self.get('/playlist/detail?id=%s'%list_id)
        data=res.json()
        playlist=data.get('playlist')
        if not playlist:
            return []
        tracks=playlist.get('tracks')
        ids=[]
        for item in tracks:
            ids.append(str(item.get('id')))
        return ids

    def getUserMusicList(self,uid):
        """获取用户歌单"""
        res=self.get('/user/playlist?uid=%s'%uid)
        data=res.json()
        playlist=data.get('playlist')
        if not playlist:
            return []
        detail={}
        for item in playlist:
            id=item.get('id')
            name=item.get('name')
            if id and name:
                detail[name]=str(id)
        return detail


if __name__=='__main__':
    api=config.api
    phone=config.phone
    password=config.password
    log.info('开始登录')
    cm=CloudMusic(api,phone,password)
    uid=cm.login()
    if not uid:
        log.info('登录失败')
        exit(0)
    log.info('【uid=%s】'%uid)
    # 循环检测
    while True:
        try:
            flag=cm.refresh()
            log.info('刷新登录状态:%s'%flag)
            if int(time.strftime('%H'))<8:
                #网易云6点更新推荐 8点后处理避免将昨天的歌单放到今天的歌单里
                log.info('不到8点，不处理')
                log.info('等待%s秒后再次检测...' % config.sleep)
                time.sleep(config.sleep)
                continue
            list_name = time.strftime('%Y-%m-%d') + '日推'
            log.info('生成歌单名 list_name=%s' % list_name)
            user_music_list = cm.getUserMusicList(uid)
            if list_name in user_music_list:
                log.info('已有日推歌单：%s' % list_name)
                list_id = user_music_list[list_name]
            else:
                log.info('创建日推歌单：%s' % list_name)
                list_id = cm.createMusicList(list_name)
            log.info('歌单id list_id=%s' % list_id)
            log.info('获取日推歌曲：')
            day_music_ids = cm.getDaySend()
            list_music_ids = cm.getMusicListDetail(list_id)
            log.info(day_music_ids)
            will_add_list = []
            for music_id in day_music_ids:
                if music_id in list_music_ids:
                    pass
                else:
                    will_add_list.append(music_id)
            if len(will_add_list) > 0:
                music_ids = ','.join(will_add_list)
                res = cm.addMusicToList(list_id, music_ids)
                if res:
                    log.info('添加日推列表：%s【成功】' % (music_ids))
                else:
                    log.info('添加日推列表：%s【失败】' % (music_ids))
        except:
            log.error('error',exc_info=True)
        log.info('等待%s秒后再次检测...'%config.sleep)
        time.sleep(config.sleep)
