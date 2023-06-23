<template>
  <div class="login">
    <form @submit.prevent="login">
      <input type="text" v-model="email">
      <input type="text" v-model="password">
      <button type="submit">login</button>
    </form>
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
      tokens: {
        "refresh":'',
        "access":'',
      },
      email: "",
      password: "",
    };
  },
  methods: {
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