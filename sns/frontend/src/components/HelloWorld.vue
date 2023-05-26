<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div>
      {{ text }}
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HelloWorld",
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
      .get("/api/v1/sample")
      .then((response) => (this.text = response.data))
      .catch((e) => console.log(e));
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

