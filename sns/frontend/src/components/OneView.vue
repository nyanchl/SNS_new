<template>
  <div class="hello">
    <div class="title-color">d [[ texts ]] b</div>
    <p v-for="(text,id) in texts" :key="id">
        [[ text.text ]]
    </p>
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