<template>
  <div class="hello">
    <div class="col-3">
      <button type="submit" class="btn btn-primary mt-auto">投稿</button>
    </div>
    <div class="title-color">d [[ texts ]] b</div>
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
  name: "OneView",
  props: {
    msg: String,
  },
  data() {
    return {
      texts: null,
    };
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