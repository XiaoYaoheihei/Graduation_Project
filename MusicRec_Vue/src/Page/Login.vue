<template>
    <div class="login">
        <!-- 第一步：选择用户 -->
        <div v-if="!(showstep2 || showstep3)" class="loginstep">
            <div class="posirelative select-out-div">
                <!-- 下拉选择框 -->
                <select class="userSelect" v-model="loginUser" name="userselect">
                    <option value="">选择登陆用户</option>
                    <option v-for="(item,index) in users" :key="index" :value="item">{{item}}</option>
                </select>
            <span class="select-hide-span"><b class="select-show-b"></b></span>
            </div>
            <button class="nextBtn" @click="shownext(1)">下一步</button>
        </div>

        <div v-if="showstep2" class="loginstep2">
            <h3>选择喜爱的歌手</h3>
            <div class="alltag">
                <!-- 行容器：复选框和文本 -->
                <span class="tagbox" v-for="(tag,index) in sings" :key="index">
                    <input type="checkbox" v-model="singsTags" name="singsbox" :value="index" />
                    {{tag}}
                </span>
            </div>
            <div class="twobtn">
                <button class="skip" @click="shownext(3)">跳过</button>
                <button class="go" @click="shownext(2)">下一步</button>
            </div>
        </div>

        <div v-if="showstep3" class="loginstep2">
            <h3>选择喜爱的歌曲</h3>
            <div class="alltag">
                <span class="tagbox" v-for="(tag,index) in songs" :key="index">
                    <input type="checkbox" v-model="songsTags" name="songsbox" :value="index" />
                    {{tag}}
                </span>
            </div>
            <div class="twobtn">
                <button class="skip" @click="goLogin('skip')">跳过</button>
                <button class="go" @click="goLogin">进入系统</button>
            </div>
        </div>
    </div>
</template>

<script>
import { initPage, getLogin } from '@/js/api';

export default {
    data() {
        return {
            // 用户列表
            users: ["用户A", "用户B", "用户C"],
            // 当前选中的用户
            loginUser: "",
            // 歌手标签
            sings: ["歌手1", "歌手2", "歌手3"],
            // 歌曲标签
            songs: ["歌曲1", "歌曲2", "歌曲3"],
            // 歌手选择的复选框值（存储索引）
            singsTags: [],
            // 歌曲选择的复选框值（存储索引）
            songsTags: [],
            // 控制步骤显示
            showstep2: false,
            showstep3: false,
        };
    },
    methods: {
        // 切换步骤
        shownext(step) {
            if (step === 1) {
                // 第一步到第二步
                if (this.loginUser) {
                    this.showstep2 = true;
                } else {
                    alert("请选择登录用户！");
                }
            } else if (step === 2) {
                if (this.singsTags.length < 2 && this.singsTags.length >= 0) {
                    alert("请至少选择2个标签哦");
                } else {
                    // 第二步到第三步
                    this.showstep3 = true;
                }
            } else if (step === 3) {
                // 跳过第二步直接到第三步
                this.showstep2 = false;
                this.showstep3 = true;
            }
        },
        // 登录或跳过
        goLogin(skip) {
            var loginInfo = {
                username: this.loginUser,
                sings: '',
                songs: '',
                cate: 1,
                baseclick: 0
            }
            if (skip === "skip") {
                alert("已跳过选择歌曲步骤，即将进入系统！");
                loginInfo.sings = ''
                loginInfo.songs = ''
            } else {
                if (this.songsTags.length < 2 && this.songsTags.length >= 0) {
                    alert("请至少选择2个标签哦");
                } else {
                    loginInfo.sings = this.singsTags.join(',')
                    loginInfo.songs = this.songsTags.join(',')
                    this.singsTags = []
                    this.songsTags = []
                }
            }
            console.log(loginInfo)

            getLogin(loginInfo).then((res) => {
                if (res.code) {
                    localStorage.setItem('username', res.data.username);
                    // this.almuta(true)
                    // this.almuuser(res.data.username)
                    const redirectPath = this.$route.query.redirect || '/'; // 默认跳转到首页
                    this.$router.replace({
                        path: decodeURIComponent(redirectPath),
                        query: {
                            'username': res.data.username,
                            'sings': res.data.sings,
                            'songs': res.data.songs,
                            'baseclick': 0
                        }
                    })
                }
            }, (err) => {
                console.log(err)
            })
            // 模拟登录成功
            alert("登录成功！\n选中的用户：" + this.loginUser);
        },
    },
    mounted () {
        // 初始化页面数据
        initPage().then((res) => {
            if (res.code === 1) {
                this.users = res.data.users
                this.sings = res.data.sings
                this.songs = res.data.songs
            }
        }, (err) => {
            console.log(err)
        })
    },
};
</script>


<style scoped>
/* 基础样式 */
.login {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
}

.loginstep,
.loginstep2 {
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

/* 下拉框样式 */
.userSelect {
    width: 100%;
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

/* 复选框样式 */
.alltag {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 15px 0;
}

.tagbox {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 10px;
    background: #f0f0f0;
    border-radius: 4px;
}

.tagbox input {
    margin-right: 5px;
}

/* 按钮样式 */
.nextBtn,
.skip,
.go {
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
}

.nextBtn {
    background: #4CAF50;
    color: white;
}

.skip {
    background: #bbb;
    color: white;
}

.go {
    background: #2196F3;
    color: white;
}

.twobtn {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 15px;
}

/* 下拉框箭头样式（模拟） */
.select-hide-span {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
}

.select-show-b {
    display: inline-block;
    border-style: solid;
    border-width: 5px 5px 0 5px;
    border-color: #777 transparent transparent transparent;
    width: 0;
    height: 0;
}
</style>