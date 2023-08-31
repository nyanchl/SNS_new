<template>
  <div>
    <div class="login">
      <form @submit.prevent="login">
        email<input type="text" v-model="email">
        password<input type="text" v-model="password">
        <button type="submit">login</button>
      </form>
    </div>
    <button @click="getInfo">User情報を取得</button>
    <div v-for="(user, uuid) in User" :key="uuid">
      <hr>
      <p>[[ user.name ]]</p>
      <hr>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import router from "../router";

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
      name: "",
      username: "",
    };
  },
  methods: {
    getInfo: function(){
      axios
      .get("http://localhost:8000/api/user/",{headers: {
        "Authorization": 'JWT ' + this.tokens.access,
      }
      })
      .then(response => (this.User = response.data));
      this.$session.start();
      this.$session.set('user', this.User)
      router.push('/');
    },
    login(){
      // token取得のためのusernameとpasswordセット
      const data = {email: this.email, password: this.password}
      // access_token&refresh_tokenを取得
      axios
        .post("http://localhost:8000/api-auth/jwt",data)
        .then(response => (this.tokens = response.data));
        this.$session.start();
        this.$session.set('token', this.tokens)
        router.push('/');
    }
  },
};
</script>

<style scoped>
.title-color {
  color: green;
}
</style>