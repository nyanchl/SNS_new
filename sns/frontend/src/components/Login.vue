<template>
  <div>
    <div class="login">
      <form @submit.prevent="login">
        email<input type="text" v-model="email">
        password<input type="text" v-model="password">
        <button type="submit">login</button>
      </form>
    </div>
    <p>aaa</p>
    <button @click="getInfo">メンバー情報を取得</button>
    <div v-for="(member, key) in User" :key="key">
      <hr>
      <p>{{ member.username }}</p>
      <hr>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginView",
  props: {
    msg: String,
  },
  data() {
    return {
      User: [],
      tokens: {
        "refresh":'',
        "access":'',
      },
      email: "",
      password: "",
    };
  },
  methods: {
    getInfo: function(){
      axios
      .get("http://localhost:8000/api-auth/jwt/",{headers: {
        // postmanでのAPIcal同様にJWTが必要
        // この通信がうまくいかない時はchromeの検証モード/networkから確認できる
        "Authorization": 'JWT ' + this.tokens.access,
      }
      })
      // レスポンスをMembersプロパティに格納
      .then(response => (this.User = response.data));
      console.log(this.User)
    },
    login(){
      // token取得のためのusernameとpasswordセット
      const data = {email: this.email, password: this.password}
      // access_token&refresh_tokenを取得
      axios
        .post("http://localhost:8000/api-auth/jwt",data)
        // レスポンスを一旦tokensプロパティに格納
        .then(response => (this.tokens = response.data));
    }
  },
};
</script>

<style scoped>
.title-color {
  color: green;
}
</style>