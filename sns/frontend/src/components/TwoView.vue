<template>
  <div class="hello">
    <div class="title-color">d [[ text ]] b</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TwoView",
  props: {
    msg: String,
  },
  data() {
    return {
      text: null,
    };
  },
  mounted() {
    axios
      .get("http://localhost:8000/api/v1/datetime/")
      .then((response) => (this.text = response.data))
      .then(response=>{
        console.log("status:",response.status)
        console.log("axiosGetData:",response.data)
      })
      .catch(err=>{
        console.log("axiosGetErr",err)
      })
  },
};
</script>

<style scoped>
.title-color {
  color: blue;
}
</style>