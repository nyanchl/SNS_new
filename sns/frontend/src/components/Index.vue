<template>
  <div class="hello">
    <form @submit.prevent="createNewTexts">
      <div class="col-9">
        <input type="text" class="form-control" v-model="postTexts" >
      </div>
      <div class="col-3">
        <button type="submit" class="btn btn-primary mt-auto">投稿を追加</button>
      </div>
    </form>
    <div v-for="(text,user,id) in texts" :key="id">
      <table>
        <thread>
          <tr>
          <th>[[ text.user ]]</th>
          </tr>
        </thread>
      </table>
      <tbody>
        <tr>
          <td>[[ text.text ]]</td>
        </tr>
      </tbody>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Index",
  props: {
    msg: String,
  },
  data() {
    return {
      texts: null,
    };
  },
  methods: {
    createNewTexts(){
      axios
        .post("http://localhost:8000/api/text/",{"text":this.postTexts})
        .then(response => this.texts(response.data))
        .catch(console.log(this.postTexts))
    },
  },
  mounted() {
    axios
      .get("http://localhost:8000/api/text/")
      .then((response) => (this.texts = response.data))
      .then(response=>{
        console.log("data:",response.data)
        
      })
      .catch(err=>{
        console.log("axiosGetErr",err)
      })
  },
};
</script>

<style scoped>
.title-color {
  color: green;
}
</style>