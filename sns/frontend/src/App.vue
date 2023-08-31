<template>
    <div>
        Home
    </div>
</template>

<script>
import router from "./router";
export default {
  name: "App",
  mounted() {
    this.checkLoggedIn();
  },
  methods: {
    checkLoggedIn() {
        router.push('/login');
    }
  }
};
</script>