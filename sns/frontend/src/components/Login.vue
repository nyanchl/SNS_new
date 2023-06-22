<template>
  <div class="login">
    <input type="text" v-model="email">
    <input type="text" v-model="password">
    <button @click="login">login</button><hr>
  </div>
</template>

<script>
// import axios from "axios";

export default {
  name: "LoginView",
  props: {
    msg: String,
  },
  data() {
    return {
      tokens: {
        "refresh":'',
        "access":'',
      },
      email: '',
      password: '',
    };
  },
  methods: {
    login: function(){
      // token取得のためのusernameとpasswordセット
      const data = {email: this.email, password: this.password}
      // access_token&refresh_tokenを取得
      this.axios
        .post("http://localhost:8000/api-auth/jwt/",data)
        // レスポンスを一旦tokensプロパティに格納
        .then(response => (this.tokens = response.data));
        console.log(this.tokens);
    }
  },
};
</script>

<style scoped>
.title-color {
  color: green;
}
</style>