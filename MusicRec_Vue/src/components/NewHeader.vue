<template>
    <div class="reHeader">
        <div class="headTop">
            <img class="topLogo" src="../assets/img/logo.png" />
            <div class="userbtn">
            {{ getName }}，您好 
            <span @click="waitlayout" class="layouticon">切换用户</span>
            </div>
        </div>
      <ul class="headNav">
        <li 
          v-for="item in datas" 
          :key="item.cate_id" 
          @click="emitGetNews(item.cate_id)"
          :class="active === Number(item.cate_id) ? 'navActive' : ''"
        >
          {{ item.cate_name }}
        </li>
        <li><a class="adminlink" :href="serverlink" target="_blank">进入后台</a></li>
      </ul>
    </div>
</template>
  
<script>
import { mapGetters, mapActions } from 'vuex'
import { getCateData, layout } from '../assets/js/api'
import { serverUrl } from '../assets/js/linkBase'

export default {
props: {
    active: {
    type: Number,
    required: true
    }
},
data() {
    return {
    datas: [],
    serverlink: ''
    }
},
computed: {
    ...mapGetters('vuexlogin', {
    getName: 'getName'
    })
},
methods: {
    ...mapActions('vuexlogin', ['almuta', 'almuuser']),
    emitGetNews(cateid) {
    this.$emit('on-get-news', { cateid: Number(cateid) }) // 统一事件名并确保数字类型
    },
    // 其他方法保持不变...
},
mounted() {
    this.serverlink = `${serverUrl}/admin/`
    this.getCates()
}
}
</script>