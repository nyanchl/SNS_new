<template>
  <div class="hello">
    <div class="title-color">d [[ texts ]] b</div>
    <div v-for="(text,user,id) in texts" :key="id">
        <p>[[ text.user ]]</p>
        <p>[[ text.text ]]</p>
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
  // computed: {
  //   sortedTexts() {
  //       const texts = this.texts
  //       return _sortBy(texts,'id').reverse();
  //   }
  // },
  // computed: {
  //   sortedTexts() {
  //     return this.texts.sort((a,b) => a.id - b.id)
  //   }
  // },
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