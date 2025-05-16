<template>
    <!-- 导航栏 -->
    <div class="nav-bar">
      <div 
        v-for="nav in navList" 
        :key="nav.id" 
        :class="['nav-item', { active: isActive === nav.id }]" 
        @click="handleNavClick(nav.id)"
      >
        {{ nav.title }}
      </div>
    </div>

    <div class="recommonContain">
        <!-- 为你推荐导航栏 -->
        <div v-if="isActive==1" class="mainContent">
            <div class="mainsign">
                <h3>歌单标签</h3>
                <ul class="lists">
                    <li v-for="(item,index) in playlist.tags" :key="index" @click="getTagMusic(item+'+2')">{{item}}</li>
                </ul>
            </div>

            <div class="mainsign">
                <h3>歌曲标签</h3>
                <ul class="lists">
                    <li v-for="(item,index) in song.tags" :key="index" @click="getTagMusic(item+'+3')">{{item}}</li>
                </ul>
            </div>

            <div class="mainsign">
                <h3>歌手标签</h3>
                <ul class="lists">
                    <li v-for="(item,index) in sing.tags" :key="index" @click="getTagMusic(item+'+4')">{{item}}</li>
                </ul>
            </div>
        </div>


        <!-- 歌单导航栏 -->
        <div v-if="isActive==2" class="mainContent">
            <div class="singCon singSongCon">
                <h3>歌单标签</h3>
                <ul class="signslists">
                    <li :class="tag == 'all' ? 'oktag' : '' " @click="getTagMusic('all')">全部</li>
                    <li :class="tag == item ? 'oktag' : '' " v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">{{item}}</li>
                    <li v-if="tags.length<=15" class="moretag" @click="getMoreTag()">更多</li>
                </ul>

                <div class="allsign">
                <ul class="relists">
                    <li v-for="item in playlists" :key="item.pl_id" class="relist singlists" @click="musicDesc(item.pl_id)">
                        <img :src="item.pl_img_url"/>
                        <p class="recreater">{{item.pl_creator}}</p>
                        <p class="rename">{{item.pl_name}}</p>
                    </li>
                </ul>
                </div>
            </div>

            <div class="singCon singSong">
                <h3>歌单推荐</h3>
                <ul class="relists">
                <li v-for="item in recomm_playlists" :key="item.pl_id" class="relist" @click="musicDesc(item.pl_id)">
                    <img :src="item.pl_img_url"/>
                    <p class="recreater">{{item.pl_creator}}</p>
                    <p class="rename">{{item.pl_name}}</p>
                </li>
                <!-- <li class="more" @click="getCateMusic({'cateid': '6','rectag': '1'})">更多 >></li> -->
                </ul>
            </div>
        </div>


        <!-- 歌曲导航栏 -->
        <div v-if="isActive==3" class="mainContent">
            <div class="singCon singSongCon">
                <h3>歌曲标签</h3>
                <ul class="signslists">
                    <li :class="tag == 'all' ? 'oktag' : ''" @click="getTagMusic('all')">全部</li>
                    <li  :class="tag == item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">{{item}}</li>
                    <li v-if="tags.length <=15" class="moretag" @click="getMoreTag()">更多</li>
                </ul>

                <div class="allsign">
                <ul class="relists">
                    <li v-for="item in songs" :key="item.song_id" class="onelist" @click="musicDesc(item.song_id)">
                        <p class="onename">{{item.song_name}}</p>
                        <p class="onetime">{{item.song_publish_time}}</p>
                    </li>
                </ul>
                </div>
            </div>

            <div class="singCon singSong">
                <h3>歌曲推荐</h3>
                <ul class="relists">
                <li v-for="item in recomm_songs" :key="item.song_id" class="onelist" @click="musicDesc(item.song_id)">
                    <p class="onename">{{item.song_name}}</p>
                    <p class="onetime">{{item.song_publish_time}}</p>
                </li>
                <!-- <li class="more" @click="getCateMusic({'cateid': '6','rectag': '2'})">更多 >></li> -->
                </ul>
            </div>
        </div>


        <!-- 歌手导航栏 -->
        <div v-if="isActive==4" class="mainContent">
            <div class="singCon singSongCon">
                <h3>歌手标签</h3>
                <ul class="signslists">
                    <li :class="tag == 'all' ? 'oktag' : ''" @click="getTagMusic('all')">全部</li>
                    <li :class="tag == item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">{{item}}</li>
                    <li v-if="tags.length <=15" class="moretag" @click="getMoreTag()">更多 >></li>
                </ul>

                <div class="allsign">
                <ul class="relists">
                    <li v-for="item in sings" :key="item.sing_id" class="relist singlists" @click="musicDesc(item.sing_id)">
                        <img :src="item.sing_url"/>
                        <p class="recreater"></p>
                        <p class="rename">{{item.sing_name}}</p>
                    </li>
                </ul>
                </div>
            </div>

            <div class="singCon singSong">
                <h3>歌手推荐</h3>
                <ul class="relists">
                <li v-for="item in recomm_sings" :key="item.sing_id" class="relist" @click="musicDesc(item.sing_id)">
                    <img :src="item.sing_url"/>
                    <p class="recreater"></p>
                    <p class="rename">{{item.sing_name}}</p>
                </li>
                <!-- <li class="more" @click="getCateMusic({'cateid': '6','rectag': '3'})">更多 >></li> -->
                </ul>
            </div>
        </div>


        <!-- 用户导航栏 -->
        <div v-if="isActive==5" class="mainContent">
            <div class="singCon singSongCon">
                <h3>用户标签</h3>
                <ul class="signslists">
                    <li :class="tag == 'all' ? 'oktag' : ''" @click="getTagMusic('all')">全部</li>
                    <li :class="tag == item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">{{item}}</li>
                    <li v-if="tags.length <=15" class="moretag" @click="getMoreTag()">更多 >></li>
                </ul>
                <div class="allsign">
                <ul class="relists">
                    <li v-for="item in users" :key="item.u_id" class="relist singlists" @click="musicDesc(item.u_id)">
                        <img :src="item.u_img_url"/>
                        <p class="recreater"></p>
                        <p class="rename">{{item.u_name}}</p>
                    </li>
                </ul>
                </div>
            </div>
            <div class="singCon singSong">
                <h3>用户推荐</h3>
                <ul class="relists">
                <li v-for="item in recomm_users" :key="item.u_id" class="relist" @click="musicDesc(item.u_id)">
                    <img :src="item.u_img_url"/>
                    <p class="recreater"></p>
                    <p class="rename">{{item.u_name}}</p>
                </li>
                </ul>
            </div>
        </div>


        <!-- 音乐会导航栏 -->
        <div v-if="isActive==6" class="mainContent">
            <div class="singCon singSongCon">
                <h3>音乐会信息</h3>
                <div class="allsign">
                <ul class="relists">
                    <li v-for="item in sings" :key="item.sing_id" class="relist singlists" @click="musicDesc(item.sing_id)">
                        <img :src="item.sing_url"/>
                        <p class="recreater"></p>
                        <p class="rename">{{item.sing_name}}音乐会</p>
                    </li>
                </ul>
                </div>
            </div>

            <div class="singCon singSong">
                <h3>音乐会推荐</h3>
                <ul class="relists">
                <li v-for="item in recomm_sings" :key="item.sing_id" class="relist" @click="musicDesc(item.sing_id)">
                    <img :src="item.sing_url"/>
                    <p class="recreater"></p>
                    <p class="rename">{{item.sing_name}}音乐会</p>
                </li>
                <!-- <li class="more" @click="getCateMusic({'cateid': '6','rectag': '3'})">更多 >></li> -->
                </ul>
            </div>
        </div>


        <!-- 排行榜导航栏 -->
        <!-- <div v-if="isActive==6" class="mainContent">

        </div> -->

        <!-- 我的足迹导航栏 -->


    </div>
</template>

<script>
import { getHomeCategoriesData, getRecommon } from '@/js/api'
// import newheader from '../components/NewHeader.vue'
export default {
    data() {
        return { 
            isActive: 1,
            navList: [
              { id: 1, title: "为你推荐" },
              { id: 2, title: "歌单" },
              { id: 3, title: "歌曲" },
              { id: 4, title: "歌手" },
              { id: 5, title: "用户" },
              { id: 6, title: "音乐会"},
            ],
            refresh: false, // 是否刷新（第一页激活）有搜索时需要
            playlist: {},
            song: {},
            sing: {},
            username: '',
            // 为你推荐导航栏的信息
            tags: [],
            
            // 歌单导航栏
            playlists: {},
            recomm_playlists :[],   // 相似歌单推荐
            // 歌曲导航栏
            songs: [],
            recomm_songs: [],
            // 歌手导航栏
            sings: [],
            recomm_sings: [],
            // 用户导航栏
            users: [],
            recomm_users: [],

            newsData: {},
            tmptags: [],
            
            tag: 'all'
        }
    },

    components: {
        // 'mheader': newheader
    },

    methods: {
        getCateMusic(option) {
            var cateId = option.cateid;
            var request = {};
            // 初始化基础参数
            this.initBaseParams(option, cateId);
    
            // 处理不同分类的逻辑
            if (cateId === '1') {
                this.handleHomeCategory(option, request);
            } else {
                this.handleOtherCategories(option, request, cateId);
            }
        },

        // 初始化参数
        initBaseParams(option, cateid) {
            option.tag = option.tag || 'all';
            option.page = option.page || 1;
            this.rectag = option.rectag || '0';
            this.tag = option.tag;
            this.isActive = cateid;
        },

        // 从首页获取分类数据
        handleHomeCategory(option, request) {
            request.cateid = '1';
            request.username = this.username;
            if (option.sings) {
                request.sings = option.sings;
                request.songs = option.songs;
            } else {
                request.sings = '';
                request.songs = '';
            }
            if (option.baseclick === '0') {
                request.baseclick = 0;
            } else {
                request.baseclick = 1;
            }

            // 发送请求
            getHomeCategoriesData(request).then((res) => {
                if (!res.code) {
                    // 后端返回数据异常
                    console.log(res.code);
                } else {
                    this.playlist = res.data.playlist;
                    this.sing = res.data.sing;
                    this.song = res.data.song;
                }
            }), (err) => {
                console.log(err);
            }
        },

        // 从其他导航栏获取数据
        handleOtherCategories(option, request, cateId) {
            request.cateid = cateId;
            request.sings = '';
            request.songs = '';
            request.baseclick = 1;
            request.tag = option.tag;
            request.page = option.page;
            request.username = this.username;

            // 获取推荐信息
            this.fetchRecommendations(cateId, request);

            // 处理 cateId=6 的特殊逻辑（排行榜）
            const shouldSkipRequest = this.shouldSkipRequest(cateId);
            if (shouldSkipRequest) {
                this.$layer.closeAll();
                return;
            }

            // 发送通用数据请求
            getHomeCategoriesData(request).then(res => {
                // this.$layer.closeAll();
                this.processResponseData(res, cateId);
            }).catch(this.handleError);

        },

        // 获取推荐信息
        fetchRecommendations(cateId, request) {
            if (['2', '3', '4', '5'].includes(cateId)) {
                const recommendRequestData = {
                    cateid: cateId,
                    username: request.username,
                };
                getRecommon(recommendRequestData).then(res => {
                    if (res.code === 1) {
                        this.assignRecommendations(res.data, cateId);
                    } else if (res.code == -1) {
                        console.log("后台还未导入相关数据，请求不成功")
                    } 
                });
            }
        },

        // 根据响应设置推荐数据
        assignRecommendations(data, cateId) {
            switch (cateId) {
                case '2':
                    this.recomm_playlists = data.recomm_playlists;
                    break;
                case '3':
                    // res.data.songs.forEach(item => item.song_publish_time = this.timeFormat(item.song_publish_time));
                    this.recomm_songs = data.songs;
                    break;
                case '4':
                    this.recomm_sings = data.sings;
                    break;
                case '5':
                    this.recomm_users = data.users;
                    break;
            }
        },

        // 判断是否需要跳过请求（针对 cateId=6）
        shouldSkipRequest(cateId) {
            if (cateId !== '6') return false;

            return (
                (this.rectag === '0' && this.sortplaylist.length && this.sortsing.length && this.sortsong.length) ||
                (this.rectag === '1' && this.sortplaylist.length) ||
                (this.rectag === '2' && this.sortsong.length) ||
                (this.rectag === '3' && this.sortsing.length)
            );
        },

        // 处理响应数据
        processResponseData(res, cateId) {
            if (!res.code) {
                this.$children[0].layout();
                return;
            }

            // 统一处理 tags
            if (res.data.tags) {
                this.tags = res.data.tags.slice(0, 15);
                this.tmptags = res.data.tags;
            }

            // 根据 cateId 分配数据到对应属性
            switch (cateId) {
                case '2':
                    this.assignPlaylistData(res);
                    break;
                case '3':
                    this.assignSongData(res);
                    break;
                case '4':
                    this.assignSingerData(res);
                    break;
                case '5':
                    this.assignUserData(res);
                    break;
                case '6':
                    this.assignRankingData(res);
                    break;
                case '7':
                    this.assignClickData(res);
                    break;
            }
        },

        // 分配歌单数据（cateId=2）
        assignPlaylistData(res) {
            this.playlists = res.data.playlist;
            this.total = res.data.total;
        },

        // 分配歌曲数据（cateId=3）
        assignSongData(res) {
            // 数据的时间格式处理
            // res.data.songs.forEach(item => item.song_publish_time = this.timeFormat(item.song_publish_time));
            this.songs = res.data.songs;
            this.total = res.data.total;
        },

        // 分配歌手数据（cateId=4）
        assignSingerData(res) {
            this.sings = res.data.sings;
            this.total = res.data.total;
        },

        // 分配用户数据（cateId=5）
        assignUserData(res) {
            this.users = res.data.sings; // 需确认是否应为 `users`
            this.total = res.data.total;
        },

        // 分配排行榜数据（cateId=6）
        assignRankingData(res) {
            this.total = 1;
            res.data.song.forEach(item => item.song_publish_time = this.timeFormat(item.song_publish_time));
            res.data.playlist.forEach(item => item.pl_create_time = this.timeFormat(item.pl_create_time));

            this.tmpplay = res.data.playlist.slice(0, 20);
            this.tmpsing = res.data.sing.slice(0, 20);
            this.tmpsong = res.data.song.slice(0, 20);

            switch (this.rectag) {
                case '1':
                    this.sortplaylist = res.data.playlist;
                    break;
                case '2':
                    this.sortsong = res.data.song;
                    break;
                case '3':
                    this.sortsing = res.data.sing;
                    break;
                default:
                    this.sortplaylist = res.data.playlist;
                    this.sortsing = res.data.sing;
                    this.sortsong = res.data.song;
            }
        },

        // 分配点击数据（cateId=7）
        assignClickData(res) {
            res.data.click.forEach(item => item.time = this.timeFormat(item.time));
            this.total = res.data.total;
            this.datas = res.data.click;
        },

        // 统一错误处理
        handleError(err) {
            console.log("请求失败", err)
        },

        // 根据标签获取音乐
        getTagMusic(option) {
            this.refresh = true
            this.tags = this.tags.slice(0, 15)
            if (option.indexOf('+') > -1) {
                var tmp_tag = option.split('+')
                this.tag = tmp_tag[0]
                this.isActive = tmp_tag[1]
            } else {
                this.tag = option
            }
            console.log("get music from tag, isActive:%s tags:%s", this.isActive, this.tag)
            this.getCateMusic({
                'cateid': this.isActive,
                'tag': this.tag
            })
        },

        // 获取更多tag
        getMoreTag() {
            this.tags = this.tmptags
        },

        musicDesc(id) {
            if (id.indexOf('+') > -1) {
                var tmpid = id.split('+')
                id = tmpid[0]
                this.isActive = tmpid[1]
                console.log(tmpid[1])
            }
            this.$router.push({
                name: 'one',
                query: {
                    id: id,
                    cateid: this.isActive
                }
            })
        },

        handleNavClick(id) {
          this.isActive = id;

          // 重置标签选择（默认选中 "全部"）
          this.tag = 'all';
          this.tags = [];

          // 根据导航栏 ID 调用数据接口
          this.getCateMusic({
            cateid: id.toString(),
            tag: 'all',
            page: 1,
            baseclick: 1
          });
        },
      },

    mounted () {
        this.username = this.$route.query.username
        var sings = this.$route.query.sings
        var songs = this.$route.query.songs
        var baseClick = this.$route.query.baseClick
        if (this.$route.params.cateid) {
            this.getCateMusic({'cateid': this.$route.params.cateid})
        } else {
            // 首页获取音乐分类数据
            this.getCateMusic({
                'cateid': '1',
                'sings': sings,
                'songs': songs,
                'baseclick': baseClick
            })
        }
    }
}

</script>

<style lang="less" scoped>
  @baseColor:#20a0ff;
  #ellies(@n){
    overflow: hidden;
    text-overflow: ellipsis;
    -webkit-line-clamp: @n;
    -webkit-box-orient: vertical;
    white-space: nowrap;
  }
  .nav-bar {
    display: flex;
    gap: 20px;
    padding: 10px;
    background: #f5f5f5;
  }

  .nav-item {
    cursor: pointer;
    padding: 8px 16px;
    border-radius: 4px;
  }

  .nav-item.active {
    background: #409eff;
    color: white;
  }
  .recommonContain{
    width: 100%;
    padding:2% 8%;
    padding-bottom: 0;
    box-sizing: border-box;
    .mainContent{
      width: 100%;
      display: flex;
      box-sizing: border-box;
      justify-content: space-around;
      .mainsign{
        width: 32%;
        box-sizing: border-box;
        padding:10px;
        border:1px solid #ddd;
        margin:15px 30px;
        box-shadow: 0 0 5px 5px #eee;
        min-height: 300px;
        .lists {
          margin-top: 10px;
          li {
            padding: 6px 8px;
            border-radius: 4px;
            color: #333;
            font-size: 16px;
            width: auto;
            display: inline-block;
            border: 1px solid #ddd;
            cursor: pointer;
            margin: 5px;
          }
          li:first-child{
            color: orange;
            border: 1px solid orange;
          }
          li:nth-child(2){
            color: red;
            border: 1px solid red;
          }
          li:nth-child(3){
            color: coral;
            border: 1px solid coral;
          }
          li:nth-child(4){
            color: chocolate;
            border: 1px solid chocolate;
          }
          li:hover {
            color: @baseColor;
            border: 1px solid @baseColor;
          }
        }
        .musiclis{
          li{
            width: 100%;
            box-sizing: border-box;
            b{
              img{
                width: 50px;
                height:50px;
                border-radius: 25px;
              }
            }
            span{
              display: inline-block;
              width: 30%;
              #ellies(1);
              vertical-align: middle;
              font-size: 12px;
            }
            span:last-child{
              font-size: 14px;
              width: 43%;
              float: right;
              line-height: 50px;
            }
            span.songname{
              font-size: 14px;
              width: 50%;
            }
            span.songtime{
              font-size: 12px;
              width: 37%;
            }
            span.singer{
              width: 65%;
            }
          }
        }
      }
      .singlemainsign{
        width: 100%;
        .lists{
          li{
            display: flex;
            justify-content: space-around;
            align-items: center;
            .icon{
              width: 140px;
            }
            span{
              margin-left: 15px;
            }
          }
          li:first-child{
            color: #666;
            border: none;
          }
          li:first-child:hover {
            color: #666;
            border: none;
          }
        }
      }
      .singCon{
        box-sizing: border-box;
        padding:10px;
        border:1px solid #ddd;
        box-shadow: 0 0 5px 5px #eee;
        min-height: 500px;
        margin-top:15px;
        margin-bottom: 15px;
        .signslists{
          margin-top:10px;
          li{
            display: inline-block;
            border: 1px solid #ddd;
            box-sizing: border-box;
            padding: 6px;
            border-radius: 4px;
            margin:5px;
            text-align: center;
            cursor: pointer;
            font-size: 12px;
            &:hover{
              color: @baseColor;
              border: 1px solid @baseColor;
            }
          }
          .oktag{
            color: @baseColor;
            border: 1px solid @baseColor;
          }
          .moretag{
            color: orange;
            border: 1px solid orange;
          }
        }
        .relists{
          margin-top:20px;
          display: flex;
          justify-content: space-around;
          flex-wrap: wrap;
          .more{
            padding: 5px;
            border:1px solid orange;
            color:#fff;
            background: orange;
            text-align: center;
            width: 120px;
            border-radius: 3px;
            height: 30px;
            line-height: 30px;
            margin-top:15px;
            cursor: pointer;
          }
          .relist{
            width: 30%;
            box-sizing: border-box;
            padding: 5px;
            color: #333;
            cursor: pointer;
            margin-bottom: 15px;
            &:hover{
              color: @baseColor;
            }
            .recreater{
              font-size: 12px;
              color: #666;
              line-height: 14px;
              margin-bottom: 5px;
              margin-top: 5px;
              #ellies(1)
            }
            .rename{
              font-size: 14px;
              line-height: 16px;
              #ellies(1)
            }
            img{
              width: 100%;
            }
          }
          .singlists{
            width: 20%;
          }
          .onelist{
            width: 100%;
            color:#666;
            margin:5px 0;
            display: flex;
            justify-content: space-between;
            cursor: pointer;
            &:hover{
              color:@baseColor;
            }
            .onetime,.onename{
              #ellies(1);
              display: inline-block;
              box-sizing: border-box;
              padding: 0 10px;
            }
          }
        }
      }
      .singSongCon{
        flex: 2;
        margin-right: 15px;
      }
      .singSong{
        flex: 1;
        margin-left: 15px;
        min-width: 30%;
      }
      .liscan{
        width: 100%;
        li{
          width: 100%;
          color: #666;
          font-size: 14px;
          display: block;
          margin:20px;
          span{
            display: inline-block;
            width: 40%;
          }
        }
        li:first-child{
          color: #000;
        }
      }
      .recnav{
        width: 10%;
        min-width: 120px;
        padding-left: 20px;
        margin-top:20px;
        box-sizing: border-box;
        li{
          width: 100%;
          height: 30px;
          box-sizing: border-box;
          line-height: 30px;
          padding-left: 20px;
          color: #666;
          cursor: pointer;
        }
        .active{
          background: #eee;
          box-shadow: 10px 0px 10px 1px @baseColor;
        }
      }
    }
    .rightpag{
      width: 70%;
    }
  }
</style>
